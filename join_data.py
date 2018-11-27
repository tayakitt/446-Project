import json
import pandas as pd
from pandas.io.json import json_normalize
import csv
import collections
import numpy

nbh_names = []
with open('raw-data/toronto_hoods.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        nbh_names.append(row[0])

postals = {}
with open('raw-data/postal_mapping.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        postals[row[2]] = row[0]

yelp_mapping = {}
with open('raw-data/yelp_mapping.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[1] != "#N/A":
            yelp_mapping[row[0]] = row[1]

hood_to_ward = {}
with open('raw-data/hood-to-ward.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        hood_to_ward[row[0]] = row[1]

# searches array of names to see if they contain a nbhd name
def contains_hood(hood_name, all_names):
    for name in all_names:
        if hood_name in name:
            return name
    return False


postal_to_nbh = {} # maps postal codes to toronto nbhds
for hood in postals:
    if hood in nbh_names:
        postal_to_nbh[postals[hood]] = hood
    else:
        hood_name = contains_hood(hood, nbh_names)
        if hood_name:
            postal_to_nbh[postals[hood]] = hood_name

# read in downtown core postal to nbhd mappings
with open('raw-data/unmatched_dt_postals_mapped.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        postal_to_nbh[row[0]] = row[1]

# read in etobicoke postal to nbhd mappings
with open('raw-data/etob_postal-code-match.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        postal_to_nbh[row[0]] = row[1]

# read in all toronto neighborhood data
hood_data = pd.read_csv("raw-data/toronto-data.csv").transpose()
hood_data.columns = hood_data.iloc[0]
hood_data.drop(hood_data.index[0], inplace=True)
hood_data.drop(hood_data.index[0], inplace=True)
hood_data["neighborhood"] = [w.replace("_", " ") for w in hood_data.index.values]

# read in all ward data
ward_data = pd.read_csv("raw-data/ward-data.csv").transpose()
ward_data.columns = ward_data.iloc[0]
ward_data.drop(ward_data.index[0], inplace=True)
ward_data["Ward"] = ward_data.index.values

# assign wards to neighbourhoods
ward_column = []
unmatched_ward = []
for index, row in hood_data.iterrows():
    neighborhood = index.replace("_", " ")
    if neighborhood in hood_to_ward:
        ward_column.append("Ward " + hood_to_ward[neighborhood])
    else:
        unmatched_ward.append(neighborhood)
        ward_column.append(None)

# add ward column
hood_data["Ward"] = ward_column

# merge nbhd and wards
hoods_and_wards = pd.merge(hood_data, ward_data, on="Ward", how="inner")
hoods_and_wards.index = hoods_and_wards["neighborhood"]

print(hoods_and_wards["neighborhood"])

# read in cleaned toronto restaurant data
toronto_rest = pd.read_pickle("pkl-data/df_toronto_restaurants.pkl")

# iterate through toronto restaurants and map to neighborhoods
neighborhood_keys = []
not_matched_nbhd = []
not_matched_postal = []
for index, row in toronto_rest.iterrows():
    postal_code = row["postal_code"].split(" ")[0]
    if row["neighborhood"] in yelp_mapping:
        neighborhood_keys.append(yelp_mapping[row["neighborhood"]])
    elif postal_code in postal_to_nbh:
        neighborhood_keys.append(postal_to_nbh[postal_code])
    elif row["postal_code"] in postal_to_nbh:
        neighborhood_keys.append(postal_to_nbh[row["postal_code"]])
    else:
        not_matched_nbhd.append(row["neighborhood"])
        not_matched_postal.append(row["postal_code"])
        neighborhood_keys.append(None)

print(neighborhood_keys.count(None))


# view which restaurants don't have a neighborhood
counter = collections.Counter(not_matched_nbhd)
print(counter.most_common(5))

counter2 = collections.Counter(not_matched_postal)
print((set(not_matched_postal)))

# add neighbourhood key to toronto rest data
hoods_and_wards.reset_index(drop=True, inplace=True)
toronto_rest["neighborhood_key"] = neighborhood_keys

# join toronto restaurants with hoods and wards
result = pd.merge(toronto_rest, hoods_and_wards, left_on="neighborhood_key", right_on="neighborhood", how="inner")

# write to a pickle
result.to_pickle("pkl-data/toronto_rest_and_hoods.pkl")
print(result)

print(hoods_and_wards.shape)

# new dataframe with neighborhoods and stars
stars = result["stars"]
hoods_and_wards["stars"] = stars
hoods_and_wards.drop(columns=["Ward", "neighborhood"], inplace=True)

#save to pickle
hoods_and_wards.to_pickle("pkl-data/hoods_and_stars.pkl")

#save to csv
hoods_and_wards.to_csv("raw-data/hoods-and-stars.csv", index=False)