from bs4 import BeautifulSoup
import requests
#miner/futurehendrix


domain = "http://ohhla.com/"
fav_list_url = domain + "favorite.html"
soup = BeautifulSoup( requests.get(fav_list_url).text , "html.parser" )
artist_links = [domain + a["href"] for a in soup.select("a[href^=YFA_]")]
for 


