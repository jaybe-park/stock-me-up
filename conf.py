import json


def get_key(name: str):
    keys = json.load(open('./keys.json'))
    return keys[name]
