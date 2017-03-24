from pymongo import MongoClient

import secrets

db = MongoClient('mongodb://%s:%s@ds139470.mlab.com:39470/hh' % (secrets.user, secrets.password)).hh
lyric_collection = db.lyric_collection


for song in lyric_collection.find():
  print(song)

