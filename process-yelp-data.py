import json
import pandas as pd

# reading the JSON data using json.load()
file = 'data/process-yelp-data.py'
with open(file) as train_file:
    dict_train = json.load(train_file)

# converting json dataset from dictionary to dataframe
train = pd.DataFrame.from_dict(dict_train, orient='index')
train.reset_index(level=0, inplace=True)