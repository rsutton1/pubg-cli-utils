# pubg-cli-utils
A CLI to the PUBG API

# Install
This project was tested on Ubuntu 14.04.

This project requires virtualenv, go
[here](https://virtualenv.pypa.io/en/stable/installation/) for
installation instructions.

Run the following commands to setup the environment:
```
git clone git@github.com:rsutton1/pubg-cli-utils.git
cd pubg-cli-utils
mkvirtualenv pubg
source pubg/bin/activate
pip install -r requirements.txt
```

Now we'll set your PUBG API key in the environment. You can get
this key [here](https://pubgtracker.com/site-api):
```
export PUBG_API_KEY=your-api-key-here
```

Now run the script:
```
python main.py player1 player2
```
