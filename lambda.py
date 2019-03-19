#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import re

from chess_openings import get_random_opening, get_chosen_opening, get_opening_by_first_moves

# Global vars to hold the openings
openings_by_name = {}
keys_by_name = []
openings_by_pgn = {}
keys_by_pgn = []


def lambda_handler(event, context):
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])


def on_session_started(session_started_request, session):
    return

def on_launch(launch_request, session):
    return get_welcome_response()
    
# Initialize global variables
def check_and_fill_data():
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


def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    check_and_fill_data()

    if intent_name == "GetRandomOpeningIntent":
        return get_random_opening_request()
        
    elif intent_name == "GetSpecificOpeningIntent":
        try:
            opening_name = intent_request['intent']['slots']['OpeningName']['value']
            opening_name = opening_name.lower()
        except:
            return get_opening_not_found_response()
        try:
            count = int(intent_request['intent']['slots']['Count']['value'])
        except:
            count = 1
            
        return get_specific_opening_request(opening_name, count)
        
    elif intent_name == "GetOpeningByMoveIntent":
        try:
            moves = intent_request['intent']['slots']['Moves']['value']
            moves = re.sub(r'([abcdefgh]) (\d)', r'\g<1>\g<2>', moves)
        except:
            return get_opening_not_found_response()
        try:
            count = int(intent_request['intent']['slots']['Count']['value'])
        except:
            count = 1
        
        return get_opening_by_move_request(moves, count)
        
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
        
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
        
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("Ending session.")
    # Cleanup goes here...


def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Chess Openings. Ask me for any opening!"
    reprompt_text = "Please ask me for a chess opening, you may say 'talk me about the Amar Opening'."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
                          card_title, speech_output, reprompt_text, should_end_session))


def get_help_response():
    session_attributes = {}
    card_title = "Help"
    speech_output = """
        Please, ask me for a chess opening: you may say 'Suggest me a new opening', 
        'Tell me about the Amar Opening' or 'Give me three openings that start with g4'.
        By the way, the Encyclopedia of Chess Openings (or ECO) is a classification system 
        for the opening moves in chess. It splits openings in five categories: Volume A (Flank Openings),
        Volume B (Semi-Open Games other than the French Defense), Volume C (Open Games and the French Defense),
        Volume D (Closed Games and Semi-Closed Games) and Volume E (Indian Defenses).
        Ask Alexa for more information on the matter.
    """
    reprompt_text = speech_output
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_opening_not_found_response():
    session_attributes = {}
    card_title = "Not Found"
    speech_output = "Couldn't find any opening based on your request, please try again!"
    reprompt_text = "Couldn't find any opening based on your request, please try again!"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_random_opening_request():
    global openings_by_name, keys_by_name
    
    opening = get_random_opening(openings_by_name, keys_by_name)
    result = f"Your new opening is the {opening['name']} (ECO {opening['eco']}) that goes like: {opening['pgn']}"

    # Build response
    session_attributes = {}
    card_title = "Your opening"
    speech_output = result
    reprompt_text = speech_output
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session)
    )


def get_specific_opening_request(opening_name, count):
    global openings_by_name, keys_by_name
    
    openings = get_chosen_opening(opening_name, openings_by_name, keys_by_name, count)
    
    n_items = len(openings)
    
    if n_items > 0:
        if n_items == 1:
            result = "The main variation of the requested opening is "
        else:
            result = "I've found:\n"
        for opening in openings:
            result += f"the {opening['name']} (ECO {opening['eco']}) that goes like: {opening['pgn']}.\n"
    else:
        result = "Sorry, I've found nothing."
    
    # Build response
    session_attributes = {}
    card_title = f"Your opening"
    speech_output = result
    reprompt_text = speech_output
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session)
    )
    
def get_opening_by_move_request(moves, count):
    global openings_by_pgn, keys_by_pgn
    
    openings = get_opening_by_first_moves(moves, openings_by_pgn, keys_by_pgn, count)
    
    n_items = len(openings)
    
    if n_items > 0:
        if n_items == 1:
            result = "The main variation of the requested opening is "
        else:
            result = "I've found:\n"
        for opening in openings:
            result += f"the {opening['name']} (ECO {opening['eco']}) that goes like: {opening['pgn']}.\n"
    else:
        result = "Sorry, I've found nothing."
    
    # Build response
    session_attributes = {}
    card_title = f"Your opening"
    speech_output = result
    reprompt_text = speech_output
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session)
    )


def handle_session_end_request():
    card_title = "Thanks"
    speech_output = "Thank you for using the skill. See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
