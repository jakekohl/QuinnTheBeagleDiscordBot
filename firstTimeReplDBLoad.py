import logging
from replit import db
import quinnDB


# This file contains values that default get propagated into Quinn's repl database if the key does not already exist. If it does exist, it will skip inserting these values. 

# Set Logging Config
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)


# Initial Triggers List
greetings = ['hello', 'hey', 'yo', 'howdy', 'greetings', 'hi', 'heyo','quinn']
sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable']
happy_words = ['treat', 'walk', 'let\'s go', 'good girl']

# Initial Responses
encouragements = ['Cheer up!', 'Hang in there.', 'You are a great person / bot!']
loves = ['I love my Dad!', 'I love curling up next to my mom!','I love chewing on bones!','I love chasing after squirrels, birds, and most importantly, Bunnies!']

# Function for populating above starting data

def populateKeys(key,value):
  if key not in quinnDB.getKeys():
    db[key] = list(value)
    logging.info(f'Inserting {key} into database with value(s): {value}')
    return

#
def onStart():
  populateKeys('greetings',greetings)
  populateKeys('encouragements',encouragements)
  populateKeys('loves',loves)
  populateKeys('sad_words',sad_words)
  populateKeys('happy_words',happy_words)
