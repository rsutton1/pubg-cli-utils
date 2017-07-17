import requests
import json
import os
import sys
import argparse

# get_player_json
#
# Returns the raw json of the player's stats from the API
def get_player_json(player):
    url = "https://pubgtracker.com/api/profile/pc/%s" % (player)
    headers = {'TRN-Api-Key': os.environ["PUBG_API_KEY"]}
    r = requests.get(url, headers=headers)

    # The server returns a 500 if the player isn't found, so if we
    # see a 500 this is the most likely problem.
    if r.status_code != 200:
        print("Player %s not found. Please enter a valid player." % (player))
        sys.exit(1)
    return r.json()

# parse_player_stats
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
def parse_player_stats(player_stats_raw):
    player_stats = {}
    for stat in player_stats_raw:
        stat_name = stat["field"]
        stat_value = stat["value"]
        player_stats[stat_name] = stat_value
    return player_stats

# get_player_stats
#
# This gets the dictionary of a player's stats given the match_type and
# region.
#
# inputs:
#   player_json: the json stats for the player
#   match_type: the type of match
#   region: the region for the stats
#
# output:
#   A dictionary of the player's stats
def get_player_stats(player_json, match_type, region):
    for stats_meta in player_json["Stats"]:
        if stats_meta["Match"] == match_type and stats_meta["Region"] == region:
            player_stats_raw = stats_meta["Stats"]
            return parse_player_stats(player_stats_raw)

# Pretty prints the result into columns and rows while filtering
# out unwanted stats
def pretty_print_stats(all_players, stats):
    print("Player\t", end='')
    for stat in stats:
        print("%20s\t" % (stat), end='')
    print("")
    for player, player_stats in all_players.items():
        print("%s\t" % player, end='')
        for stat in stats:
            print("%20s\t" % player_stats[stat], end='')
        print("")

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
    all_stats[player] = get_player_stats(player_json, match_type, region)

pretty_print_stats(all_stats, stats)
