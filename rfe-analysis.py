

# df = pd.read_pickle("pkl-data/df_toronto_restaurants.pkl")
# headers = list(df.columns.values)
# print(len(headers))

from sklearn.datasets import make_friedman1
from sklearn.feature_selection import RFE
from sklearn.svm import SVR
import pandas as pd

X, y = make_friedman1(n_samples=50, n_features=10, random_state=0)
estimator = SVR(kernel="linear")
selector = RFE(estimator, 5, step=1)
selector = selector.fit(X, y)
print(selector.support_)


print(selector.ranking_)


df_toronto_rest = pd.read_pickle("pkl-data/df_toronto_restaurants.pkl")

print("something")