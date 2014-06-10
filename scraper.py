#!/usr/bin/env python3
import collections
import json
import requests
import os
from bs4 import BeautifulSoup
from util import sets

rarity_to_id = {
    'Common': 1,
    'Uncommon': 2,
    'Rare': 3,
    'Mythic Rare': 4
}


def scrape_set(code):
    print("Fetching data for set {}".format(code))
    html = requests.get('http://magiccards.info/{}/en.html'.format(code)).text
    soup = BeautifulSoup(html)

    name = soup.h1.text.split(' ')[0]

    # Please, magiccards.info, never change your shitty <table>-based layout
    rows = soup.find_all('table')[-2].contents[2:]

    cards = {
        1: [],
        2: [],
        3: [],
        4: []
    }

    for row in rows:
        if row == '\n':
            continue
        data = row.contents
        #import pdb; pdb.set_trace()
        # Parse an individual card
        card = data[3].text
        try:
            rarity = rarity_to_id[data[9].text]
        except KeyError:
            continue

        cards[rarity].append(card)

    with open('sets/{}.json'.format(code), 'w') as f:
        print(cards)
        json.dump(cards, f, ensure_ascii=False)
    return len(cards)


def main():
    for code in sets:
        count = scrape_set(code)

if __name__ == "__main__":
    main()
