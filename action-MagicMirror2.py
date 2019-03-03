#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io, json
#import paho.mqtt.client as mqtt
from MagicMirror2.MM2_client import SnipsMM2

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

# each intent has a language associated with it
# extract language of first intent of assistant since there should only be one language per assistant
lang = json.load(open('/usr/share/snips/assistant/assistant.json'))['intents'][0]['language'] 

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name: option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    user,intentname = intentMessage.intent.intent_name.split(':')  # the user can fork the intent with this method
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)

def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined 

    Refer to the documentation for further details.
    """
    intentname = intentMessage.intent.intent_name.split(':')[1]

    MM2 = SnipsMM2(conf["secret"]["magicmirror2_mqtt_ip"],conf["secret"]["site_id"])

    niy_de = 'Das ist was schiefgegangen.'
    niy_en = 'Something went wrong.'

    #conf = read_configuration_file(CONFIG_INI)
    #print("Conf:", conf)

    ## MQTT client to connect to the bus
    #mqtt_client = mqtt.Client()

    #def on_connect(client, userdata, flags, rc):
	#client.subscribe("hermes/intent/#")

    try:
        slots = {slot['slotName']: slot['value']['value'] for slot in data['slots']}
        user, intentname = data['intent']['intentName'].split(':')

        module = slots['MODULE']

        if module == 'ALL':
            mode = 'ALL'
        elif 'PAGE' in module:
            mode = 'PAGE'
        else:
            mode = 'STANDARD'

        if intentname == 'MM_Hide' and (mode == 'STANDARD' or mode == 'ALL'):
            action = {'module':module}
	    conn = MM2.MM_Hide(intentname, action)
	    if conn is None:
		if lang == 'de':
		    result_sentence = niy_de
		elif lang == 'en':
		    result_sentence = niy_en
	    else:
		if lang == 'de':
		    result_sentence = u'Die Wassertemperatur wurde auf 52 Grad gesetzt'
		elif lang == 'en':
		    result_sentence = u'The hot water temperature has been set to 52 degree'

        elif intentname == 'MM_Show' and (mode == 'STANDARD' or mode == 'PAGE') :
            action = {'module':module}
	    conn = MM2.MM_Show(intentname, action)

        elif intentname == 'MM_Move' and mode == 'STANDARD':
            position = slots['POSITION']
            action = {'module':module, 'position':position}
	    conn = MM2.MM_Move(intentname, action, position)

        else:
            raise UnboundLocalError("Das kann ich leider nicht")

        say(session_id, "Mache ich")
        #MM2(intentname, action)
    except UnboundLocalError, e:
        say(session_id, e.message)

    except KeyError:
        say(session_id, "Ich habe dich leider nicht verstanden.")
    
    hermes.publish_end_session(intentMessage.session_id, result_sentence.encode('utf-8'))

"""def message(client, userdata, msg):
    data = json.loads(msg.payload.decode("utf-8"))
    session_id = data['sessionId']
    try:
        slots = {slot['slotName']: slot['value']['value'] for slot in data['slots']}
        user, intentname = data['intent']['intentName'].split(':')

        module = slots['MODULE']

        if module == 'ALL':
            mode = 'ALL'
        elif 'PAGE' in module:
            mode = 'PAGE'
        else:
            mode = 'STANDARD'

        if intentname == 'MM_Hide' and (mode == 'STANDARD' or mode == 'ALL'):
            action = {'module':module}
        elif intentname == 'MM_Show' and (mode == 'STANDARD' or mode == 'PAGE') :
            action = {'module':module}
        elif intentname == 'MM_Move' and mode == 'STANDARD':
            position = slots['POSITION']
            action = {'module':module, 'position':position}
        else:
            raise UnboundLocalError("Das kann ich leider nicht")
        say(session_id, "Mache ich")
        MM2(intentname, action)
    except UnboundLocalError, e:
        say(session_id, e.message)

    except KeyError:
        say(session_id, "Ich habe dich leider nicht verstanden.")
"""

def MM2(intentname, action):
    mqtt_client.publish(('external/MagicMirror2/' + intentname),
                        json.dumps(action))

def say(session_id, text):
    mqtt_client.publish('hermes/dialogueManager/endSession',
                        json.dumps({'text': text, "sessionId": session_id}))

if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
	h.subscribe_intents(subscribe_intent_callback).start()

"""
if __name__ == "__main__":
    mqtt_client.on_connect = on_connect
    mqtt_client.message_callback_add("hermes/intent/captn2:MM_Hide/#", message)
    mqtt_client.message_callback_add("hermes/intent/captn2:MM_Show/#", message)
    mqtt_client.message_callback_add("hermes/intent/captn2:MM_Move/#", message)
    mqtt_client.connect("localhost", "1883")
    mqtt_client.loop_forever()
"""