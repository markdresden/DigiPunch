import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost",1883,60)
while True:
	id = input('Enter your ID: ')
	if id != 'q':
		client.publish("digipunch/terminals",id)
		print("Punch sent!")
	else:
		client.disconnect()
		print("Exiting...")
		exit()
