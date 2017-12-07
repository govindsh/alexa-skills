"""
This Alexa skills calculates percentages
"""

from __future__ import print_function

def lambda_handler(event, context):
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
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.721d5aae-179c-4550-8e58-635e485500f9"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
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

    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetPercentageInfoIntent":
        return get_percentage_info_response()
    elif intent_name == "GetPercentageIntent":
        return get_percentage_response(intent_request)
    elif intent_name == "GetPercentageResultIntent":
        return get_percentage_result(intent_request)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
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


def get_welcome_response():

    session_attributes = {}
    speech_output = "Welcome to Get Percentage app. You can ask me how much is 35 percent of 120 and I can help you with that. Lets try it now."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with the same text.
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(speech_output, reprompt_text, should_end_session))


def get_help_response():
    session_attributes = {}
    speech_output = "Welcome to the help section for the Get Percentage skill. Lets get started now by trying one of these. What is 20 percent of 120. Or, Result of 35 percent of 2000. When you ask for result I will return the difference between the original value and the percentage."

    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(speech_output,reprompt_text,should_end_session))


def get_percentage_info_response():
    session_attributes = {}
    speech_output = "The Get Percentage Skill helps you calculate percentages."

    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output,reprompt_text,should_end_session))


def get_percentage_response(intent_request):
    session_attributes = {}
    speech_output = ""
    print(intent_request)
    percent, number, result = get_result(intent_request)
    
    if percent is None or number is None or result is None:
        return error_response()
    
    speech_output = "Answer is {}.".format(result)
    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output,reprompt_text,should_end_session))

def get_percentage_result(intent_request):
    session_attributes = {}
    speech_output = ""
    percent, number, result = get_result(intent_request, get_item="result")
    if percent is None or number is None or result is None:
        return error_response()
    
    speech_output = "Answer is {}.".format(result)
    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output,reprompt_text,should_end_session))


def get_result(intent_request, get_item="percent"):
    caught_exception = False
    try:
        percent = int(intent_request["intent"]["slots"]["percent"]["value"])
        number = int(intent_request["intent"]["slots"]["number"]["value"])
    except (ValueError, KeyError):
        caught_exception = True
    if caught_exception:
        return None, None, None
    
    result = (number * percent)/100
    if get_item != "percent":
        final_answer = number - result
        return percent, number, final_answer
    return percent, number, result


def error_response():
    session_attributes = {}
    speech_output = "Sorry, I did not understand that. Please try again or ask get percentage help."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(speech_output,reprompt_text,should_end_session))


def handle_session_end_request():
    speech_output = "Thank you for using the Get Percentage skill! We hope you enjoyed the experience."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(speech_output, None, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
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
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

