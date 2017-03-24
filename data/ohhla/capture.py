from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

import secrets

db = MongoClient('mongodb://%s:%s@ds139470.mlab.com:39470/hh' % (secrets.user, secrets.password)).hh

domain = "http://ohhla.com/"
fav_list_url = domain + "favorite.html"
soup = BeautifulSoup( requests.get(fav_list_url).text , "html.parser" )
artist_links = [a["href"] for a in soup.select("a[href^=YFA_]")]

for artist in artist_links[:]:
  artist_soup = BeautifulSoup( requests.get(domain + artist).text, "html.parser" )
  song_links = [a["href"] for a in artist_soup.select("a[href$=txt]")]

  for song in song_links[:]:
    song_content = requests.get(domain + song).text
    song_soup = BeautifulSoup(song_content, "html.parser")
    lyrics = song_soup.find("pre").text
    lyrics = lyrics[lyrics.index("\n\n"):]
    lyrics = [l.strip() for l in lyrics.split("\n") if l and not '[' in l]
    print(lyrics)



