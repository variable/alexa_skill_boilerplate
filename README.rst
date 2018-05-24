=======================
Alexa Skill Boilerplate
=======================


.. image:: https://img.shields.io/pypi/v/alexa_skill_boilerplate.svg
        :target: https://pypi.python.org/pypi/alexa_skill_boilerplate

.. image:: https://img.shields.io/travis/variable/alexa_skill_boilerplate.svg
        :target: https://travis-ci.org/variable/alexa_skill_boilerplate

.. image:: https://readthedocs.org/projects/alexa-skill-boilerplate/badge/?version=latest
        :target: https://alexa-skill-boilerplate.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Provides a base class that helps developer to focus on developing alexa skills


* Free software: MIT license
* Documentation: https://alexa-skill-boilerplate.readthedocs.io.


Example
--------


.. codeblock:: python

    # encoding: utf-8
    import os
    import sys
    from base import Skill


    # --------------- Helpers that build all of the responses ----------------------

    class HelloWorldSkill(Skill):
        card_title = "Hello World"
        welcome_speech = """Welcome to the Alexa Skills for Hello World."""
        welcome_reprompt_text = 'You can say search food in Auckland'

        def hello_world(self, intent, session):
            """Intent Handler"""
            
            # slot_value = intent['slots']['slot_name']
        
            should_end_session = False
            session_attributes = {}
            speech_output = "Hellow World!"
            reprompt_text = None

            # Setting reprompt_text to None signifies that we do not want to reprompt
            # the user. If the user does not respond or says something that is not
            # understood, the session will end.
            return self.build_response(session_attributes, self.build_speechlet_response(
                intent['name'], speech_output, reprompt_text, should_end_session)


        @property
        def intent_handlers(self):
            handlers = super(SearchSkill, self).intent_handlers
            handlers.update({
                'HelloWorld': self.hello_world,  # adding the intent handler
            })
            return handlers

    # AWS Lambda Handler
    def handler(event, context):
        return HellowWorldSkill().lambda_handler(event, context)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
