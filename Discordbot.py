#! python3
# InterstellarMonitoringSystem v.0.0.1
# Discordbot for Elite Factions Updates
# made by SpoonLoeffel


#### Modules ####

# used Modules
import os
import sys
import time
import datetime
import pprint

# for the Database
import requests
import json

# for Discord integration
import discord      # discord module
from discord.ext import commands, tasks
import asyncio
import logging      # dependency for discord


# Logger
logger = logging.getLogger('discord')
logger.setLevel(logging.FATAL)
handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')         # TODO Cleanup
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


#### variables ####
token = None
version = '0.1.2'

settings = {
    'version': '0.1.2',                                 # Version Number
    'databaseUpdated': None,                            # Timestamp of Database update
    'messagePosted': None,                              # Timestamp of last Message post
    'updateTime': None,                                 # TODO add Default Update Time
    'autoDBUpdate': False,                              # En-/Disables Automatic Database download
    'dailyUpdate': False,                               # En-/Disables Automatic Message Posting
    'dbLocation': os.getcwd(),                          # Standard Location of Database
    'updateChannels': [408061983917867024],             # Standard Channles to post update into
    'factionId': 75448,                                 # Standard Faction ID
    'owner': 167343578857603072,                        # It's Myself
    'adminUsers': [],                                   # User with Admin rights
    'tokenLocation': None,                              # Default location of Tokenfile
    }
cacheSystems = {'refreshTime': None, 'Systems': []}



impressum = '''Interstellar Monitoring System version: %s
Made by SpoonLoeffel

Source code at:
https://github.com/SpoonLoeffel/InterstellarMonitoringSystem''' % (version)
                


#### Functions ####

## Save File Handling ##
# Create new Settings file
def createSettingsFile():
    # TODO Add Error Checking
    fileObj = open('DiscordBotSettings.py', 'w')
    fileObj.write('import datetime\n\nsettings = ' + pprint.pformat(settings) + '\n')
    fileObj.close()

# Load Settings file
def loadSettingsFile():
    # TODO Add Error Checking
    import DiscordBotSettings
    settings = DiscordBotSettings.settings
    return settings


## Token Handling ##
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
    
## Deal with DB ##
# Download the DB
def downloadDB():
    print('downloadDB()')
    global settings
    tries = 0
    # Download attempts
    while tries < 5:
        res = requests.get('https://eddb.io/archive/v6/systems_populated.json') # Download the json
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
        break                                                                   # cleanup loop
    
    # Save SystemPopulation to file
    dbFile = open(os.path.join(settings['dbLocation'], 'systems_populated.json'), 'w')
    dbFile.write(res.text)
    dbFile.close()
    # TODO Add Error Checking
    settings['databaseUpdated'] = datetime.datetime.now()                   # Add Time when Database was updated
    createSettingsFile()
    refreshFactions()

# refresh loaded Factions
def refreshFactions():
    print('refreshFactions()')
    global cacheSystems
    
    dbFile = open(os.path.join(settings['dbLocation'], 'systems_populated.json'), 'r')  # Open the DB file
    # TODO Add Error Checking
    stringOfJsonData = dbFile.read()                                                    # read DB content to string
    dbFile.close()                                                                      # close the file
    jsonData = json.loads(stringOfJsonData)                                             # convert Json to Python data
    cacheSystems = {'refreshTime': datetime.datetime.now(), 'Systems': []}              # clear casheSystems
    for i in jsonData:                                                                  # Iterate over all Star Systems
        for k in i['minor_faction_presences']:                                          # Iterate over 
            if k['minor_faction_id'] == settings['factionId']:                          # Is the desired faction in that system
                cacheSystems['Systems'] = cacheSystems['Systems'] + [i]                 # add found system into cacheSystems

# check if DB should be updated
def checkDBUpdate():
    dtnow = datetime.datetime.now()
    updateDelta = datetime.timedelta(hours=12)
    if os.path.isfile(os.path.join(settings['dbLocation'], 'systems_populated.json')) == True:
        if settings['autoDBUpdate'] == True:
            if settings['databaseUpdated'] < dtnow - updateDelta:
                downloadDB()
            elif settings['databaseUpdated'] == None:
                downloadDB()
            else:
                refreshFactions()
    else:
        downloadDB()
    if cacheSystems['refreshTime'] == None:
        refreshFactions()
    
## Messages ##
def readySystem(systemInfo, factionId):
    print(f'readySystem({systemInfo}, {factionId})')
    factionListPosition = 0
    for i in range(len(systemInfo['minor_faction_presences'])):
        if systemInfo['minor_faction_presences'][i]['minor_faction_id'] == factionId:
            factionListPosition = i
            break
	    
    messageVariables = [
        systemInfo['name'],
        systemInfo['primary_economy'],
        systemInfo['security'],
        systemInfo['controlling_minor_faction'],
        ]
    if len(systemInfo['states']) == 0:
        messageVariables += ['None']
    else:
        states = ''
        for i in systemInfo['states']:
            states = states + ' & ' + i['name']
        messageVariables += [states[3:]]
    messageVariables += [
        str(systemInfo['minor_faction_presences'][factionListPosition]['happiness_id']),
        str(systemInfo['minor_faction_presences'][factionListPosition]['influence']),
        ]

    # Recovering States
    if len(systemInfo['minor_faction_presences'][factionListPosition]['recovering_states']) == 0:
        messageVariables += ['None']
    else:
        states = ''
        for i in systemInfo['minor_faction_presences'][factionListPosition]['recovering_states']:
            states = states + ' & ' + i['name']
        messageVariables += [states[3:]]

    # Active States
    if len(systemInfo['minor_faction_presences'][factionListPosition]['active_states']) == 0:
        messageVariables += ['None']
    else:
        states = ''
        for i in systemInfo['minor_faction_presences'][factionListPosition]['active_states']:
            states = states + ' & ' + i['name']
        messageVariables += [states[3:]]

    # Pending States
    if len(systemInfo['minor_faction_presences'][factionListPosition]['pending_states']) == 0:
        messageVariables += ['None']
    else:
        states = ''
        for i in systemInfo['minor_faction_presences'][factionListPosition]['pending_states']:
            states = states + ' & ' + i['name']
        messageVariables += [states[3:]]

    # System Info Updated
    dt = datetime.datetime.fromtimestamp(systemInfo['updated_at'])
    messageVariables += [dt.strftime('%Y/%m/%d %H:%M:%S')]

    print(messageVariables)
