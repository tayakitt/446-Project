from matplotlib import pyplot as plt
from sklearn.model_selection import cross_val_score, cross_val_predict, KFold
from sklearn import metrics
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

# load data
df = pd.read_pickle('pkl-data/no_wards.pkl')

# features to include
features = [
    "review_count",
    "restaurantsGoodForGroups_False",
    "businessParking_False",
    "noiseLevel_quiet",
    "noiseLevel_average",
    "businessAcceptsCreditCards_False",
    "noiseLevel_very_loud",
    "restaurantsPriceRange_2",
    "restaurantsPriceRange_1",
    "restaurantsPriceRange_3",
    "restaurantsAttire_casual",
    "restaurantsDelivery_False",
    "restaurantsAttire_formal",
    "restaurantsTakeOut_False",
    "Citizenship_Canadian_citizens_aged_18_and_over",
    "Canada_Generation_status_Second_generation",
    "Canada_Generation_status_First_generation",
    "Citizenship_Not_Canadian_citizens",
    "Canada_Generation_status_Third_generation_or_more",
    "Citizenship_Canadian_citizens_aged_under_18",
    "Ethnic_Origin_Asian_origins",
    "Ethnic_Origin_East_and_Southeast_Asian_origins",
    "Ethnic_Origin_South_Asian_origins",
    "Ethnic_Origin_West_Central_Asian_and_Middle_Eastern_origins",
    "Citizenship_Canadian_citizens",
    "Marital_Status_Married_or_living_common_law",
    "Marital_Status_Married",
    "Marital_Status_Living_common_law",
    "Work_location__Worked_at_usual_place",
    "Class_of_worker__Employee",
    "Class_of_worker__Self_employed",
    "Household_status_Without_children_in_household",
    "Ethnic_Origin_Other_African_origins"
]

y_df = df['stars'].copy()
x_df = df[features].copy()

kf = KFold(n_splits=10)

# using sklearn
lm = LinearRegression()
predictions = cross_val_predict(lm, x_df, y_df, cv=kf)
plt.scatter(y_df, predictions)
plt.xlabel("Actual Star")
plt.ylabel("Predicted Star")
plt.title("Acutal Star Rating VS Predicted")
plt.show()

# accuracy score of different folds
scores = cross_val_score(lm, x_df, y_df, cv=kf)
print("Accuracy: %0.5f (+/- %0.5f)" % (scores.mean(), scores.std() * 2))

accuracy = metrics.r2_score(y_df, predictions)
print("R2: {}".format(accuracy))


# manual way
# for train_index, test_index in kf.split(X):
#     print("TRAIN:", train_index, "TEST:", test_index)
#     X_train, X_test = X[train_index], X[test_index]
#     y_train, y_test = y[train_index], y[test_index]
#     lm.fit(X_train, y_train)
#     pred = lm.predict(X_test)