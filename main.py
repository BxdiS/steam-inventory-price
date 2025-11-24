import asyncio
from datetime import datetime
from utils import vanity_to_steamid64_public, steamid32_to_steamid64
from inventory import get_inventory, get_contextid
from market import fetch_prices
import json

def save_results(prices, steamid, appid):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{steamid}_{appid}_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(prices, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved: {filename}")

def main():
    first_run = True
    DEBUG = False

    while True:
        user_input = input("Enter SteamID32, SteamID64 or Vanity URL: ").strip()
        if user_input.isdigit() and len(user_input) <= 10:
            steamid64 = steamid32_to_steamid64(int(user_input))
        if user_input.isdigit() and len(user_input) > 10:
            steamid64 = user_input
        else:
            steamid64 = vanity_to_steamid64_public(user_input)
            if steamid64 is None:
                continue
        print(f"SteamID64: {steamid64}")

        appid_input = input("Enter AppID of the game: ").strip()
        if not appid_input.isdigit():
            print("Invalid AppID.")
            continue
        appid = int(appid_input)
        contextid = get_contextid(appid)

        if first_run:
            debug_input = input("Enable debug output? (y/N): ").strip().lower()
            DEBUG = debug_input == "y"
            first_run = False

        items = get_inventory(steamid64, appid, contextid)
        if not items:
            print("Inventory is empty or unavailable.")
            continue

        print("\nFetching prices...\n")
        prices = asyncio.run(fetch_prices(appid, items, DEBUG))

        total_value = sum(prices.values())
        print(f"\nTotal inventory value: ${total_value:.2f}")

        save_results(prices, steamid64, appid)
        print("\nChecking next inventory...\n")

if __name__ == "__main__":
    main()
