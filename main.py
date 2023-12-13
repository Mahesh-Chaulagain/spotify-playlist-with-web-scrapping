import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN = os.getenv("TOKEN")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? type the date in YYYY-MM_DD format:")

# set URl
URL = f"https://www.billboard.com/charts/hot-100/{date}"

# get response
response = requests.get(URL)
website_html = response.text

# scrap the site
soup = BeautifulSoup(website_html, "html.parser")
# print(soup.prettify())

# select the element to get the song title using selector
songs = soup.select("li ul li h3")
song_name = [song.getText().strip() for song in songs]
# print(song_name)

song_uris = []
year = date.split("-")[0]
for song in song_name:
    # search spotify track
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doessn't exist in spotify so skipped")

# create playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

# add tracks to playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)



