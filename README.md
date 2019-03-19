# Alexa Chess Openings

Source code for the Alexa Chess Openings skill. Here you can find the lambda function code, logic for formatting the openings from the original file 'openings.json' to PGN and the individual resulting JSON files. Credit to niklasf for the dataset (https://github.com/niklasf/eco).

## Skill description

Have you ever wondered about that flashy opening that your opponent pulls out of nowhere? What where the main lines used by the great chess players in History? How many variations from the Réti Opening do exist?

This skill allows you to discover old and hypermodern openings that will make you improve your game. You can ask for any opening by its name or by its first moves (with PGN notation). It will return the main line and as many variations as you want with their name, ECO classification and list of moves. You can also ask for random openings to explore new ideas. There are 3000+ variations available.

The Encyclopedia of Chess Openings (or ECO) is a classification system for the opening moves in chess. It splits openings in five categories: Volume A (Flank Openings), Volume B (Semi-Open Games other than the French Defense), Volume C (Open Games and the French Defense), Volume D (Closed Games and Semi-Closed Games) and Volume E (Indian Defenses).

Examples:
- Alexa, ask Chess Openings to give me a new random opening.
- Alexa, ask Chess Openings to explain me the Réti opening.
- Alexa, ask Chess Openings to give me three variations of the Grob.
- Alexa, ask Chess Openings to tell me which opening starts with g four.
- Alexa, ask Chess Openings to give me five variations that start with g four.

Check the source code, make suggestions or contact me -> https://github.com/ZipBomb

Icon made by Gregor Cresnar from www.flaticon.com.

---
**Project licensed under the MIT License.**