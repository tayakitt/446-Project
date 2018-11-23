from pandas import read_csv
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from matplotlib import pyplot as plt
import pandas as pd

# load data
df = pd.read_pickle('pkl-data/df_toronto_restaurants.pkl')
df.drop(columns=["postal_code", "neighborhood"], inplace=True)

# One-hot-encoding
df = pd.get_dummies(df)

# set explanatory and prediction data
Y = df["stars"]
X = df.drop("stars", axis=1)

# split data for test and train
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
print (X_train.shape, y_train.shape)
print (X_test.shape, y_test.shape)

# fit model
lm = LinearRegression()
model = lm.fit(X_train, y_train)

# get predictions of model
predictions = lm.predict(X_test)

# plot results
plt.scatter(y_test, predictions)
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()

# accuracy score
score = model.score(X_test, y_test)
print("model score: {}".format(score))
