#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import re

openings_by_name, openings_by_pgn = {}, {}
keys_by_name, keys_by_pgn = [], []

# Give me a new opening
def get_random_opening(openings_by_name, keys_by_name):
    key = random.choice(keys_by_name)
    return openings_by_name[key]

# Tell me about the Amar Opening
# Tell me 5 variations of the Amar Opening
def get_chosen_opening(name, openings_by_name, keys_by_name, limit=None):
    keys = keys_by_name
    matches = list(filter(lambda key: key.startswith(name), keys))
    
    if limit is not None and limit > 0:
        matches = matches[:limit]

    result = []
    for match in matches:
        result.append(openings_by_name[match])
    
    return result

# Which openings start with b3? (all the...)
# Tell me 5 variations that start with g4
def get_opening_by_first_moves(first_moves, openings_by_pgn, keys_by_pgn, limit=None):
    keys = keys_by_pgn
    matches = list(filter(lambda key: key.startswith(first_moves), keys))

    if limit is not None and limit > 0:
        matches = matches[:limit]
    
    result = []    
    for match in matches:
        result.append(openings_by_pgn[match])

    return result

# Openings with ECO = A00
def get_opening_by_eco(eco, openings_by_eco, keys_by_eco, limit=None):
    keys = keys_by_eco
    matches = list(filter(lambda key: key == eco, keys))

    if limit is not None and limit > 0:
        matches = matches[:limit]
    
    result = []    
    for match in matches:
        result.append(openings_by_eco[match])

    return result


def main():
    """ Main program """

    # Initialize global variables
    global openings_by_name, openings_by_pgn
    global keys_by_name, keys_by_pgn

    if len(keys_by_name) == 0 or len(keys_by_pgn) == 0:
        with open('openings_by_name.json', encoding='utf-8') as f:
            openings_by_name = json.load(f)
        with open('openings_by_pgn.json', encoding='utf-8') as f:
            openings_by_pgn = json.load(f)
        with open('keys_by_name.json', encoding='utf-8') as f:
            keys_by_name = json.load(f)
        with open('keys_by_pgn.json', encoding='utf-8') as f:
            keys_by_pgn = json.load(f)
            
    opening = get_random_opening(openings_by_name, keys_by_name)
    print(f"Your new opening is the {opening['name']} (ECO {opening['eco']})-> {opening['pgn']}")
    
    keyword = 'hungarian opening'
    openings = get_chosen_opening(keyword, openings_by_name, keys_by_name)
    print(f"There are {len(openings)} variations of the {keyword}:")
    for opening in openings:
        print(f"The {opening['name']}, with ECO {opening['eco']}-> {opening['pgn']}")

    keyword = 'g3 d5'
    openings = get_opening_by_first_moves(keyword, openings_by_pgn, keys_by_pgn)
    print(f"There are {len(openings)} variations that start with {keyword}:")
    for opening in openings:
        print(f"The {opening['name']} (ECO {opening['eco']})-> {opening['pgn']}")


if __name__ == "__main__":
    main()