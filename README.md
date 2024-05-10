# Twitch Translation Bot

This script is a rough proof of concept for a twitter bot that listens to all
messages in a Twitch channel, identifies the language of each message, and 
translates the message to the desired target language if it's not already in
that language.  It's just a couple of hugging face models slapped together but
it's fun.

Please note that this is not super useful and makes plenty of mistakes, feel
free to make PRs or open issues.

## Table of Contents

- [Installation](#installation)
- [ToDo](#ToDo)

## Installation

I'm currently using this with python 3.10.  Or build and use the Dockerfule
```sh
# work from a virtualenv
virtualenv ~/.envs/twitch-translation-bot
source ~/.envs/twitch-translation-bot/bin/activate

# install requirements
pip install -r app/requirements.txt

# Run this script (First time will take time and bandwidth to download models)
python app/prep.py

# Get your Twitch access token and configure your .env file

# Start the bot:
python app/app.py --dotenv

```

## ToDo

- Catch exceptions
- Modularize
- Add web interface (pywebio)

## Shortcomings
- I've only spent a few hours on it
- It makes lots of mistakes
