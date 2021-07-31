# Create your tasks here

from celery import shared_task
from piStation.celery import app

from .models import Broker, Location, PhysicalVar, Topic, Field, Fields

import paho.mqtt.client as mqtt
import json
import signal
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def _read_broker_data(self):
    global BROKER_HOST 
    global BROKER_PORT
    global CLIENT_ID
    global TOPICS
    global TOGGLE
    TOPICS = []
    TOGGLE = False
    BROKER_HOST = str(self)
    BROKER_PORT = self.broker_port
    CLIENT_ID = str(self.client_id)
    TOPICS.append(self.fields.topic.location.place + '/' + self.fields.topic.location.location)
    return

def on_connect(client, userdata, flags, result_code):
    if result_code == 0:
        logger.info("Connected to MQTT Broker")
    else:
        logger.error("Failed to connect to MQTT Broker: " +
                      mqtt.connack_string(result_code))

    count = 0
    client.publish("PC/test", payload=count, qos=2, retain=False)
    count += 1
    # TODO
    client.subscribe(TOPICS)

def on_disconnect(client, user_data, result_code):
    logger.error("Disconnected from MQTT Broker")

def on_message(client, userdata, msg):
    data = None

    try:
        data = json.loads(msg.payload.decode("UTF-8"))
    except json.JSONDecodeError as e:
        logger.error("JSON Decode Error: " + msg.payload.decode("UTF-8"))

    if not data:
        return

    logger.info("topic: %s, qos: %s" % (msg.topic, msg.qos))
    logger.info(data)

    print("MESSAGE TOPIC: " + print(type(msg.topic)))
    found = 0
    #TODO
    #for topic in TOPICS:
    #    if msg.topic == topic[0]:
    #        fields = [x for x in FIELDS if x['topic']
    #                  == msg.topic][0].get('fields')
    #        if fields:
    #            process_topic(msg.topic, data, fields[0], fields[1], fields[2])
    #            found = 1

    if found == 0:
        logger.error("Unhandled message topic {} with payload " +
                      str(msg.topic, msg.payload))

def on_publish(client, userdata, mid):
    logger.debug("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos):
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, userdata, level, buf):
    logger.debug("Log level", level)
    #if buf.find("ERROR"):
    #    logger.debug("ERROR catched")
    print(buf)

@shared_task
def mqtt_receive_data():
    # Ask for broker status
    if TOGGLE:
        # register the signals to be caught
        logger.info("Listening for messages on topic '" + "'. Press Control + C to exit.")
        client.loop_start()

def mqtt_start(uuid):
    logger.info("MQTT is starting")

    # TODO: use instance not first()
    # Get Broker config Data
    
    qs = Broker.objects.filter(uuid=uuid)
    broker_obj = qs[0]
    _read_broker_data(broker_obj)

    # Initialize Module
    global client
    client = mqtt.Client(
            client_id=CLIENT_ID,
            clean_session=False)
    # Setup callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.on_message = on_message
    client.on_log = on_log

    # Connect to Broker.
    client.connect(BROKER_HOST, BROKER_PORT)
    TOGGLE = True

    # Recive Data.
    #mqtt_receive_data()

def mqtt_stop():
    logger.info("MQTT stop")

@app.task
@shared_task
def main_device_task():
    """ Main function. Get, process and send data """
    mqtt_start()
    # Ask for broker status
    if True:
        print('GET DATA')
        client.publish("PC/test", payload='543', qos=2, retain=False)
