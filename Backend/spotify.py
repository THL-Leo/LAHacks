import requests
import urllib.parse
from Backend.gemini import image_mood_generator


import spotipy
from spotipy import SpotifyOAuth

# information provided by spotify
CLIENT_ID = '92195f066c464f1089b36bd63547285f'
CLIENT_SECRET = '153058ff6ab24fa4ae2ad10341251679'
REDIRECT_URI = 'http://localhost:3000'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token' # refresh token
API_BASE_URL = 'https://api.spotify.com/v1/'



# want user to login for access token -> code sends request to spotify's authorization with our scope that gives us access to retrieve playlist later on
def login(state):
    # user-read-private = get current user's profile / username
    scope = "user-read-private user-read-email playlist-read-private"
    # state = generate_random_string(16)
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code', # spotify documentation tells us to set us at code
        'scope': scope,
        'redirect_uri': REDIRECT_URI, # on incorrect logins
        'show_dialog': True,
        'state': state
    }
    
    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"


# callback endpoint -> two scenarios: user logs in successfully (gain access token) or they don't (calls the callback and error)
def callback(code):
        req_body = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        # send to spotify
        response = requests.post(TOKEN_URL, data=req_body)
        return response.json()

def get_playlists(access_token, mood, img):
    mood = image_mood_generator(img)
    playlist_name_mood = f"{mood} Mix"
    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers) # stores the result of the request we send (PLAYLISTS ACHIEVED HERE)
    # now we have all playlists in json
    all_playlists = response.json().get('items', [])

    # filter for special playlists with words
    # happy, sad, energetic, angry, chill, carefree, classical, retro, or euphoric.
    mood_playlist = next((plist for plist in all_playlists if plist['name'] == playlist_name_mood), None)

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
     

        

