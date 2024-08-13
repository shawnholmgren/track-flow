# Track Flow

A Flask-based Python application that interacts with the Spotify API to search for artists, retrieve their top tracks, and access user profile and top artists information. This application uses Spotify's OAuth2 authorization to obtain an access token and make requests for artist and user data.

## Features

- **Authenticate with Spotify API**: Implements OAuth2 authorization to obtain an access token.
- **Search for Artists**: Searches for an artist by name and retrieves information.
- **Retrieve Artist's Top Tracks**: Fetches the top tracks of a specific artist.
- **Get User Profile**: Retrieves information about the authenticated user.
- **Get User's Top Artists**: Fetches the top artists of the authenticated user.

## Prerequisites

- Python 3.x
- `Flask` library
- `requests` library
- `python-dotenv` library

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/shawnholmgren/track-flow.git
   cd track-flow
   ```
2. **Create and Activate a Virtual Environment**
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate 
3. **Install Dependencies**
   
   ```bash
   pip3 install -r requirements.txt
4. **Set Up Environment Variables**
   
   Create a .env file in the root of the project directory.
   ```env
   CLIENT_ID=your_spotify_client_id
   CLIENT_SECRET=your_spotify_client_secret
   REDIRECT_URI=your_redirect_uri
   ```
   Replace `your_spotify_client_id` and `your_spotify_client_secret` with your actual Spotify API credentials.
5. **Set Up Environment Variables**
    ```bash
    python run.py
    ```
    Navigate to http://localhost:8888 in your browser to start the authorization process.
## Routes
- `/`: Redirects to Spotify for authorization.
- `/callback`: Handles the authorization callback and retrieves the access token.
- `/all`: Retrieves and displays artist information, user profile, and top artists.
- `/search`: Searches for a specific artist.
- `/profile`: Retrieves the authenticated user's profile.
- `/top-artists`: Retrieves the authenticated user's top artists.

## Troubleshooting

- `ModuleNotFoundError`: Ensure all dependencies are installed. Check requirements.txt and use pip install -r requirements.txt.
- Authentication Issues: Verify your .env file contains the correct Spotify API credentials.
- Invalid Redirect URI: Ensure that the redirect URI in your Spotify Developer Dashboard matches the one in your .env file.
