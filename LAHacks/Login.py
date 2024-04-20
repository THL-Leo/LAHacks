import functools
import json
import os
import time
import reflex as rx
import Backend.spotify as spotify
import secrets
import string


CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_API", "")



class Login_state(rx.State):
    authorization_code: str = rx.LocalStorage('')
    access_code: str = rx.LocalStorage('')
    state: str = rx.LocalStorage('')

    def parse_URI(self):
        args = self.router.page.params
        code = args.get('code', None)
        state = args.get('state', None)
        return code, state

    def get_access_token(self):
        self.authorization_code, self.state = self.parse_URI()

    def on_success(self, id_token: dict):
        self.access_code = json.dumps(id_token)

    def logout(self):
        self.access_code = ''

def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

random_string = generate_random_string(16)

def login() -> rx.Component:
    return rx.center(
        rx.box("Login to Spotify", class_name="p-4", style={"width": "300px"}),
        rx.link("Login", href=spotify.login(random_string), class_name="btn btn-primary"),
    )

def on_load(self):
    print(Login_state.authorization_code)
    if not len(Login_state.authorization_code) == 0:
        Login_state.parse_URI()



        

