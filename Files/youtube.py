import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# env
load_dotenv()
API_KEY = os.getenv("GOOGLE_KEY")
youtube = build('youtube', 'v3', developerKey=API_KEY)

# constants
url_types = ["https://www.youtube.com", "https://youtu.be/", "https://music.youtube.com/"]
possible_endings = ["official", "music", "lyric", "audio", "visualizer", "video"]
possible_separators = [" – ", " - "]
open_parentheses = ["(", "<", "[", "{"]
closed_parentheses = [")", ">", "]", "}"]


def is_youtube_link(link):
    return any(url in link for url in url_types)


def get_snippet(_id):
    return youtube.videos().list(part="snippet", id=_id).execute()["items"][0]["snippet"]


def process_link(link):
    if link.startswith("<"):
        link = link[1:-1]
    if link.startswith("https://youtu.be/"):
        return link[17:]
    else:
        return link.split("watch?v=")[-1]


def get_data(snippet):
    data = {"title": snippet["title"], "artist": snippet["channelTitle"]}

    if " - Topic" in data["artist"]:
        data["artist"] = data["artist"][:data["artist"].index(" - Topic")]

    for separator in possible_separators:
        if separator in data["title"]:
            potential_artist = data["title"][:data["title"].index(separator)]
            if potential_artist in data["artist"] \
                    or potential_artist.replace(" ", "") in data["artist"]\
                    or data["artist"] in potential_artist:
                data["artist"] = potential_artist
                data["title"] = data["title"][data["title"].index(separator) + 3:]
            break

    for ending in possible_endings:
        if ending in data["title"].lower():
            data["title"] = data["title"][:data["title"].lower().index(ending)-1].strip()
            break

    for i in range(len(open_parentheses)):
        if open_parentheses[i] in data["title"] and closed_parentheses[i] not in data["title"]:
            data["title"] = data["title"][:data["title"].index(open_parentheses[i])]

    return data


def echo_info(link):
    video_id = process_link(link)
    data = get_data(get_snippet(video_id))
    return [data["title"], data["artist"], f"https://youtu.be/{video_id}"]
