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

df = pd.io.json.json_normalize(test_data)
df.columns = df.columns.map(lambda x: x.split(".")[-1])

data = []
filename = "yelp_academic_dataset_business.json"
with open(filename) as f:
    counter = 0
    for line in f:
        data.append(line)

a = pd.concat([pd.DataFrame(pd.io.json.json_normalize(json.loads(data[i])), columns=df.columns) for i in range(len(data))], ignore_index=True)
a.to_pickle("data.pkl")

