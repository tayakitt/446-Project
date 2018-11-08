import json
import pandas as pd

df = pd.read_pickle("data.pkl")
print(list(df.columns.values))

# get all restaurants in toronto that is open
df_toronto = df.loc[(df['city'].isin(['Toronto'])) & (df['is_open']==True)]


print (df_toronto.neighborhood.unique().tolist())
print (df_toronto.shape)