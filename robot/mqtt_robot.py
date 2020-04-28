# www.thinkcreatelearn.co.uk
#
# MQTT Controlled Raspberry Pi Robot
#
# Handles the incoming MQTT messages and translates them into robot movements.
#
# How you then respond to those messages depends on your robot hardware and the behaviour you want.
#
# This code assumes you have a simple robot similar to the one described here:
#   https://projects.raspberrypi.org/en/projects/build-a-buggy/2
#
# But there are lots of ways to build robots with a Raspberry Pi, so adjust the code as necessary.
#


# Imports
# -------------------------------------------------------------------------------------------------

from gpiozero import Robot              # controls the robot hardware
import paho.mqtt.client as mqtt         # provides IoT functionality to send messages between computers

# Constants
# -------------------------------------------------------------------------------------------------

# Settings for MQTT communication
MQTT_BROKER = "web-server"              # Change to name of your broker 
MQTT_TOPIC = "robots/clarissa"          # Change to name of your topic

# Globals
# -------------------------------------------------------------------------------------------------

# Set the GPIO pins used to connect to the motor controller
robot = Robot(left=(19,26), right=(16,20))


# Functions
# -------------------------------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    # Called when the client receives connection acknowledgement response from the broker

    print("MQTT Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)

 
def on_message(client, userdata, msg):
    # Called when a PUBLISH message is received from the broker

    # Extract the message
    m = msg.payload.decode("utf-8")
    print(msg.topic+" " + m)

    # Depending on the message received, make the robot respond
    if m=="forward":
        robot.forward(1.0) 
    elif m=="backward":
        robot.backward(1.0) 
    elif m=="left":
        robot.left(1.0) 
    elif m=="right":
        robot.right(1.0) 
    elif m=="stop":
        robot.stop() 
    


# ======================================================================================================
# Main program
# ======================================================================================================

# Create an MQTT client, which will allow the robot to receive messages
client = mqtt.Client()

# Set up the function that will be called when we connect to the broker
client.on_connect = on_connect

# Set up the function that will be called when we receive a message
client.on_message = on_message
 
# Connect to the broker, so we can receive messages
client.connect(MQTT_BROKER)
 
# Now just loop, waiting for messages
client.loop_forever()
