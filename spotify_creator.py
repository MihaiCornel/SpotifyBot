from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

USER = input("Enter the date(YYYY-MM-DD) that you want to travel: ")
Client_ID = os.environ.get("spotify_id")
Client_Secret = os.environ.get("spotify_pass")
URL = f"https://www.billboard.com/charts/hot-100/{USER}/"

response = requests.get(URL)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

songs_names_h3 = soup.select(".o-chart-results-list__item h3")
song_names = [song.getText().strip() for song in songs_names_h3]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )

)
user_id = sp.current_user()["id"]

song_uris = []
year = USER.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")



playlist = sp.user_playlist_create(user=user_id, name=f"{USER} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
