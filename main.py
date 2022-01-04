import nextcord
import os
import requests
import json
import random
import string
import logging
from replit import db
from keep_alive import keep_alive

# Set Logging Config
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)

# Much of this code so far comes from the Discord Bot tutorial @ https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

client = nextcord.Client()

## Lists sections

# Instantiate lists for triggers
greetings = ['hello', 'hey', 'yo', 'howdy', 'greetings', 'hi', 'heyo','quinn']
sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable']
happy_words = ['treat', 'walk', 'let\'s go', 'good girl']

# Lists of responses
starter_encouragements = ['Cheer up!', 'Hang in there.', 'You are a great person / bot!']
loves = ['I love my Dad!', 'I love curling up next to my mom!','I love chewing on bones!','I love chasing after squirrels, birds, and most importantly, Bunnies!']

## Configuration
if "responding" not in db.keys():
  db["responding"] = True


## Functions Section

# Pulls a random quote from zenquotes.com using their API
def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return (quote)

# update encouragements from the database
def update_encouragements(encouraging_message):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [encouraging_message]

# delete encouragements from the database
def delete_encouragment(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
  db['encouragements'] = encouragements

# Retrieve contents from db[] based on key in the list format
def retrieve_db_contents(table):
  key = table 
  contents = list(db[key])
  return contents

# TODO: implement retrieve_db_contents for other datatypes



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
    
    # Logic to add / delete encouragement statements from the database
    if msg.startswith('!new'):
      encouraging_message = msg.split('!new ',1)[1]
      logging.debug(f'User submitted encouraging_message: {encouraging_message}')
      update_encouragements(encouraging_message)
      await message.channel.send(f'New encouraging message added!: {encouraging_message}')
    if msg.startswith('!del'):
      encouragements = []
      if 'encouragements' in db.keys():
        index = int(msg.split('!del',1)[1])
        logging.debug(f'index variable: {str(index)}')
        delete_encouragment(index)
        encouragements = list(db['encouragements'])
      await message.channel.send(encouragements)

    # Logic to pull contents from db[] based off of key
    if msg.startswith('!query'):
      key = msg.split('!query ',1)[1]
      logging.debug(f'User submitted Key: {key}')
      try:
        results = retrieve_db_contents(key)
        await message.channel.send(results)
      except KeyError as e:
        await message.channel.send(f'{KeyError}: The key {e} does not exist!')

    # Check to see if I should be wagging my tail
    if any(word in msg for word in happy_words):
        await message.channel.send('*Wags tail*')
        logging.debug('I am happily wagging my tail.')
    
    # option to update responding key or retrieve the current value
    if msg.startswith("$responding"):
      if int(len(msg)) > 11:
        value = msg.split("$responding ",1)[1]
        if value == "true":
          db["responding"] = True
          await message.channel.send("Responding is on.")
        elif value == 'false':
          db["responding"] = False
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
