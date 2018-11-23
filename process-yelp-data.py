import json
import pandas as pd
import csv

# read yelp business data
df = pd.read_pickle("pkl-data/data.pkl")

# read food terms data
file = open("raw-data/food_terms.txt", "r")
file_lines = file.read().splitlines()

# regex to match whole word
food_words = "|".join(file_lines)
food_words = ".*\\b("+food_words+")\\b.*"

# get all businesses that's in toronto, open, and has a neighborhood
df_toronto = df.loc[(df['city'].isin(['Toronto'])) & (df['is_open'] == True) & (df['neighborhood'] != "")]

# get all restaurants in toronto
df_toronto_rest = df_toronto[df_toronto["categories"].str.contains(food_words, case=False, na=False)]

# drop not need columns
df_toronto_rest.drop(columns=["address", "business_id", "city", "latitude", "longitude", "name", "state", "hours.Friday", "hours.Saturday", "hours.Sunday", "is_open", "attributes.BikeParking", "attributes.WheelchairAccessible", "categories"], inplace=True)

# replace NaN values in some columns with default values
df_toronto_rest["attributes.Alcohol"].fillna("none", inplace=True)
df_toronto_rest["attributes.NoiseLevel"].fillna("average", inplace=True)
df_toronto_rest["attributes.RestaurantsAttire"].fillna("casual", inplace=True)
df_toronto_rest["attributes.Smoking"].fillna("no", inplace=True)
df_toronto_rest["attributes.WiFi"].fillna("no", inplace=True)

# count NaN values for each column
print(df_toronto_rest.isna().sum())

# clean car parking attribute
df_toronto_rest.loc[df_toronto_rest["attributes.BusinessParking"].str.contains('True', na=False), "attributes.BusinessParking"] = 'True'
df_toronto_rest.loc[~df_toronto_rest["attributes.BusinessParking"].str.contains('True', na=False), "attributes.BusinessParking"] = 'False'

# drop NaN
df_toronto_rest = df_toronto_rest.dropna()

# rename column headers
df_toronto_rest.columns = [
    "alcohol",
    "businessAcceptsCreditCards",
    "businessParking",
    "goodForKids",
    "noiseLevel",
    "restaurantsAttire",
    "restaurantsDelivery",
    "restaurantsGoodForGroups",
    "restaurantsPriceRange",
    "restaurantsReservations",
    "restaurantsTakeOut",
    "smoking",
    "wiFi",
    "neighborhood",
    "postal_code",
    "review_count",
    "stars"
]

# pickle data for future use
df_toronto_rest.to_pickle("pkl-data/df_toronto_restaurants.pkl")

# write to CSV
df_toronto_rest.to_csv("df_toronto_restaurants.csv", index=False)

# column headers
headers = list(df_toronto_rest.columns.values)

print (df_toronto.shape)
print (df_toronto_rest.shape)
