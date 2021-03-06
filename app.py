import collections
import json
import os
import random
from flask import Flask, request, render_template
from flask.helpers import make_response
from util import sets

app = Flask(__name__)

main_dist = [1] * 10 + [2] * 3

rare_dist = [3] * 7 + [4]

extra_dist = ([1] * 10 + [2] * 3 + [3]) * 7 + [4]

@app.route('/')
def index():
    return render_template('index.html', sets=sets)


def get_land():
    l = {}
    for land in ["Mountain", "Forest", "Island", "Plains", "Swamp"]:
        l[land] = 3
    return l


@app.route('/generate')
def generate():
    gen_sets = []
    arg_sets = request.args.get('sets', None)
    arg_single_set = request.args.get('set', None)
    if arg_sets:
        gen_sets = arg_sets.lower().split(',')
    elif arg_single_set:
        gen_sets = [arg_single_set]
    else:
        return "No set specified", 400

    cards = {
        1: [],
        2: [],
        3: [],
        4: []
    }

    for set in gen_sets:
        if set not in sets:
            return "No such set: {}".format(set), 404

        with open('sets/{}.json'.format(set), 'r') as data:
            js = json.load(data)
            for rarity in js:
                cards[int(rarity)].extend(js[rarity])

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

    name = "packwars-{}".format(''.join(gen_sets))

    deck = render_template('packwars.cod', cards=pack, name=name)
    response = make_response(deck)
    response.headers["Content-Disposition"] = "attachment; filename={}.cod".format(name)

    return response

if __name__ == '__main__':
    app.run(debug=True)