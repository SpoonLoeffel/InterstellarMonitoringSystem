#! python3
# InterstellarMonitoringSystem v.0.0.1
# Discordbot for Elite Factions Updates
# made by SpoonLoeffel

# used Modules
import os
import sys
import time
import pprint

# for the Database
import requests
import json

# for Discord integration
import discord      # discord module
import logging      # dependency for discord


# Logger
logger = logging.getLogger('discord')
logger.setLevel(logging.FATAL)
handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')         # TODO Cleanup
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


## variables ##
token = None
version = '0.0.3'

settings = {
    'version': '0.0.3',                         # Version Number
    'databaseUpdated': None,                    # Timestamp of Database update
    'messagePosted': None,                      # Timestamp of last Message post
    'updateTime': 1700,                         # Default Update Time
    'autoUpdate': False,                        # En-/Disables Automatic Database download
    'dailyUpdate': False,                       # En-/Disables Automatic Message Posting
    'dbLocation': None,                         # Standard Location of Database
    'updateChannels': [408061983917867024],     # Standard Channles to post update into
    'factionId': 75448,                         # Standard Faction ID
    'owner': 167343578857603072,                # It's Myself
    'adminUsers': [],                           # User with Admin rights
    'tokenLocation': None,                      # Default location of Tokenfile
    }


## Functions ##

# Create new Settings file
def createSettingsFile():
    # TODO Add Error Checking
    fileObj = open('DiscordBotSettings.py', 'w')
    fileObj.write('settings = ' + pprint.pformat(settings) + '\n')
    fileObj.close()

# Load Settings file
def loadSettingsFile():
    # TODO Add Error Checking
    import DiscordBotSettings
    settings = DiscordBotSettings.settings
    return settings

# Create new Token file
def createTokenFile(tokenLocation):
    # TODO Add Error Checking
    fileObj = open(os.path.join(tokenLocation, 'discordToken'), 'w')
    fileObj.write('<insert token here>')
    fileObj.close()

    
# Load Token file
def loadTokenFile(tokenLocation):
    fileObj = open(os.path.join(tokenLocation, 'discordToken'), 'r')
    token = fileObj.read()
    # TODO Add Error Checking
    return token
    fileObj.close()
    

# Download the DB
def downloadDB(dbLocation):
    tries = 0
    # Download attempts
    while tries < 5:
        res = requestss.get('https://eddb.io/archive/v6/systems_populated.json') # Download the json
        # Error Checking
        try:
            res.raise_for_status()
        except Exception as exc:
            if tries == 5:
                return
            else:
                tries += 1
                time.sleep(5)
                continue

    # Save SystemPopulation to file
    dbFile = open(os.path.join(dbLocation, 'systems_populated.json'), 'w')
    dbFile.write(res)
    dbFile.close()



## Main Program ##
# Startup
# Load settings
if os.path.isfile('DiscordBotSettings') == True:
    settings = loadSettingsFile()
else:
    createSettingsFile()

# Get the Token
tokenLocation = settings['tokenLocation']
if tokenLocation == None:
    tokenLocation = ''
if os.path.isfile(os.path.join(tokenLocation, 'discordToken')) != True:         # no token File exists
    createTokenFile(tokenLocation)                                              # create template
    print('No token Found\nDouble Check the file location\n' + tokenLocation)   # notify user
    sys.exit()                                                                  # 
else:
    token = loadTokenFile(tokenLocation)



# Discord integration

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ping'):
        await message.channel.send('pong!')

client.run(token)
