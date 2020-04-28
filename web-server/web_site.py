# www.thinkcreatelearn.co.uk
#
# Main web site page
# 
# Controls all web page requests and calls other functions to carry out the request
#
# Requires installation of Flask and Paho MQTT.  Install with:
#
#   pip install flask
#   pip install paho-mqtt
#
# For details see:
#   https://pypi.org/project/paho-mqtt/
#   https://pypi.org/project/Flask/


# Includes
# -------------------------------------------------------------------------------------------------

# Flask provides a framework for building web applications in Python
from flask import Flask, render_template, Response

# Paho MQTT provides the ability to send messages from one computer to another using the MQTT protocol
import paho.mqtt.publish as publish

# We keep the video streaming code in a separate python file
from pi_camera_player import VideoPlayer


# Constants
# -------------------------------------------------------------------------------------------------

# Identify the name of the computer that will act as the MQTT broker
# If it is the same as the computer that is running this web site, you can use localhost
MQTT_SERVER = "localhost"                       # Change to name of your broker 

# Identify the name of the topic that your robot will be listening on
MQTT_TOPIC = "robots/clarissa"                  # Change to name of your topic


# Global objects
# -------------------------------------------------------------------------------------------------
# Create our video player object
player = VideoPlayer()   

# Create the Flask web application
app = Flask(__name__)


# Web request handlers
# -------------------------------------------------------------------------------------------------

# The default web page returns index.html from the templates folder
@app.route('/')
def index():
    print("/")
    return render_template('index.html')

# When a request to the /video url is made, we run this
@app.route('/video')
def video_feed():          

    # Pass in the generator function to the response.  Flask will then loop around, calling the generator.
    # We use the multipart mime type.  In this case we have a video made up of multiple frames.
    # I.e. we are saying that our content is made up of multiple parts (the frames).
    return Response(player.genVideo(), mimetype='multipart/x-mixed-replace; boundary=frame')

# When a control request comes in, we run this
@app.route('/control/<control_name>')
def control(control_name):
    print(control_name)
    publish.single(MQTT_TOPIC, control_name, hostname=MQTT_SERVER)
    return Response('queued')

# Run the web site.  Specifying 0.0.0.0 as the host makes it visible to the rest of the network.
# We runs as a threaded site so we can have multiple clients connect and so the site responds to user interaction when busy streaming
if __name__ == '__main__':
    #print(flask.__version__)
    app.run(threaded=True, host='0.0.0.0') #, debug=True)