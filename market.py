import aiohttp
import asyncio
import sys
import random
import urllib.parse
from utils import parse_price

async def get_item_price(session, appid, market_name, DEBUG=False):
    url = f"https://steamcommunity.com/market/priceoverview/?currency=1&appid={appid}&market_hash_name={urllib.parse.quote(market_name)}"
    retry_delays = [10, 60, 300, 600, 1200]  # 10s, 1m, 5m, 10m, 20m

    for attempt, delay in enumerate(retry_delays, start=1):
        try:
            async with session.get(url) as resp:
                try:
                    data = await resp.json(content_type=None)
                except:
                    if DEBUG:
                        print(f"[DEBUG] {market_name}: got HTML instead of JSON")
                    data = {}

                if DEBUG:
                    print(f"[DEBUG] {market_name} attempt {attempt}: {data}")

                if data.get('success') and data.get('lowest_price'):
                    return parse_price(data['lowest_price'])

        except Exception as e:
            if DEBUG:
                print(f"[DEBUG] Error {market_name}: {e}")

        if attempt < len(retry_delays):
            if DEBUG:
                print(f"[DEBUG] Empty response, retrying in {delay} seconds...")
            await asyncio.sleep(delay)

    if DEBUG:
        print(f"[DEBUG] Failed to get price for {market_name} after all attempts.")
    return 0.0

async def fetch_prices(appid, items, DEBUG=False):
    prices = {}
    total = len(items)
    async with aiohttp.ClientSession() as session:
        for i, market_name in enumerate(items, start=1):
            price = await get_item_price(session, appid, market_name, DEBUG)
            prices[market_name] = price
            remaining = total - i
            sys.stdout.write(f"\rItems remaining: {remaining}  ")
            sys.stdout.flush()
            await asyncio.sleep(random.uniform(3, 6))
    print()
    return prices
