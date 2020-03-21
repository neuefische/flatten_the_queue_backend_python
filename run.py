#imports
import populartimes
import pandas as pd
import json

# read json file with lat and lng input, till now no radius, radius is set by default to 1 km
json1_file = open("user_data.json")
json1_str = json1_file.read()
json1_data = json.loads(json1_str)

# Larissas api_key, feel free to change
api_key = "AIzaSyD7MB-Afk1X3Buu0brPpYO3SK_2DILXtYQ"

# types of locations that should be considered.
# others are 'supermarket', 'food', check here:
types = ["grocery_or_supermarket"]

# default values for boundrys ( +/- 0.01)
bound_lower = (json1_data['lat']-0.01, json1_data['lng']-0.01)
bound_upper = (json1_data['lat']+0.01, json1_data['lng']+0.01)
n_threads = 20
# default
radius = 1000
all_places = False

results = populartimes.get(api_key, types, bound_lower, bound_upper, n_threads,  radius, all_places)


# create DataFrame to split Address in street and city
df = pd.DataFrame(results)
df = df.fillna(1000)
df['street'] = df['address'].str.split(', ', n=1, expand=True)[0]
df['city'] = df['address'].str.split(', ', n=1, expand=True)[1]

# extract important info
columns = ['name', 'id', 'street', 'city', 'current_popularity']
df = df[columns]

# convert to json
df.to_json(r'output.json', orient='records')

# check for consistency
# df.to_csv(r'df2.csv', index=False)
