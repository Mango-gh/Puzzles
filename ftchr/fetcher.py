import requests
import json

API_URL = 'https://script.google.com/macros/s/AKfycbxXViBBf9C2MaWW99NH12qChdFQwOIudMC7kE65BFOedTBm70vPRj5xNOsmOQDYcC8/exec'


def fetch_json(url: str):
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching: {e}')
    except json.JSONDecodeError as e:
        print(f'Error parsing JSON: {e}')
    return None


def main():
    data = fetch_json(API_URL)
    if data is None:
        print('No data received.')
        return
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
