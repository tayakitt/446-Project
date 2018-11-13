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

print(yelp_mapping)
print(postals)
print(nbh_names)

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

