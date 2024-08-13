import requests
from .config import Config

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    response = requests.get(url + query, headers=headers)
    return response.json()

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)
    return response.json()

def get_user_top_artists(token):
    url = "https://api.spotify.com/v1/me/top/artists"
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)
    return response.json()

def get_user_profile(token):
    url = "https://api.spotify.com/v1/me"
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)
    return response.json()

