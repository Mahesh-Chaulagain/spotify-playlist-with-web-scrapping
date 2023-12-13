from bs4 import BeautifulSoup
import requests

date = input("Which year do you want tot travel to? type the date in YYYY-MM_DD format:")

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
print(song_name)




