import json
import pandas as pd
from pandas.io.json import json_normalize

test_data = {
    "business_id": "tnhfDv5Il8EaGSXZGiuQGg",
    "name": "Garaje",
    "neighborhood": "SoMa",
    "address": "475 3rd St",
    "city": "San Francisco",
    "state": "CA",
    "postal code": "94107",
    "latitude": 37.7817529521,
    "longitude": -122.39612197,
    "stars": 4.5,
    "review_count": 1198,
    "is_open": 1,
    "attributes": {
        "RestaurantsTakeOut": True,
        "BusinessParking": {
            "garage": False,
            "street": True,
            "validated": False,
            "lot": False,
            "valet": False
        },
    },
    "categories": [
        "Mexican",
        "Burgers",
        "Gastropubs"
    ],
    "hours": {
        "Monday": "10:00-21:00",
        "Tuesday": "10:00-21:00",
        "Friday": "10:00-21:00",
        "Wednesday": "10:00-21:00",
        "Thursday": "10:00-21:00",
        "Sunday": "11:00-18:00",
        "Saturday": "10:00-21:00"
    }
}

# https://stackoverflow.com/questions/21104592/json-to-pandas-dataframe
# reading the JSON data using json.load()
# file = 'data/yelp_academic_dataset_business.json'
# with open(file) as f:
#     data = json.load(f)

# train = pd.DataFrame.from_dict(data, orient='index')
# train.reset_index(level=0, inplace=True)

# https://stackoverflow.com/questions/34341974/nested-json-to-pandas-dataframe-with-specific-format
df = pd.io.json.json_normalize(test_data)
df.columns = df.columns.map(lambda x: x.split(".")[-1])

