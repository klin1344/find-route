import json
from collections import defaultdict
import datetime
import math


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
        counts[tuple(map(lambda x: round(x / 10000000.0, 2),
                         [loc_point["latitudeE7"], loc_point["longitudeE7"]]))] += 1
    max_coord = max_freq(counts)
    route.append(max_coord)
    counts.pop(max_coord)
    route.append(max_freq(counts))
    return route

with open('location.json') as data_file:
    loc_json = json.load(data_file)

print get_route(loc_json)
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
