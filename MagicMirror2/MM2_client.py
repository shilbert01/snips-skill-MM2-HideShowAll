#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import paho.mqtt.client as mqtt
from queue import Queue

q=Queue()

def on_log(client, userdata, level, buf):
	print("log: ",buf)

def on_disconnect(client, userdata, flags, rc=0):
	print("DisConnected flags"+"result code "+str(rc))
	client.connected_flag=False

def on_connect(client, userdata, flags, rc):
	if rc == 0:
	    client.connected_flag=True # set flag
	    print("connected OK")
	else:
	    client.bad_connection_flag=True
	    print("Bad connection Return code=", rc)

def on_message(client, userdata, message):
	client.on_message_flag=True #set flag
	print("received message =",str(message.payload.decode("utf-8")))
	q.put(str(message.payload.decode("utf-8")))

class SnipsMM2(object):
	def __init__(self, ipaddress, site_id):
	    self.broker_ip = ipaddress
	    self.site_id = site_id
	    mqtt.Client.connected_flag=False # create flag in class
	    mqtt.Client.bad_connection_flag=False

	def mqtt_messenger(self,subscription_topic,pub_topic,pub_msg):
	    broker=self.broker_ip
	    client = mqtt.Client("client-002") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
	    client.on_log=on_log #client logging
	    client.on_message=on_message #bind call back function
	    client.on_connect=on_connect #bind call back function
	    client.on_disconnect=on_disconnect
	    client.loop_start() #start loop to process received messages
	    print("connecting to broker ",broker)
	    try:
		client.connect(broker)#connect
	    except:
		return "An error occured. I was not able to connect to the ebus mqtt server"
	    while not client.connected_flag and not client.bad_connection_flag: # wait in loop
	    	print(client.connected_flag)
	    	print("In wait loop")
	    	time.sleep(1)
		if client.bad_connection_flag:
		    client.loop_stop()     # Stop loop
		    return "An error occured during mqtt connection. Bad connection return code was raised"
	    print("In Main loop")
	    client.subscribe(subscription_topic)#subscribe
	    ret = client.publish(pub_topic,pub_msg,0)#publish
	    print("publish",ret)
	    time.sleep(1)
	    while not q.empty():
		results = q.get()
	    print("message payload",results)
	    client.loop_stop() #stop loop
	    client.disconnect() #disconnect
	    return results

	def MM2_Hide(self,intentname,action):
	    result = 0
	    param = intentname
	    topic = "external/MagicMirror2/"+param
	    pub_topic, pub_msg = topic, json.dumps(action)
	    while result != action:
		result = mqtt_messengert(topic, pub_topic, pub_msg)
		print("result",result,"action",action)

	def setHeatingCurve(self,curve):
	    result = 0
	    if self.hs == '2':
		param, subparam = "HeatingCurve", "curve"
		topic = self.prefix+"/mc/"+param+"/"+subparam #publish
	    else:
		return None
	    pub_topic, pub_msg = topic+"/set", curve
	    while result != curve:
		result = self.mqtt_messenger(topic,pub_topic,pub_msg)
		print("result",result,"curve",curve)
	    return result
