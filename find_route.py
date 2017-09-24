import os
import sys
import json
from os.path import join, dirname
from dotenv import load_dotenv
from collections import defaultdict
from pymongo import MongoClient
import datetime
import math

dotenv_path = join(dirname(__file__), '.env')

load_dotenv(dotenv_path)
client = MongoClient(os.environ.get("MONGO_URI"))

db = client["hackrice"]
routes = db["locations"]

try:
    email = sys.argv[1]
except:
    raise ValueError("You must specify an email as the third argument")

def insertData(data):
    bulkInsertData = map(lambda info: {
        "lat": info[0],
        "lon": info[1],
        "timestamp": info[2],
        "frequency": data[info],
        "email": email
    }, data.keys())

    return routes.insert_many(bulkInsertData)

def max_freq(counts):
    max_count = 0
    max_coord = None
    for coord, count in counts.items():
        if count > max_count:
            max_count = count
            max_coord = coord
    return max_coord


def clean_locs(loc_json):
    # only get datapoints whose timestamps are on weekdays
    clean_locs = []
    for loc in loc_json["locations"]:
        weekday = datetime.datetime.fromtimestamp(
            int(loc["timestampMs"]) / 1000.0).weekday()
        if weekday >= 0 and weekday <= 4:
            clean_locs.append(loc)
    return clean_locs

def get_route(loc_json):
    route = []
    counts = defaultdict(int)
    cleaned = clean_locs(loc_json)
    for loc_point in cleaned:
        key = map(lambda x: round(x / 10000000.0, 2), [loc_point["latitudeE7"], loc_point["longitudeE7"]])
        key.append(round(float(loc_point["timestampMs"]), -8))
        counts[tuple(key)] += 1

    insertData(counts)

    max_coord = max_freq(counts)
    route.append(max_coord)
    counts.pop(max_coord)
    route.append(max_freq(counts))
    return route

with open(os.path.dirname(os.path.realpath(__file__)) + '/location.json') as data_file:
    loc_json = json.load(data_file)

sys.stdout.write(str(get_route(loc_json)))

# def match_routes(user_1, user_2):
#     route_1 = get_route(user_1[1])
#     route_2 = get_route(user_2[1])
#     for pair in zip(route_1, route_2):
#         if math.fabs(pair[0][0] - pair[1][0]) <= 0.13 and math.fabs(pair[1][0] - pair[1][1]) <= 0.13:
#             return True
#     return False

# print get_route()

# max_coord, max_count = max_freq(counts)
# print max_coord, max_count
# counts.pop(max_coord)

# max_coord, max_count = max_freq(counts)
# print max_coord, max_count
# counts.pop(max_coord)

# max_coord, max_count = max_freq(counts)
# print max_coord, max_count
# counts.pop(max_coord)

# max_coord, max_count = max_freq(counts)
# print max_coord, max_count
# counts.pop(max_coord)

# max_coord, max_count = max_freq(counts)
# print max_coord, max_count
# counts.pop(max_coord)

# max_coord, max_count = max_freq(counts)
# print max_coord, max_count
# counts.pop(max_coord)
