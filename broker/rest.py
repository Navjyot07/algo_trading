import requests
from broker.auth import get_headers

BASE_URL = "https://api.dhan.co"

def fetch_option_chain(underlying):
    url = f"{BASE_URL}/optionchain"
    resp = requests.get(url, headers=get_headers()).json()
    return resp["data"]   # list of options

def place_order(payload):
    url = f"{BASE_URL}/orders"
    return requests.post(url, headers=get_headers(), json=payload).json()
