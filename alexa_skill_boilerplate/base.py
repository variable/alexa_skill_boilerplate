# encoding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division


# encoding: utf-8
"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""
from __future__ import print_function
import os
import sys
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'libs')
sys.path.append(vendor_dir)
import requests


# --------------- Helpers that build all of the responses ----------------------

class Skill(object):

    # common attributes
    welcome_card_title = 'Welcome'
    welcome_speech = "Welcome to the Alexa Skills"
    welcome_reprompt_text = 'This is reprompt text'
    end_card_title = 'Good bye'
    end_speech = "Good bye"

    def build_speechlet_response(self, title, output, reprompt_text, should_end_session):
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'card': {
                'type': 'Simple',
                'title': "SessionSpeechlet - " + title,
                'content': "SessionSpeechlet - " + output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }


    def build_response(self, session_attributes, speechlet_response):
        return {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': speechlet_response
        }


    # --------------- Functions that control the skill's behavior ------------------

    def get_welcome_response(self):
        """ If we wanted to initialize the session to have some attributes we could
        add those here
        """

        session_attributes = {}
        should_end_session = False
        return self.build_response(session_attributes, self.build_speechlet_response(
            self.welcome_card_title, self.welcome_speech, self.welcome_reprompt_text, should_end_session))


    def handle_session_end_request(self):
        # Setting this to true ends the session and exits the skill.
        should_end_session = True
        return self.build_response({}, self.build_speechlet_response(
            self.end_card_title, self.end_speech, None, should_end_session))

    # --------------- Events ------------------

    def on_session_started(self, session_started_request, session):
        """ Called when the session starts """

        print("on_session_started requestId=" + session_started_request['requestId']
              + ", sessionId=" + session['sessionId'])


    def on_launch(self, launch_request, session):
        """ Called when the user launches the skill without specifying what they
        want
        """

        print("on_launch requestId=" + launch_request['requestId'] +
              ", sessionId=" + session['sessionId'])
        # Dispatch to your skill's launch
        return self.get_welcome_response()


    def on_intent(self, intent_request, session):
        """ Called when the user specifies an intent for this skill """

        print("on_intent requestId=" + intent_request['requestId'] +
              ", sessionId=" + session['sessionId'])

        intent = intent_request['intent']
        intent_name = intent_request['intent']['name']

        # Dispatch to your skill's intent handlers
        if intent_name in self.intent_handlers:
            return self.intent_handlers[intent_name](intent, session)
        elif intent_name == "AMAZON.HelpIntent":
            return self.get_welcome_response()
        elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
            return self.handle_session_end_request()
        else:
            raise ValueError("Invalid intent")


    def on_session_ended(self, session_ended_request, session):
        """ Called when the user ends the session.

        Is not called when the skill returns should_end_session=true
        """
        print("on_session_ended requestId=" + session_ended_request['requestId'] +
              ", sessionId=" + session['sessionId'])
        # add cleanup logic here

    @property
    def intent_handlers(self):
        """
        # TODO think about better way for better inheritance
        To be extended here with more intent handlers
        """
        return {
            'AMAZON.HelpIntent': self.get_welcome_response,
            'AMAZON.CancelIntent': self.handle_session_end_request,
            'AMAZON.StopIntent': self.handle_session_end_request
        }

    # --------------- Main handler ------------------
    def lambda_handler(self, event, context):
        """ Route the incoming request based on type (LaunchRequest, IntentRequest,
        etc.) The JSON body of the request is provided in the event parameter.
        """
        print("event.session.application.applicationId=" +
              event['session']['application']['applicationId'])

        """
        Uncomment this if statement and populate with your skill's application ID to
        prevent someone else from configuring a skill that sends requests to this
        function.
        """
        # if (event['session']['application']['applicationId'] !=
        #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
        #     raise ValueError("Invalid Application ID")

        if event['session']['new']:
            self.on_session_started({'requestId': event['request']['requestId']},
                               event['session'])

        if event['request']['type'] == "LaunchRequest":
            return self.on_launch(event['request'], event['session'])
        elif event['request']['type'] == "IntentRequest":
            return self.on_intent(event['request'], event['session'])
        elif event['request']['type'] == "SessionEndedRequest":
            return self.on_session_ended(event['request'], event['session'])
