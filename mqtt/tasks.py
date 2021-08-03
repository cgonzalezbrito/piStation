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
    global UUID
    global BROKER_HOST 
    global BROKER_PORT
    global CLIENT_ID
    global TOPICS
    global STATUS
    TOPICS = []
    UUID = self.uuid
    BROKER_HOST = str(self)
    BROKER_PORT = self.broker_port
    CLIENT_ID = str(self.client_id)
    topic = (self.fields.topic.location.place + '/' + self.fields.topic.location.location, 0)
    TOPICS.append(topic)
    STATUS = self.status
    return

def on_connect(client, userdata, flags, result_code):
    if result_code == 0:
        logger.info("Connected to MQTT Broker")
    else:
        logger.error("Failed to connect to MQTT Broker: " +
                      mqtt.connack_string(result_code))

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

    found = 0

    if found == 0:
        logger.error("Unhandled message topic {} with payload " +
                      str(msg.topic))

def on_publish(client, userdata, mid):
    logger.debug("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, userdata, level, buf):
    logger.debug("Log level", level)
    #if buf.find("ERROR"):
    #    logger.debug("ERROR catched")
    print(buf)

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


def mqtt_stop():
    logger.info("MQTT stop")
    try:
        client.loop_stop()
        client.disconnect()
    except:
        logger.info("Not client yet")

def get_data():
    # TODO: GET DATA TO SEND
    return '123'

@app.task
@shared_task
def main_device_task():
    """ Main function. Get, process and send data """

    # Ask for active brokers 
    broker_objects = Broker.objects.filter(status=True)
    print(broker_objects)
    for obj in broker_objects:
        _read_broker_data(obj)

        logger.info('GET DATA')
        data = get_data()
        logger.info('SEND DATA')
        mqtt_start(UUID)
        for topic in TOPICS:
            print(topic)
            client.loop_start()
            client.publish(topic[0], data, qos=2, retain=False)
            client.loop_stop()
