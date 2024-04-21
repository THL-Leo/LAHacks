"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config
from Backend.gemini import image_mood_generator
import reflex as rx
import PIL.Image
from LAHacks.Login import *
from Backend.spotify import *

docs_url = "https://reflex.dev/docs/getting-started/introduction/"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""

    # The images to show.
    img_name: list[str] = []
    tracks: list[tuple[str, str]] = []
    # Whether there are images.
    has_img: bool = False

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Get the width and height of the image
            with PIL.Image.open(outfile) as img:
                width, height = img.size

            # Update the img var.
            self.img_name.append((file.filename, width, height))
        # Update the has_img var because images are uploaded
        self.has_img = True

        image_paths = [str(rx.get_upload_dir() / img[0]) for img in self.img_name]
        self.tracks = await spotify.get_playlists(image_paths)

        # Call image_mood_generator with the uploaded images
        # For simplicity, assuming image_mood_generator takes a list of image paths
        # self.results = result.candidates[0].content.parts[0].text

    async def clear_images(self):
        """Clear the list of images."""
        # Clear the list of images and set has_img to False
        self.img_name.clear()
        self.has_img = False
        
        

    # async def info(self):
    #     login_state = await self.get_state(Login_state)
    #     headers = {
    #         'Authorization': f"Bearer {login_state.access_code}"
    #     }
    # passes in access token through headers
        # response = requests.get('https://api.spotify.com/v1/me', headers=headers)

    # async def renew(self):
    #     login_state = await self.get_state(Login_state)
    #     login_state.access_code = await spotify.renew_token(login_state.refresh_token)

    # async def call_gemini(self, input_list, width, height):
    #     """Call the gemini API."""
    #     return image_mood_generator(input_list, width, height)


color = "rgb(107,99,246)"

def index():
    """The main view."""
    return rx.center(
                rx.vstack(
                    rx.cond(
                        State.has_img,
                        rx.grid(
                            rx.foreach(
                                State.img_name,
                                lambda img: rx.vstack(
                                    rx.image(src=rx.get_upload_url(img[0])),
                                    rx.text(img[0]),
                                    align="center",
                                ),
                            ),
                            columns="1",
                            spacing="1",
                        ),
                        rx.upload(
                            rx.vstack(
                                rx.button("Select File", color=color, bg="white", border=f"1px solid {color}"),
                                rx.text("Drag and drop files here or click to select files", class_name="lg:text-2xl md:text-lg sm:text-md"),
                            ),
                            id="upload2",
                            multiple=False,
                            accept = {
                                "image/png": [".png"],
                                "image/jpeg": [".jpg", ".jpeg"],
                                "image/heic": [".heic"],
                            },
                            max_files=1,
                            disabled=False,
                            on_keyboard=True,
                            on_drop=State.handle_upload(rx.upload_files(upload_id="upload2", multiple=False)),
                            border=f"1px dotted {color}",
                            padding="5em",
                            align="center",
                            height="50vh",
                            width="50vw",
                        ),
                    ),
                    rx.button(
                        "Clear",
                        on_click= State.clear_images(),
                    ),
                    rx.button(
                        "Logout",
                        on_click= Login_state.logout(),
                    ),
                    rx.grid(
                            rx.foreach(
                                State.tracks,
                                lambda song: rx.vstack(
                                    rx.text(song[0]),
                                    rx.text(song[1]),
                                    align="center",
                                ),
                            ),
                            columns="1",
                            spacing="1",
                        ),
                    padding="5em",
                    align="center",                 
                ),
                align="center",
        )

app = rx.App()
app.add_page(index, route = '/', on_load=Login_state.redirect_if_authorized)
app.add_page(login, route = '/login')
