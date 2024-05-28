import requests
import json
from bs4 import BeautifulSoup


def fetch_lots():
    url = "https://goszakup.gov.kz/ru/search/lots?filter%5Bname%5D=школа"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    lots = []

    for link in soup.find_all("a"):
        link = str(link.get("href"))
        if "/ru/announce/index/" in link:
            lots.append({'id': link[19::], 'link': "https://goszakup.gov.kz"+link})

    return lots


def load_known_lots(filename='known_lots.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except json.decoder.JSONDecodeError:
        return []
    except FileNotFoundError:
        return []


def save_known_lots(lots, filename='known_lots.json'):
    with open(filename, 'w') as file:
        json.dump(lots, file)


def get_new_lots(current_lots, known_lots):
    known_lot_ids = {lot['id'] for lot in known_lots}
    return [lot for lot in current_lots if lot['id'] not in known_lot_ids]
