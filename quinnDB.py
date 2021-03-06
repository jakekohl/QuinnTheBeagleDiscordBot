from replit import db
import logging

# Outputs a list of keys
def getKeys():
  keys = db.keys()
  return keys

# delete a key and its contents
def deleteKey(key):
  del db[key]

# get a specific key value/s
def getKeyValues(key):
  values = list(db[key])
  return values 

# set new key and value 
def setKeyValue(key,value):
  db[key] = value
  logging.info(f'Added {value} into db.{key}')
  return

# Append new key value 
def appendKeyValue(key,value):
  if key in db.keys():
    keyList = list(db[key])
    logging.info(f'keyList is: {keyList}')
    keyList.append(value)
    db[key] = keyList
  else:
    db[key] = value

# delete value from a key from the database
def deleteKeyValue(key,index):
  keyValues = list(db[key])
  if len(keyValues) > index:
    del keyValues[index]
  db[key] = keyValues
