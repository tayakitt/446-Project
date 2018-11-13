import json
import pandas as pd
from pandas.io.json import json_normalize

test_data = {
   'business_id':'AjEbIBw6ZFfln7ePHha9PA',
   'name':"CK'S BBQ & Catering",
   'neighborhood':'',
   'address':'',
   'city':'Henderson',
   'state':'NV',
   'postal_code':'89002',
   'latitude':35.9607337,
   'longitude':-114.939821,
   'stars':4.5,
   'review_count':3,
   'is_open':0,
   'attributes':{
      'Alcohol':'none',
      'BikeParking':'False',
      'BusinessAcceptsCreditCards':'True',
      'BusinessParking':"{'garage': False, 'street': True, 'validated': False, 'lot': True, 'valet': False}",
      'NoiseLevel': 'average',
      'GoodForKids':'True',
      'RestaurantsAttire':'casual',
      'RestaurantsDelivery':'False',
      'RestaurantsGoodForGroups':'True',
      'RestaurantsPriceRange2':'2',
      'RestaurantsReservations':'False',
      'RestaurantsTakeOut':'True',
      'Smoking': 'True',
      'WheelchairAccessible':'True',
      'WiFi':'no'
   },
   'categories':'Chicken Wings, Burgers, Caterers, Street Vendors, Barbeque, Food Trucks, Food, Restaurants, Event Planning & Services',
   'hours':{
      'Friday':'17:0-23:0',
      'Saturday':'17:0-23:0',
      'Sunday':'17:0-23:0'
   }
}

test_df = pd.io.json.json_normalize(test_data)
col_names = test_df.columns.values

# https://stackoverflow.com/questions/21058935/python-json-loads-shows-valueerror-extra-data
file = 'data/yelp_academic_dataset_business.json'

# df = pd.DataFrame()
# counter = 0
#
# for obj in open(file, 'r'):
#     print (counter)
#     business = json.loads(obj)
#     new_record = pd.DataFrame(pd.io.json.json_normalize(business), columns=col_names)
#     df = pd.concat([df, new_record], sort=True)
#
#     # if counter == 50:
#     #     break
#     counter += 1
#
# # save data
# df.to_pickle("data.pkl")

# print("\n\n")
# print(len(list(df.columns.values)))
# print(list(df.columns.values))

data = []
filename = "yelp_academic_dataset_business.json"
with open(filename) as f:
    counter = 0
    for line in f:
        data.append(line)

a = pd.concat([pd.DataFrame(pd.io.json.json_normalize(json.loads(data[i])), columns=col_names) for i in range(len(data))], ignore_index=True)
a.to_pickle("data.pkl")

print(a)

