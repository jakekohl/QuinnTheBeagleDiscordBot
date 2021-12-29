import discord
import os
import requests
import json
import random
from replit import db

# Code so far comes from the Discord Bot tutorial @ https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

client = discord.Client()
greetings = ['hello','hey','yo','howdy','greetings']
sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable']
starter_encouragements = ['Cheer up!','Hang in there.','You are a great person / bot!']

# Pulls a random quote from zenquotes.com using their API
def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return(quote)


# Main code runs here
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    first_word_message = msg.split(' ',1)
    first_word = first_word_message[0].lower()
    if first_word in (tuple(greetings)):
        await message.channel.send('Hi friend!')

    if message.content.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))    

client.run(os.getenv('TOKEN'))