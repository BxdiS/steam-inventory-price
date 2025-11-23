import requests

def get_contextid(appid: int) -> int:
    return 6 if appid == 753 else 2

def get_inventory(steamid64, appid, contextid):
    url = f"https://steamcommunity.com/inventory/{steamid64}/{appid}/{contextid}?l=english&count=2500"
    try:
        response = requests.get(url, timeout=10).json()
    except Exception as e:
        print("Inventory request error:", e)
        return []

    if 'assets' not in response or 'descriptions' not in response:
        print("Inventory is empty or unavailable.")
        return []

    desc_map = {(d["classid"], d["instanceid"]): d for d in response['descriptions']}
    items = []
    for asset in response['assets']:
        key = (asset['classid'], asset['instanceid'])
        desc = desc_map.get(key)
        if desc:
            items.append(desc.get('market_hash_name', desc.get('name', 'Unknown')))
    return items
