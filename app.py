import collections
import json
import os
import random
from flask import Flask, request, render_template_string
from flask.helpers import make_response
from util import sets

app = Flask(__name__)

main_dist = [1] * 10 + [2] * 3

rare_dist = [3] * 7 + [4]

extra_dist = ([1] * 10 + [2] * 3 + [3]) * 7 + [4]

@app.route('/')
def index():
    return 'Hello World'


def get_land():
    l = {}
    for land in ["Mountain", "Forest", "Island", "Plains", "Swamp"]:
        l[land] = 3
    return l


@app.route('/generate')
def generate():
    set = request.args.get('set', 'm14')
    if set not in sets:
        return 'No such set', 404

    with open('sets/{}.json'.format(set), 'r') as data:
        js = json.load(data)
        cards = {
            1: js["1"],
            2: js["2"],
            3: js["3"],
            4: js["4"]
        }
        pack = collections.defaultdict(int)
        #Generate the 13 main cards
        for rarity in main_dist:
            card = random.choice(cards[rarity])
            pack[card] += 1

        # Generate the rare
        rarity = random.choice(rare_dist)
        card = random.choice(cards[rarity])
        pack[card] += 1

        # Generate the 15th card
        rarity = random.choice(extra_dist)
        card = random.choice(cards[rarity])
        pack[card] += 1

        pack.update(get_land())

        deck = render_template_string('packwars.cod', cards=pack)
        response = make_response(deck)
        response.headers["Content-Disposition"] = "attachment; filename=packwars.cod"

        return response

if __name__ == '__main__':
    app.run(debug=True)