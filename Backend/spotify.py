import requests
import urllib.parse
from Backend.gemini import image_mood_generator
import os

import spotipy
from spotipy import SpotifyOAuth
from dotenv import load_dotenv
from LAHacks.Login import *

# information provided by spotify
# CLIENT_ID = '92195f066c464f1089b36bd63547285f'
# CLIENT_SECRET = '153058ff6ab24fa4ae2ad10341251679'
# REDIRECT_URI = 'http://localhost:3000'

# AUTH_URL = 'https://accounts.spotify.com/authorize'
# TOKEN_URL = 'https://accounts.spotify.com/api/token' # refresh token
# API_BASE_URL = 'https://api.spotify.com/v1/'


# want user to login for access token -> code sends request to spotify's authorization with our scope that gives us access to retrieve playlist later on
def get_auth_URI():
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    SCOPES = os.getenv("SCOPES")
    AUTH_URL = os.getenv("AUTH_URL")
    # TOKEN_URL = os.getenv("TOKEN_URL") # refresh token
    # API_BASE_URL = os.getenv("API_BASE_URL")
    # user-read-private = get current user's profile / username    #scope = "user-read-private user-read-email playlist-read-private"
    # state = generate_random_string(16)
    
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code', # spotify documentation tells us to set us at code
        'scope': SCOPES,
        'redirect_uri': REDIRECT_URI, # on incorrect logins
        'show_dialog': True,
    }
    
    
    # auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPES, show_dialog=True)
    # auth_url = auth_manager.get_authorize_url()
    
    # sp = spotipy.Spotify(auth_manager=auth_manager)
    # token_info = sp.auth_manager.get_cached_token()
    # access_token = None
    # if (token_info is None):
    #     access_token = sp.auth_manager.get_access_token()
    # else:
    #     access_token = token_info['access_token']

    # return auth_url, access_token
    # return auth_url
    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    # return ""


# callback endpoint -> two scenarios: user logs in successfully (gain access token) or they don't (calls the callback and error)
def callback(code):
    # load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    SCOPES = os.getenv("SCOPES")
    # AUTH_URL = os.getenv("AUTH_URL")
    TOKEN_URL = os.getenv("TOKEN_URL") # refresh token
    # API_BASE_URL = os.getenv("API_BASE_URL")
    # req_body = {
    #     'code': code,
    #     'grant_type': 'authorization_code',
    #     'redirect_uri': REDIRECT_URI,
    #     'client_id': CLIENT_ID,
    #     'client_secret': CLIENT_SECRET
    # }

    # send to spotify
    # response = requests.post(TOKEN_URL, data=req_body)
    # return response.json()
    auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPES, show_dialog=True)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    token_info = sp.auth_manager.get_cached_token()
    access_token = None
    if (token_info is None):
        access_token = sp.auth_manager.get_access_token()
    else:
        access_token = token_info['access_token']
    return access_token

async def get_playlists(access_token, img):
    raw_mood = await image_mood_generator(img)
    mood = raw_mood.candidates[0].content.parts[0].text.lower().strip(' ')
    playlist_name_mood = f"{mood} Mix"
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    print(headers)
    # passes in access token through headers
    response = requests.get("https://api.spotify.com/v1/browse/categories/0JQ5DAt0tbjZptfcdMSKl3", headers=headers) # stores the result of the request we send (PLAYLISTS ACHIEVED HERE)
    # now we have all playlists in json
    print(response)
    all_playlists = response.json().get('items', [])

    # filter for special playlists with words
    # happy, sad, energetic, angry, chill, carefree, classical, retro, or euphoric.
    mood_playlist = next((plist for plist in all_playlists if plist['name'].lower() == playlist_name_mood.lower()), None)

    if mood_playlist:
         return mood_playlist
    return None

def playlist_tracks(access_token, playlist_id):
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=headers)
    tracks = response.json().get('items', [])

    return [{
         'name': track['track']['name'],
         'artist': track['track']['artists'][0],
         'album': track['track']['album']['name']
    } for track in tracks[:5]]
     

        

