from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
import pandas as pd

# load data
yelp_df = pd.read_pickle('pkl-data/df_toronto_restaurants.pkl')
yelp_df.drop(columns=["postal_code", "neighborhood"], inplace=True)
yelp_df = pd.get_dummies(yelp_df)
num_attributes = len(yelp_df.columns) - 1

y_array = yelp_df.values

Y = y_array[:,1]
x_df = yelp_df.drop(columns=["stars"])
X = x_df.values

yelp_features = x_df.columns.values

# feature extraction
model = LinearRegression()
rfe = RFE(model, num_attributes)
fit = rfe.fit(X, Y)
print("Num Features: %d" % (fit.n_features_,))
print("Selected Features: %s" % (fit.support_,))
print("Feature Ranking: %s" % (fit.ranking_,))

rest_and_hoods = pd.read_pickle('pkl-data/toronto_rest_and_hoods.pkl')
rest_and_hoods.drop(columns=["neighborhood_x", "postal_code", "neighborhood_key"], inplace=True)

rest_hoods_array = rest_and_hoods.values

YY = rest_hoods_array[:, 1]
XX = rest_and_hoods.drop(columns=["stars"]).values

rest_and_hoods_features = rest_and_hoods.drop(columns=["stars"]).columns.values

num_attributes2 = len(rest_and_hoods_features)

rfe2 = RFE(model, num_attributes2)
fit2 = rfe2.fit(XX, YY)
print("Num Features: %d" % (fit2.n_features_,))
print("Selected Features: %s" % (fit2.support_,))
print("Feature Ranking: %s" % (fit2.ranking_,))
