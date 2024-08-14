from flask import Blueprint, request, redirect, jsonify
from .auth import get_authorization_url, get_access_token
from .utils import remove_images
import requests
from .spotify import (
    search_for_artist,
    get_songs_by_artist,
    get_user_top_artists,
    get_user_profile
)

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return redirect(get_authorization_url())

@bp.route('/callback')
def callback():
    code = request.args.get('code')
    
    if not code:
        return jsonify({'error': 'No authorization code provided'}), 400

    token = get_access_token(code)
    
    if not token:
        return jsonify({'error': 'Failed to obtain access token'}), 500

    return redirect(f'/all?token={token}')

@bp.route('/search')
def search():
    token = request.args.get('token')
    
    if not token:
        return jsonify({'error': 'No access token provided'}), 400

    artist_name = 'Mobb Deep'
    artist_data = search_for_artist(token, artist_name)
    if not artist_data.get('artists', {}).get('items'):
        return jsonify({'error': 'Artist not found'}), 404
    
    return jsonify(artist_data)

@bp.route('/profile')
def profile():
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'No access token provided'}), 400

    user_profile = get_user_profile(token)
    return jsonify(user_profile)

@bp.route('/top-artists')
def top_artists():
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'No access token provided'}), 400

    user_top_artists = get_user_top_artists(token)
    return jsonify(user_top_artists)

@bp.route('/all')
def all_info():
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'No access token provided'}), 400
    
    artist_name = 'Mobb Deep'
    try:
        artist_data = search_for_artist(token, artist_name)
        
        if not artist_data.get('artists', {}).get('items'):
            return jsonify({'error': 'Artist not found'}), 404

        artist_id = artist_data['artists']['items'][0]['id']
        songs = get_songs_by_artist(token, artist_id)
        user_profile = get_user_profile(token)
        user_top_artists = get_user_top_artists(token)

        artist_data = remove_images(artist_data)
        songs = remove_images(songs)
        user_profile = remove_images(user_profile)
        user_top_artists = remove_images(user_top_artists)

        return jsonify({
            'artist': artist_name,
            'songs': songs.get('tracks', []),
            'user_profile': user_profile,
            'top_artists': user_top_artists
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/recommendations')
def recommendations():
    token = request.args.get('token')
    
    if not token:
        return jsonify({'error': 'No access token provided'}), 400
    
    try:
        user_top_tracks = get_user_top_tracks(token)
        seed_tracks = [track['id'] for track in user_top_tracks.get('items', [])]
        recs = get_recommendations(seed_tracks, token)
        
        return jsonify(recs)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_user_top_tracks(token):
    url = "https://api.spotify.com/v1/me/top/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {'error': 'Failed to fetch top tracks'}
    return response.json()

def get_recommendations(seed_tracks, token):
    if not seed_tracks:
        return {'error': 'No valid seed tracks provided'}, 400

    # Limit seed_tracks to a maximum of 5
    limited_seed_tracks = seed_tracks[:5]

    url = "https://api.spotify.com/v1/recommendations"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "seed_tracks": ','.join(limited_seed_tracks),
        "limit": 10
    }

    # TODO: REMOVE
    print(f"Request URL: {url}")
    print(f"Headers: {headers}")
    print(f"Parameters: {params}")

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return {'error': f'Failed to fetch recommendations: {response.text}'}, response.status_code

    return response.json()

def get_track_info(href, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(href, headers=headers)
    if response.status_code != 200:
        return {'error': f'Failed to fetch track info: {response.text}'}, response.status_code
    
    return response.json()

@bp.route('/track-info')
def track_info():
    token = request.args.get('token')
    href = request.args.get('href')  # Assuming you pass the href in the request

    if not token:
        return jsonify({'error': 'No access token provided'}), 400

    if not href:
        return jsonify({'error': 'No href URL provided'}), 400
    
    track_info = get_track_info(href, token)
    return jsonify(track_info)
