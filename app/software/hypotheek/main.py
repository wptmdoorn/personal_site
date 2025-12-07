from nicegui import ui, app, run
# from pytube import YouTube
from io import BytesIO
import requests


SOFTWARE_TYPE = "NICEGUI"

# Load your HTML file from GitHub
url = "https://raw.githubusercontent.com/wptmdoorn/hypotheek_calculator/refs/heads/main/hypotheek.svg"
html_content = requests.get(url).text


def content():
    app.storage.user['ready'] = False
    app.storage.user['resolutions'] = []
    app.storage.user['resolution'] = -1
    app.storage.user['title'] = None
    app.storage.client['stream'] = None

    ui.add_body_html(html_content)
