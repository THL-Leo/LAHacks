import requests

from flask import Flask

app = Flask(__name__)

app.secret_key = '9bf9a99c9bf4c5243b38a73501778cd0d66dd676d761d1f4'

# information provided by spotify
CLIENT_ID = '92195f066c464f1089b36bd63547285f'
CLIENT_SECRET = '153058ff6ab24fa4ae2ad10341251679'
REDIRECT_URI = 'http://localhost:3000/'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token' # refresh token
API_BASE_URL = 'https://api.spotify.com/v1/'

# root of flask app
'''
@app.route('/') 
def index():
    return "<a href='/login'>Login Spotify </a>" # redirects to endpoint
    '''



# want user to login for access token
@app.route('/login')
def login():
    # user-read-private = get current user's profile / username
    scope = "user-read-private user-read-email playlist-read-private"

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code', # spotify documentation tells us to set us at code
        'redirect_uri': REDIRECT_URI, # on incorrect logins

    }




