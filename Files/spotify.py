import os
from dotenv import load_dotenv
import requests
import base64

# env
load_dotenv()
ID = os.getenv("SPOTIFY_ID")
SECRET = os.getenv("SPOTIFY_SECRET")


def is_spotify_link(link):
    return "open.spotify.com" in link


def get_token():
    auth = base64.b64encode(f"{ID}:{SECRET}".encode()).decode()
    head = {"Authorization": f"Basic {auth}"}
    data = {"grant_type": "client_credentials"}
    url = "https://accounts.spotify.com/api/token"
    return requests.post(url, headers=head, data=data).json()['access_token']


def get_item(item):
    head = {"Authorization": f"Bearer {get_token()}"}
    url = f"https://api.spotify.com/v1/{ item['type']}s/{item['id']}"
    return requests.get(url, headers=head).json()


def process_link(link):
    if link.startswith("<"):
        link = link[1:-1]
    if "?si=" in link:
        link = link[:link.index("?si=")]
    values = link.split('/')[-2:]
    return {"type": values[0], "id": values[1], "link": link}


def get_title(json):
    return json['name']


def get_artists(json):
    return ", ".join([artist['name'] for artist in json['artists']])


def echo_info(discriminator, link):
    processed_link = process_link(link)
    json = get_item(processed_link)
    return [discriminator, get_title(json), get_artists(json), processed_link["link"]]
