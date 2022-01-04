import nextcord
import os
import requests
import json
import random
import string
import logging
from replit import db
from keep_alive import keep_alive
from quinnDB import *
from firstTimeReplDBLoad import onStart

# Set Logging Config
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)

client = nextcord.Client()
onStart()
logging.info(f'Populated starting data into the database if keys don\'t exist')

## Functions Section
# Pulls a random quote from zenquotes.com using their API
def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return (quote)


# Defining logic paths for logging into servers
@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client))

# Defining logic paths for message events
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Massage content by making msg iterable in all lower case. Special use case for removing punctuation for greetings
    msg = message.content.lower()
    if ' ' not in (msg):
        logging.debug(f'String Input: {message.content}')
        first_word_message = msg.translate(
            str.maketrans('', '', string.punctuation))
        logging.debug(f'first_word_message: {first_word_message}')
        first_word = first_word_message
    else:
        first_word_message = msg.split(' ', 1)
        first_word = first_word_message[0]

    # Check to see if I should say hi friend
    logging.debug(f'This is my first_word: {first_word}')
    if first_word in (tuple(greetings)):
        await message.channel.send('Hi friend!')

    # Checks to see if I should be helpful or not
    if msg.startswith('!help'):
      response = f'''Woof! My name is Quinn! I am a friendly and welcoming Beagle! Here are my list of commands!
```!inspire - Need an inspiration quote? I can get you a random one from ZenQuotes.com!
!new [TEXT] - If you have an idea for me to encourage someone should they feel down or sad, you can add a new statement to my memory that I will pull out from time to time if someone needs it! Replace [TEXT] with whatever you'd like me to say!
!del [int] - Do we need to delete a phrase from my encouragement statements list? pass this command with the index number and I can delete that for you!
!query encouragements - I can dump my encouragement statements by passing this command!
$responding [true/false] - Turn on or off my friendly encouraging nature by setting true or false. Pass it without a parameter and I'll let you know if i'll encourage people or not!```
I also sometimes respond to various keywords in certain situations. I am sure you'll figure out what makes me happy as you get to know me better!
If you have any questions, my owner can help out! I am, after all, just a loving beagle! Woof!'''
      await message.channel.send(response)

    # Check to see if I should pull out an inspiring quote
    if message.content.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)
        logging.debug(f'Sent the following quote: {quote}')

    # Checks to see if I should send a word of encouragement
    # Also contains functionality to add/delete encouraging words submitted by users
    if db["responding"]:
      options = starter_encouragements
      if 'encouragements' in db.keys():
        options = options + list(db['encouragements'])
      if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))
        logging.debug('Sent a word of encouragement to my friend!')
    

    # Database Interactions
    if msg.startswith('!keys'):
      keyList = getKeys()
      await message.channel.send(keyList)

    # Logic to pull contents from db[] based off of key
    if msg.startswith('!query'):
      key = msg.split('!query ',1)[1]
      logging.debug(f'User submitted Key: {key}')
      try:
        results = getKeyValues(key)
        await message.channel.send(results)
      except KeyError as e:
        await message.channel.send(f'{KeyError}: The key {e} does not exist!')


    # Logic to add / delete encouragement statements from the database
    if msg.startswith('!new'):
      encouraging_message = msg.split('!new ',1)[1]
      logging.debug(f'User submitted encouraging_message: {encouraging_message}')
      appendKeyValue('encouragements',encouraging_message)
      await message.channel.send(f'New encouraging message added!: {encouraging_message}')
    if msg.startswith('!del'):
      encouragements = []
      if 'encouragements' in db.keys():
        index = int(msg.split('!del',1)[1])
        logging.debug(f'index variable: {str(index)}')
        deleteKeyValue('encouragements',index)
        encouragements = list(db['encouragements'])
      await message.channel.send(encouragements)


    # Check to see if I should be wagging my tail
    if any(word in msg for word in happy_words):
        await message.channel.send('*Wags tail*')
        logging.debug('I am happily wagging my tail.')
    
    # option to update responding key or retrieve the current value
    if msg.startswith("$responding"):
      if int(len(msg)) > 11:
        value = msg.split("$responding ",1)[1]
        if value == "true":
          setKeyValue('responding','True')
          await message.channel.send("Responding is on.")
        elif value == 'false':
          setKeyValue('responding','False')
          await message.channel.send("Responding is off.")
        else:
          await message.channel.send("I don't understand this command. Please provide a true or false value so I can update this configuration properly.")
      else:
        key = msg.split('$',1)[1]
        response = db[key]
        await message.channel.send(f'Responding Config: {str(response)}')


# Main Client code
keep_alive()
client.run(os.getenv('TOKEN'))