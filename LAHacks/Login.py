import functools
import json
import os
import time
import reflex as rx
import Backend.spotify as spotify

class Login_state(rx.State):
    authorization_code: str = rx.LocalStorage('')
    access_code: str = rx.LocalStorage('')
    
    @rx.var
    def parse_URI(self):
        self.authorization_code = self.router.page.params.get("code")
        if self.authorization_code != '':
            self.access_code = spotify.callback(self.authorization_code)

    def redirect_if_authorized(self):
        if self.authorization_code == '':
            return rx.redirect("/login")

    def logout(self):
        self.access_code = ''
        self.authorization_code = ''

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_API", "")


def login() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.box("Login to Spotify", class_name="p-4", style={"width": "300px"}),
            rx.link("Login", href=spotify.get_auth_URI(), class_name="btn btn-primary"),
        ),
    )