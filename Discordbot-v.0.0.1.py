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

# variables
token = None

settings = {
    'version': '0.0.1',                         # Version Number
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
    fileObj = open('DiscordBotSettings.py', 'w')
    fileObj.write('settings = ' + pprint.pformat(settings) + '\n')
    fileObj.close()

# Load Settings file
def loadSettingsFile():
    import DiscordBotSettings
    settings = DiscordBotSettings.settings
    return settings

# Create new Token file
def createTokenFile(tokenLocation):
    fileObj = open(os.path.join(tokenLocation, 'discordToken.py'), 'w')
    fileObj.write('token = ' + '<insert token here>')
    fileObj.close()

    
# Load Token file
def loadTokenFile(tokenLocation):
    


