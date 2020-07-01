#! python3
# InterstellarMonitoringSystem v.0.0.1
# Discordbot for Elite Factions Updates
# made by SpoonLoeffel

# used Modules
import discord
import os
import sys
import time
import json
import pprint
import requests



# variables
token = None
version = '0.0.2'

settings = {
    'version': '0.0.2',                         # Version Number
    'databaseUpdated': None,                    # Timestamp of Database update
    'messagePosted': None,                      # Timestamp of last Message post
    'updateTime': 1700,                         # Default Update Time
    'autoUpdate': False,                        # En-/Disables Automatic Database download
    'dailyUpdate': False,                       # En-/Disables Automatic Message Posting
    'dbLocation': None,                         # Standard Location of Database
    'updateChannels': ['408061983917867024'],   # Standard Channles to post update into
    'factionId': 75448,                         # Standard Faction ID
    'owner': '167343578857603072',              # It's Myself
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
    fileObj = open(os.path.join(tokenLocationk, 'discordToken'), 'r')
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


