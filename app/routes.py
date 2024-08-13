from flask import Blueprint, request, redirect, jsonify
from .auth import get_authorization_url, get_access_token
from .spotify import (
    search_for_artist,
    get_songs_by_artist,
    get_user_top_artists,
    get_user_profile
)
from .utils import remove_images

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return redirect(get_authorization_url())

@bp.route('/callback')
def callback():
    code = request.args.get('code')
    token = get_access_token(code)
    return redirect(f'/all?token={token}')

@bp.route('/search')
def search():
    token = request.args.get('token')
    artist_name = 'Mobb Deep'
    artist_data = search_for_artist(token, artist_name)
    if not artist_data['artists']['items']:
        return jsonify({'error': 'Artist not found'}), 404
    return jsonify(artist_data)

@bp.route('/profile')
def profile():
    token = request.args.get('token')
    user_profile = get_user_profile(token)
    return jsonify(user_profile)

@bp.route('/top-artists')
def top_artists():
    token = request.args.get('token')
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
        if not artist_data['artists']['items']:
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

