from requests import post, get
from dotenv import load_dotenv
import os
import base64
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = { "grant_type": "client_credentials" }
    result = post(url, headers=headers, data=data).content
    json_result = json.loads(result.decode("utf-8"))
    token = json_result["access_token"]
    return token


def get_auth_header(token):

    return {"authorization": "Bearer " + token, "Content-Type": "application/json"}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search" 
    headers = get_auth_header(token)
    query= f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query 
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content.decode("utf-8"))["artists"]["items"]
    if len(json_result) == 0:
        print("No artistis with this names exists...")
        return None
    
    return json_result[0]


def get_songs_by_artist(token, artists_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content.decode("utf-8"))["tracks"] 
    return json_result

def get_top_50_global(token):
    url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF/tracks"  # URL da playlist "Top 50 Global"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content.decode("utf-8"))
    tracks = json_result['items']
    for track in tracks:
        print(f"Name: {track['track']['name']}, Popularity: {track['track']['popularity']}")



token = get_token()
result = search_for_artist(token, "The Beatles")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
get_top_50_global(token)

# for idx, song in enumerate(songs):
#     print(f"{idx + 1}. {song['name']}")



