import requests
from .config import Config

def get_authorization_url():
    return (
        f"{Config.AUTH_URL_AUTHORIZE}"
        f"?response_type=code"
        f"&client_id={Config.CLIENT_ID}"
        f"&scope={Config.SCOPES}"
        f"&redirect_uri={Config.REDIRECT_URI}"
    )

def get_access_token(code):
    url = Config.AUTH_URL
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": Config.REDIRECT_URI,
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET
    }
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    return response_data.get("access_token")

