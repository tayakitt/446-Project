from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression, LinearRegression
import pandas as pd
import operator
import csv


def rfe(class_name, df, top_num):

    y = df[class_name].values
    x = df.drop(columns=[class_name]).values

    model = LinearRegression()

    features = df.drop(columns=[class_name]).columns.values

    rfe = RFE(model, 1)
    fit = rfe.fit(x, y)

    print("Num Features: %d" % (fit.n_features_,))
    print("Selected Features: %s" % (fit.support_,))
    print("Feature Ranking: %s" % (fit.ranking_,))
    coeffs = rfe.estimator_.coef_
    print('coefficients', coeffs)

    features_rankings = {}
    features_coeff = {}
    index = 0
    for rank in fit.ranking_:
        features_rankings[features[index]] = rank
        if (index < len(coeffs)):
            features_coeff[features[index]] = coeffs[index]
        index += 1

    features_rankings = sorted(features_rankings.items(), key=operator.itemgetter(1), reverse=False)
    print(features_rankings)
    print(features_coeff)
    return features_rankings


def toCsv(filename, data):
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for row in data:
            writer.writerow(row)


# rfe for yelp data
yelp_df = pd.read_pickle('pkl-data/df_toronto_restaurants.pkl')
yelp_df.drop(columns=["postal_code", "neighborhood"], inplace=True)
yelp_df = pd.get_dummies(yelp_df)

features = ["noiseLevel_very_loud",
"noiseLevel_quiet",
"noiseLevel_average",
"wiFi_free",
"wiFi_paid",
"restaurantsPriceRange_3",
"restaurantsPriceRange_2",
"restaurantsPriceRange_1",
"restaurantsGoodForGroups_False",
"businessParking_False",
"smoking_yes",
"smoking_outdoor",
"restaurantsTakeOut_False",
"restaurantsReservations_False",
"restaurantsAttire_casual",
"restaurantsAttire_formal",
"goodForKids_False",
"restaurantsDelivery_False",
"businessAcceptsCreditCards_False",
"review_count",
"alcohol_none",
"alcohol_full_bar",
"stars"]

yelp_df = yelp_df[features]

print("Yelp data")
toCsv("yelp-feature-ranks.csv", rfe("stars", yelp_df))

# rfe for hoods and stars
hoods_and_stars = pd.read_pickle("pkl-data/hoods_and_stars.pkl")
hoods_and_stars.drop(columns=["neighborhood", "Ward"], inplace=True)

print("neighborhoods and stars")
toCsv("neighorhood-feature-ranks.csv", rfe("stars", hoods_and_stars))

# rfe for joined data
rest_and_hoods = pd.read_pickle('pkl-data/toronto_rest_and_hoods.pkl')
rest_and_hoods.drop(columns=["neighborhood_x", "postal_code", "neighborhood_key", "Ward", "neighborhood_y"], inplace=True)

print("joined data")
toCsv("joined-features-ranks.csv", rfe("stars", rest_and_hoods))

