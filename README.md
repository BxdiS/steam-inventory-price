# Steam Inventory Price Checker

Fetch your Steam inventory items and get their current market prices in USD **without login or API key**.

Works for any game that has items on the Steam Community Market

# Features

* Fetch inventory by SteamID32, SteamID64 or Vanity URL
* Supports any Steam game via AppID
* Async fetching with progress display
* Automatic retries on empty or invalid responses
* Outputs results in JSON format
* Optional debug mode

## Requirements

* Python 3.9+
* `requests`
* `aiohttp`

Install dependencies via:

```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python main.py
```

Follow the steps:

1. Enter a SteamID32, SteamID64 or Vanity URL.
2. Enter the AppID of the game.
3. Optional: enable debug output.
4. The script fetches inventory items and their prices.
5. Results are saved automatically as a JSON file with the format: `steamid_appid_YYYYMMDD_HHMMSS.json`.

## Notes

* Random delays reduce risk of Steam temporary ip-bans.
* Maximum retries per item: 5 (10s → 1m → 5m → 10m → 20m).

## License

This project is licensed under the MIT License.