#     message='''System: **%s**
# Economy: %s; Security: %s; Controlling Faction: %s
# System States: %s
# Happiness: %s; Influence: %s
# Recovering States: %s; Current States: %s; Pending States: %s
# Info updated at: %s''' % tuple(messageVariables)
    message='''System: **%s**
-------------------------------
Economy:             %s
Security:            %s
Controlling Faction: %s
System States:       %s
Happiness:           %s
Infulence:           %s
Recovering States:   %s
Current States:      %s
Pending States:      %s
-------------------------------
Info updated at: %s''' % tuple(messageVariables)
    return message

# Ready the Message
def readyFactionMessage(factionId):
    # Check DB here
    print('readyFactionMessage()')
    checkDBUpdate()

    # Prepare the Message
    messageVariables = [
        'The Hellssina Knights',                                # TODO Make this variable
        datetime.datetime.now().strftime('%Y/%m/%d'),           # Current Time
        ]
    
    # Controlled Systems
    controlledSystems = ''
    for i in cacheSystems['Systems']:                                       # Loop through cachedSystems
        if i['controlling_minor_faction_id'] == factionId:                  # Compare ID of Faction with the one Controlling the System
            controlledSystems += i['name'] + '; '                           # Add System to list of controlled Systems
    if len(controlledSystems) > 0:                                          # See if Faction controls atleast one System
        messageVariables += [controlledSystems[:-1]]                        # Remove trailing Space and add controlledSystems to the messageVariables
    else:
        messageVariables += ['Faction does not controle any Systems']

    # Systems requireing Attention
    # TODO add this
    messageVariables += ['Function not yet implimented']
    
    message = '''Faction overview for: %s on %s
Controlled Systems:
%s
Systems Requireing Attention:
%s''' % tuple(messageVariables)
    return message



#### Main Program ####
# Startup
# Load settings
if os.path.isfile('DiscordBotSettings.py') == True:
    settings = loadSettingsFile()
else:
    createSettingsFile()

# Get the Token
tokenLocation = settings['tokenLocation']
if tokenLocation == None:
    tokenLocation = ''
if os.path.isfile(os.path.join(tokenLocation, 'discordToken')) != True:         # no token File exists
    createTokenFile(tokenLocation)                                              # create template
    print('No token Found\nDouble Check the file location\n' + tokenLocation)   # notify user if no token found
    sys.exit()                                                                  # exit program
else:
    token = loadTokenFile(tokenLocation)

# Discord integration

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Background task loop
async def my_background_task():
    await client.wait_until_ready()
    print('background task')
    while not client.is_closed:
        await asyncio.sleep(6)
            
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ping'):
        print('channel: ' + str(message.channel))
        await message.channel.send('pong!')

    if message.content.startswith('!impressum'):
        await message.channel.send(impressum)

    if message.content.startswith('!updateDB'):
        if message.author.id in [settings['owner']] + settings['adminUsers']:
            await message.channel.send('Updateing Database')
            downloadDB()
            await message.channel.send('Database updated')

    if message.content.startswith('!refreshSystems'):
        print('refresh cached Systems')
        refreshFactions()
        await message.channel.send('cache refresh complete')
        print('refresh complete')
        print(cacheSystems)
        await message.channel.send('done')
            

    if message.content.startswith('!factionInfo'):
        refreshFactions()
        await message.channel.send(readyFactionMessage(settings['factionId']))

    if message.content.startswith('!detailedFactionInfo'):
        if message.author.id in [settings['owner']] + settings['adminUsers']:
            await message.channel.send(readyFactionMessage(settings['factionId']))
            for i in range(len(cacheSystems['Systems'])):
                await message.channel.send(readySystem(cacheSystems['Systems'][i], settings['factionId']))
                
    if message.content.startswith('!ShootMeInTheHead'):
        if message.author.id in [settings['owner']] + settings['adminUsers']:
            await message.channel.send('Goodbye!')
            sys.exit()

# Daily Update Message
@tasks.loop(hours=24)
async def called_once_a_day():
    print(settings['dailyUpdate'])
    if settings['dailyUpdate'] == True:
        dtnow = datetime.datetime.now()
        updateDelta = datetime.timedelta(hours=12)
        if (settings['messagePosted'] < dtnow - updateDelta) or (settings['messagePosted'] == None):
            for i in settings['updateChannels']:
                print(i)
                channel = client.get_channel(i)
                await channel.send(readyFactionMessage(settings['factionId']))
                for k in range(len(cacheSystems['Systems'])):
                    await channel.send(readySystem(cacheSystems['Systems'][k], settings['factionId']))
            
            settings['messagePosted'] = datetime.datetime.now()
            createSettingsFile()
            refreshFactions()

@called_once_a_day.before_loop
async def before():
    await client.wait_until_ready()
    print('finished waiting')

called_once_a_day.start()
#client.loop.create_task(my_background_task())
client.run(token)
