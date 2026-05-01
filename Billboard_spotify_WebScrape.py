from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#scrapping billboard 100
date=input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
header={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"}
billboard_url="https://appbrewery.github.io/bakeboard-hot-100/"+ date
response=requests.get(url=billboard_url,headers=header)
soup= BeautifulSoup(response.text, 'html.parser')
song=soup.find_all("h3",class_="chart-entry__title")
song_names = [song.getText().strip() for song in song]
print(song_names)
#authenticating spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id="my_client_id",
        client_secret="my_client_secret",
        show_dialog=True,
        cache_path="token.txt",
        username="my_username",
    )
)
user_id = sp.current_user()["id"]

#searching spotify for songs

song_uris=[]
year=date.split("-")[0]
for song in song_names:
    result=sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri=result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# creating playlist in spotify

playlist =sp.current_user_playlist_create(name=f"{date} Billboard 100", public=False)
print(playlist)

#adding songs into playlist
sp.playlist_add_items(playlist["id"], items=song_uris)
