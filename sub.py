import paho.mqtt.client as mqtt
import subprocess

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("digipunch/terminals")
def on_message(client, userdata, msg):
    print(msg.topic+": "+str(msg.payload.decode()))
    subprocess.call("python3 rpi_spreadsheet.py " + msg.payload.decode(), shell=True)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
