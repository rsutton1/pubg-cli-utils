import requests
import time
import json
import os
import argparse

# get_player_json
#
# Returns the raw json of the player's stats from the API
def get_player_json(player):
    url = "https://pubgtracker.com/api/profile/pc/%s" % (player)
    headers = {'TRN-Api-Key': os.environ["PUBG_API_KEY"]}
    r = requests.get(url, headers=headers)
    return r.json()

# filter_dict
#
# This helper function removes all the keys from the dictionary
# except for the keys passed into the function
def filter_dict(dict_unfiltered, keys):
    return { key : dict_unfiltered[key] for key in keys }

# parsePlayerStats
#
# This turns the json stats list into a convenient
# dictionary with the stat name as the key.
#
# input:
#   player_stats_raw: the player stats as a list of attributes
#
# output:
#   a stats dictionary with the stat name as the key and
#   the stat value as the value
def parsePlayerStats(player_stats_raw):
    player_stats = {}
    for stat in player_stats_raw:
        stat_name = stat["field"]
        stat_value = stat["value"]
        player_stats[stat_name] = stat_value
    return player_stats

# getPlayerStats
#
# This gets the json of a player's stats given the match_type and
# region.
#
# inputs:
#   player_json: the json blob for the player
#   match_type: the type of match
#     values: solo, duo, or squad
#   region: the region for the stats
#     values: na or agg
#
# output:
#   A json blob of the player's stats
def getPlayerStats(player_json, match_type, region):
    for stats_meta in player_json["Stats"]:
        if stats_meta["Match"] == match_type and stats_meta["Region"] == region:
            player_stats_raw = stats_meta["Stats"]
            return parsePlayerStats(player_stats_raw)

# Parse the arguments to get players to compare
parser = argparse.ArgumentParser()
parser.add_argument("players", nargs="+")
args = parser.parse_args()

region = "agg"
match_type = "solo"
stats = ["KillDeathRatio","WinRatio","Rating"]

all_stats = {}

for player in args.players:
    player_json = get_player_json(player)
    player_stats_all = getPlayerStats(player_json, match_type, region)
    player_stats_filtered = filter_dict(player_stats_all, stats)
    all_stats[player] = player_stats_filtered
    time.sleep(1)

print(all_stats)
