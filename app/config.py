import os

class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    AUTH_URL = "https://accounts.spotify.com/api/token"
    AUTH_URL_AUTHORIZE = "https://accounts.spotify.com/authorize"
    SCOPES = "user-top-read"

