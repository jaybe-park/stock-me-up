import json


def get_url(name: str):
    urls = json.load(open('./urls.json'))
    return urls[name]


def get_key(name: str):
    keys = json.load(open('./keys.json'))
    return keys[name]
