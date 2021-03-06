"""
Skill to handle the Pollen Count Alexa skill
"""

from __future__ import print_function

import os

from pypollen import Pollen
from geopy.geocoders import Nominatim
import requests

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if event['session']['application']['applicationId'] != os.environ['SKILL_ID']:
        raise ValueError("Invalid Application ID")

    if event['session'].get('new'):
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'], event['context'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session, context):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'] + ", intentName=" + intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "LocationRequestIntent":
        return handle_location_request(intent)
    elif intent_name == "HomeRequestIntent":
        return handle_home_request(context)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def handle_home_request(context):
    """ Handle a request for home """

    city = get_home_city(context)

    if city:
        return handle_request(city)
    else:
        print("Requesting permission")
        return build_response({}, build_permissions_response())

def handle_location_request(intent):
    """ Handle a request for a specified City """

    city = intent['slots']['Location']['value']
    return handle_request(city)

def handle_request(city):
    """ Handle a request for the provided city """
    session_attributes = {}

    try:
        pollen_count = get_pollen_count(city)

        if (pollen_count is not None):
            card_title = "Pollen Count"
            should_end_session = True
            reprompt_text = None
            speech_output = "Today in %s, the Pollen Count is %s" % (city, pollen_count)

            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        else:
            should_end_session = True
            reprompt_text = None
            speech_output = "I'm sorry, but there is currently no pollen count "\
                "for %s. Pollen Count is only available within the UK "\
                "and only during the pollen season." % city

            return build_response(session_attributes, build_speech_response(
                speech_output, reprompt_text, should_end_session))
    except ValueError:
        should_end_session = False
        speech_output = "I'm sorry, I was not able to lookup %s. "\
                 "You can request the pollen count for your "\
                 "current location by saying 'give me an update'. You can also ask for "\
                 "the count anywhere in the UK by asking, 'what is the pollen count in "\
                 "Glasgow'. How can I help? " % city
        reprompt_text = "Please tell me how I can help? " \
                        "For example; give me an update."

        return build_response(session_attributes, build_speech_response(
            speech_output, reprompt_text, should_end_session))
    except RuntimeError as e:
        should_end_session = True
        reprompt_text = None
        speech_output = "I'm sorry, the UK Social Pollen Count service this "\
            "skill uses is having difficulties at the moment. As a result, I can't give "\
            "you an update for %s. " % city

        return build_response(session_attributes, build_speech_response(
            speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ Welcome the user and suggest an utterance """

    session_attributes = {}
    speech_output = "Welcome to Pollen Count, you can request the pollen count " \
                    "for your current location by saying 'give me an update'. " \
                    "You can also ask for the count anywhere in the UK by asking, " \
                    "'what is the pollen count in Glasgow'. How can I help? "
    reprompt_text = "Please tell me how I can help? " \
                    "For example; give me an update."
    should_end_session = False

    return build_response(session_attributes, build_speech_response(
        speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    """ Polite goodbye message when ending the request early"""

    speech_output = "Thank you for using Pollen Count. Have a nice day! "
    should_end_session = True

    return build_response({}, build_speech_response(
        speech_output, None, should_end_session))

# --------------- Library -------------------

def get_home_city(context):
    """ Using the context, lookup the device's address """

    device_id = context['System']['device']['deviceId']
    consent_token = context['System']['user']['permissions'].get('consentToken')
    api_endpoint = context['System']['apiEndpoint']

    if consent_token:
        url = api_endpoint \
            + "/v1/devices/" + device_id \
            + "/settings/address"

        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + consent_token
        }

        json = {}

        init_res = requests.get(url, headers=headers, allow_redirects=False)
        if init_res.status_code == 307:
            api_response = requests.get(init_res.headers['Location'],
                                        headers=headers, allow_redirects=False)
            if api_response.status_code == 200:
                json = api_response.json()
        elif init_res.status_code == 200:
            json = init_res.json()

        return json['city']

def get_pollen_count(city):
    """ Given the city, download the pollen count """
    (lat, long) = get_lat_long(city)
    return Pollen(lat, long).pollencount

def get_lat_long(city):
    """ Given a UK City, find the lat long """
    geolocator = Nominatim(country_bias="gb",
                           user_agent="pollen_count_backend")
    location = geolocator.geocode(city)
    if location:
        return (location.latitude, location.longitude)

    raise ValueError("Nominatim Lookup failed for %s" % city)

# --------------- Helpers that build all of the responses ----------------------

def build_permissions_response():
    """ Build a response containing only speech """
    output = "I'm sorry, I was not able to lookup your home town. "\
             "With your permission, I can provide you with this information. "\
             "Please check your companion app for details"
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'AskForPermissionsConsent',
            'permissions': [
                'read::alexa:device:all:address'
            ]
        },
        'shouldEndSession': True
    }

def build_speech_response(output, reprompt_text, should_end_session):
    """ Build a response containing only speech """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """ Build a response containing both speech and a card """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    """ Standard response """
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
