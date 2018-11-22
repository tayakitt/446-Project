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
df_toronto = df.loc[(df['city'].isin(['Toronto'])) & (df['is_open']==True) & (df['neighborhood']!="")]

# get all restaurants in toronto
df_toronto_rest = df_toronto[df_toronto["categories"].str.contains(food_words, case=False, na=False)]

# pickle data for future use
df_toronto_rest.to_pickle("pkl-data/df_toronto_restaurants.pkl")

# drop not need columns
df_toronto_rest.drop(columns=["address", "business_id", "city", "hours.Friday", "hours.Saturday", "hours.Sunday", "is_open", "latitude", "longitude", "name", "postal_code", "state"], inplace=True)

# write to CSV
df_toronto_rest.to_csv("df_toronto_restaurants.csv", index=False)

# column headers
headers = list(df_toronto.columns.values)

print (df_toronto.shape)
print (df_toronto_rest.shape)
