import json
import pandas as pd
from pandas.io.json import json_normalize
import csv


nbh_names = []
with open('toronto_hoods.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        nbh_names.append(row[0])

postals = {}
with open('postal_mapping.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        postals[row[2]] = row[0]

yelp_mapping = {}
with open('yelp_mapping.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        yelp_mapping[row[0]] = row[1]

hood_to_ward = {}
with open('hood-to-ward.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        hood_to_ward[row[0]] = row[1]

print(yelp_mapping)
print(postals)
print(nbh_names)
print(hood_to_ward)

def contains_hood(hood_name, all_names):
    for name in all_names:
        if hood_name in name:
            return name

    return False

postal_to_nbh = {}

for hood in postals:
    if hood in nbh_names:
        postal_to_nbh[postals[hood]] = hood
    else:
        hood_name = contains_hood(hood, nbh_names)
        if hood_name:
            postal_to_nbh[postals[hood]] = hood_name

print(postal_to_nbh)
print(len(postal_to_nbh))
print(len(nbh_names))

def map_yelp_to_toronto(yelp_name):
    if yelp_name in yelp_mapping:
        return yelp_mapping[yelp_name]
    return False

hood_data = pd.read_csv("toronto-data.csv").transpose()
hood_data.columns = hood_data.iloc[0]
hood_data.reindex(hood_data.index.drop("Unnamed: 0"))
hood_data["nbhd"] = hood_data.index.values

ward_data = pd.read_csv("ward-data.csv").transpose()
ward_data.columns = ward_data.iloc[0]
ward_data.reindex(ward_data.index.drop("Unnamed: 0"))
ward_data["Ward"] = ward_data.index.values
print(ward_data)

# assign wards to neighbourhoods
ward_column = []
for index, row in hood_data.iterrows():
    if index in hood_to_ward:
        ward_column.append("Ward " + hood_to_ward[index])
    else:
        ward_column.append(None)

hood_data["Ward"] = ward_column
print(ward_column)

hoods_and_wards = pd.merge(hood_data, ward_data, on="Ward", how="outer")
hoods_and_wards.index = hoods_and_wards["nbhd"]

print(hoods_and_wards)

