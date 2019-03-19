#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chess.pgn
import json
import re
import io

def main():
    """ Main program """
    with open('openings.json', encoding='utf-8') as f:
        openings = json.load(f)

    openings_by_name, openings_by_pgn = {}, {}

    for opening in openings:
        # Get name, ECO and UCI moves from the openings file
        name = opening['n'].lower().replace("-", " ").replace("'", "").replace(",", "").replace(":", "").replace("é", "e")
        eco = opening['c'].lower()
        moves = opening['m'].split(" ")
        # Start a game and keep adding the moves
        game = chess.pgn.Game()
        node = game.add_variation(chess.Move.from_uci(moves.pop(0)))
        for move in moves:
            node = node.add_variation(chess.Move.from_uci(move))
        # Export the current game as PGN in a string
        exporter = chess.pgn.StringExporter(headers=False, variations=False, comments=False)
        pgn_string = game.accept(exporter)

        # Fix for pieces name
        pgn_string = pgn_string.replace("N", "knight ")
        pgn_string = pgn_string.replace("B", "bishop ")
        pgn_string = pgn_string.replace("R", "rook ")
        pgn_string = pgn_string.replace("Q", "queen ")
        pgn_string = pgn_string.replace("K", "king ")
        pgn_string = pgn_string.replace("x", " takes ")
        pgn_string = pgn_string.replace("+", " check ")
        pgn_string = pgn_string.replace("#", " checkmate ")
        pgn_string = pgn_string.replace("O-O-O", "castles queenside")
        pgn_string = pgn_string.replace("O-O", "castles kingside")
        pgn_string = pgn_string.replace("1.", "")
        pgn_string = re.sub(r"\d+\.", ".", pgn_string)
        pgn_string = re.sub("[ ]+\.", ".", pgn_string)
        pgn_string = pgn_string.replace('*', '')
        pgn_string = pgn_string.replace("  ", " ")
        
        content = {"name": name, "eco": eco, "pgn": pgn_string.strip()}

        openings_by_name[name] = content
        new_key = re.sub(r"\.", "", content['pgn'])
        openings_by_pgn[new_key] = content

    keys_by_name = list(openings_by_name.keys())
    keys_by_pgn = list(openings_by_pgn.keys())

    result = [openings_by_name, openings_by_pgn, keys_by_name, keys_by_pgn]
    result_names = ["openings_by_name", "openings_by_pgn", "keys_by_name", "keys_by_pgn"]

    i = 0
    for name in result_names:
        with io.open(f"{name}.json", 'w', encoding='utf8') as outfile:
            json.dump(result[i], outfile, ensure_ascii=False)
        i += 1


if __name__ == "__main__":
    main()