from sklearn.model_selection import KFold
from matplotlib import pyplot as plt
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn import metrics
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

# load data
df = pd.read_pickle('pkl-data/df_toronto_restaurants.pkl')
df.drop(columns=["postal_code", "neighborhood"], inplace=True)

# One-hot-encoding
df = pd.get_dummies(df)
y_df = df["stars"]

number_rows = len(df.index)

# set explanatory and prediction data
array = np.array(df.values)
Y = array[ :,1]
x_df = df.drop(columns=["stars"], axis=1)
X = x_df.values

kf = KFold(n_splits=number_rows-1)
kf.get_n_splits(X)

print(kf)

# for train_index, test_index in kf.split(X):
#     print("TRAIN:", train_index, "TEST:", test_index)
#     X_train, X_test = X[train_index], X[test_index]
#     y_train, y_test = y[train_index], y[test_index]

lm = LinearRegression()
predictions = cross_val_predict(lm, x_df, y_df, cv=number_rows-1)
plt.scatter(y_df, predictions)
plt.show()