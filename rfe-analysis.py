from sklearn.datasets import make_friedman1
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
import pandas as pd

df = pd.read_pickle("pkl-data/df_toronto_restaurants.pkl")
headers = list(df.columns.values)
print(headers)

predictor = df["stars"]
