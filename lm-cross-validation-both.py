from matplotlib import pyplot as plt
from sklearn.model_selection import cross_val_score, cross_val_predict, KFold
from sklearn import metrics
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

# load data
df = pd.read_pickle('pkl-data/hoods_and_stars.pkl')
# df.drop(columns=["neighborhood_x", "postal_code", "neighborhood_key", "Ward", "neighborhood_y"], inplace=True)

# features to include
features = [
    "Canada_Generation_status_First_generation",
    "Citizenship_Canadian_citizens",
    "Canada_Generation_status_Second_generation",
    "Canada_Generation_status_Third_generation_or_more",
    "Citizenship_Not_Canadian_citizens",
    "Labour_Force_In_the_labour_force",
    "Education_Total_Highest_certificate_diploma_or_degree_for_the_population_aged_15_years_and_over_in_private_households_25percent_sample_data",
    "Labour_Force_Not_in_the_labour_force",
    "Marital_Status_Married_or_living_common_law",
    "Marital_Status_Married",
    "Marital_Status_Living_common_law",
    "Marital_Status_Not_married_and_not_living_common_law",
    "Marital_Status_Never_married",
    "Marital_Status_Divorced",
    "Migration_Mobllity_and_Languages_2001_to_2005",
    "Migration_Mobllity_and_Languages_2001_to_2010",
    "Migration_Mobllity_and_Languages_2006_to_2010",
    "Marital_Status_Widowed",
    "Marital_Status_Separated",
    "Ethnic_Origin_East_and_Southeast_Asian_origins",
    "Ethnic_Origin_Asian_origins",
    "Ethnic_Origin_South_Asian_origins",
    "Ethnic_Origin_West_Central_Asian_and_Middle_Eastern_origins",
    "Class_of_worker__All_classes_of_workers",
    "Class_of_worker__Employee",
    "Work_location__Worked_at_usual_place",
    "Work_location__Worked_at_home",
    "Household_status_Single_person_household",
    "Household_status_With_children_in_household",
    "Ethnic_Origin_European_origins",
    "Ethnic_Origin_Central_and_West_African_origins"
]

y_df = df['stars'].copy()
x_df = df[features].copy()
# x_df = df.copy().drop(columns="stars")

# set explanatory and prediction data
# X = np.array(x_df.values)
# Y = np.array(y_df.values)

kf = KFold(n_splits=10)

# using sklearn
lm = LinearRegression()
predictions = cross_val_predict(lm, x_df, y_df, cv=kf)
plt.scatter(y_df, predictions)
plt.xlabel("Actual Star")
plt.ylabel("Predicted Star")
plt.title("Acutal Star Rating VS Predicted Star Rating")
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