import nextcord
import os
import requests
import json
import random
import string
import logging

from replit import db

import quinnDB
from keep_alive import keep_alive
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

    # Database Interactions
    # Gets list of keys
    if msg.startswith('!keys'):
      keyList = quinnDB.getKeys()
      logging.info(f'keyList value is: {keyList}')
      await message.channel.send(keyList)

    # Get values from a key
    if msg.startswith('!query'):
      key = msg.split('!query ',1)[1]
      logging.debug(f'User submitted Key: {key}')
      try:
        results = quinnDB.getKeyValues(key)
        await message.channel.send(results)
      except KeyError as e:
        await message.channel.send(f'{KeyError}: The key {e} does not exist!')
        return

    # Delete a specific key from the database
    if msg.startswith('!drop'):
      try:
        key = msg.split(' ',1)[1]
      except IndexError:
        await message.channel.send(f'{IndexError}: Please provide an key to drop!')
        return
      quinnDB.deleteKey(key)
      await message.channel.send(f'Key {key} has been dropped!')

    # Logic to add / delete statements from the database
    if msg.startswith('!new'):
      messageNoKey = msg.split('!new ',1)[1]
      key = messageNoKey.split(' ',1)[0]
      value = messageNoKey.split(' ',1)[1]
      if key not in quinnDB.getKeys():
        await message.channel.send(f'The key {key} doesn\'t exist.')
      else:
        quinnDB.appendKeyValue(key,value)
        await message.channel.send(f'New value in {key} added!: {value}')
    if msg.startswith('!del'):
      key = msg.split(' ',2)[1]
      try:
        index = int(msg.split(' ',2)[2])
        logging.debug(f'index variable: {str(index)}')
      except IndexError:
        await message.channel.send(f'{IndexError}: Please provide an index to represent the phrase to delete!')
      quinnDB.deleteKeyValue('encouragements',index)
      await message.channel.send(f'Item at Index[{index}] has been removed!')




    # Friendly Response Section

    # Check to see if I should say hi friend
    logging.debug(f'This is my first_word: {first_word}')
    if first_word in quinnDB.getKeyValues('greetings'):
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
      if any(word in msg for word in quinnDB.getKeyValues('sad_words')):
        await message.channel.send(random.choice(quinnDB.getKeyValues('encouragements')))
        logging.debug('Sent a word of encouragement to my friend!')
    else:
      logging.debug(f'$responding is turned off')

    # Check to see if I should be wagging my tail
    if any(word in msg for word in quinnDB.getKeyValues('happy_words')):
        await message.channel.send('*Wags tail*')
        logging.debug('I am happily wagging my tail.')
    
    # option to update responding key or retrieve the current value
    if msg.startswith("$responding"):
      if int(len(msg)) > 11:
        value = msg.split("$responding ",1)[1]
        if value == "true":
          quinnDB.setKeyValue('responding','True')
          await message.channel.send("Responding is on.")
        elif value == 'false':
          quinnDB.setKeyValue('responding','False')
          await message.channel.send("Responding is off.")
        else:
          await message.channel.send("I don't understand this command. Please provide a true or false value so I can update this configuration properly.")
      else:
        key = msg.split('$',1)[1]
        response = quinnDB.getKeyValues(key)
        await message.channel.send(f'Responding Config: {str(response)}')


# Main Client code
keep_alive()
client.run(os.getenv('TOKEN'))