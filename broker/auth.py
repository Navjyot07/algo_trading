from config.settings import DHAN_ACCESS_TOKEN

def get_headers():
    return {
        "access-token": DHAN_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
