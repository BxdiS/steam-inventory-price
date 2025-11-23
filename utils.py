import requests
from config import STEAMID32_OFFSET

def vanity_to_steamid64_public(vanity):
    url = f"https://steamcommunity.com/id/{vanity}/?xml=1"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("Profile not found or private.")
            return None
        import re
        match = re.search(r"<steamID64>(\d+)</steamID64>", response.text)
        return int(match.group(1)) if match else None
    except Exception as e:
        print("Request error:", e)
        return None

def steamid32_to_steamid64(steamid32):
    return int(steamid32) + STEAMID32_OFFSET

def parse_price(price_str):
    if not price_str:
        return 0.0
    try:
        return float(price_str.replace("$", "").replace(",", "").strip())
    except:
        return 0.0
