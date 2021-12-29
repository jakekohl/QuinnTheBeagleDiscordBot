import discord
import os
import requests
import json
import random
import string
import logging
from replit import db

# Set Logging Config
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

# Code so far comes from the Discord Bot tutorial @ https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

client = discord.Client()
greetings = ['hello','hey','yo','howdy','greetings','hi','heyo']
sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable']
starter_encouragements = ['Cheer up!','Hang in there.','You are a great person / bot!']
happy_words = ['treat','walk','let\'s go','good girl']

# Pulls a random quote from zenquotes.com using their API
def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return(quote)


# Main code runs here
@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Massage content by making msg iterable in all lower case. Special use case for removing punctuation for greetings 
    msg = message.content.lower()
    if ' ' not in (msg):
      logging.debug('String Input: ' + message.content)
      first_word_message = msg.translate(str.maketrans('', '', string.punctuation))
      logging.debug('first_word_message: ' + first_word_message)
      first_word = first_word_message
    else:
      first_word_message = msg.split(' ',1)
      first_word = first_word_message[0]

    # Check to see if I should say hi friend
    logging.debug('This is my first_word: '+first_word)
    if first_word in (tuple(greetings)):
        await message.channel.send('Hi friend!')

    # Check to see if I should pull out an inspiring quote
    if message.content.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)
        logging.debug("Sent the following quote: "+quote)

    # Checks to see if I should send a word of encouragement
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))   
      logging.debug('Sent a word of encouragement to my friend!') 

    # Check to see if I should be wagging my tail
    if any(word in msg for word in happy_words):
      await message.channel.send('*Wags tail*')
      logging.debug('I am happily wagging my tail.')

client.run(os.getenv('TOKEN'))