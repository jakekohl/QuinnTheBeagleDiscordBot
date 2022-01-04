import string
import list
from repl import db
import database


# This file contains values that default get propagated into Quinn's repl database if the key does not already exist. If it does exist, it will skip inserting these values. 



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