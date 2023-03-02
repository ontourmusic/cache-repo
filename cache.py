import os
from dotenv import load_dotenv

load_dotenv()

app_id = os.environ["APP_ID"]

artist_list = [
    "Adele",
    "Andrea Bocelli",
    "Billie Eilish",
    "Billy Joel",
    "The Chainsmokers",
    "Dominic Fike",
    "Elton John",
    "Harry Styles",
    "Jack Harlow",
    "Old Dominion",
    "Post Malone",
    "Yung Gravy",
]


def url_generator(artist_name):
    import urllib.parse

    query = urllib.parse.urlencode({"app_id": app_id, "date": "past"})
    return f"https://rest.bandsintown.com/artists/{artist_name.replace(' ', '%20')}/events?{query}"


def request_cache(url):
    import requests

    try:
        result = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    return result


if __name__ == "__main__":
    import json

    artist_map = {artist: url_generator(artist) for artist in artist_list}

    cache = {}
    try:
        with open("cache.json", "r") as f:
            cache = json.load(f)
    except FileNotFoundError:
        pass

    for artist, url in artist_map.items():
        try:
            cache[artist] = request_cache(url).json()
        except Exception as e:
            print(f"Error for {artist}: {e}")
            continue

    with open("cache.json", "w") as f:
        json.dump(cache, f, indent=4)
