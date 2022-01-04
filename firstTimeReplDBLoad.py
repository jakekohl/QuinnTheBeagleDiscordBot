import string
from replit import db
from quinnDB import *
import logging


# This file contains values that default get propagated into Quinn's repl database if the key does not already exist. If it does exist, it will skip inserting these values. 



# Initial Triggers List
greetings = ['hello', 'hey', 'yo', 'howdy', 'greetings', 'hi', 'heyo','quinn']
sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable']
happy_words = ['treat', 'walk', 'let\'s go', 'good girl']

# Initial Responses
encouragements = ['Cheer up!', 'Hang in there.', 'You are a great person / bot!']
loves = ['I love my Dad!', 'I love curling up next to my mom!','I love chewing on bones!','I love chasing after squirrels, birds, and most importantly, Bunnies!']

# Function for populating above starting data

def populateKeys(key,value):
  if key not in getKeys():
    db[key] = value
    return logging.info(f'Inserting {key} into database with value(s): {value}')

#
def onStart():
  populateKeys('greetings',greetings)
  populateKeys('encouragements',encouragements)
  populateKeys('loves',loves)
  populateKeys('sad_words',sad_words)
  populateKeys('happy_words',happy_words)
