import json
import pandas as pd
import csv

df = pd.read_pickle("data.pkl")

# get all restaurants in toronto that is open
df_toronto = df.loc[(df['city'].isin(['Toronto'])) & (df['is_open']==True)]

distinct_neighborhood = df_toronto.neighborhood.unique().tolist()

print (df_toronto.shape)

with open("output.csv", "w") as f:
    for d in distinct_neighborhood:
        print(d)
        f.write(d + '\n')

