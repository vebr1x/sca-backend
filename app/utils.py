import requests

BREEDS_CACHE = None

def validate_breed(breed_name: str) -> bool:
    global BREEDS_CACHE
    if BREEDS_CACHE is None:
        resp = requests.get("https://api.thecatapi.com/v1/breeds")
        if resp.status_code == 200:
            BREEDS_CACHE = [b["name"].lower() for b in resp.json()]
        else:
            BREEDS_CACHE = []

    return breed_name.lower() in BREEDS_CACHE
