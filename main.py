import requests
import json
import os
import argparse

# Parse the arguments to get players to compare
parser = argparse.ArgumentParser()
parser.add_argument("player1")
args = parser.parse_args()

# Request and print the player's info
url = "https://pubgtracker.com/api/profile/pc/%s" % (args.player1)
headers = {'TRN-Api-Key': os.environ["PUBG_API_KEY"]}
r = requests.get(url, headers=headers)
print(json.dumps(r.json(),indent=4))
