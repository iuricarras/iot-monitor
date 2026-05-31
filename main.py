import random
import os, subprocess
import psutil
import time
import json
from paho.mqtt import client as mqtt_client
from paho.mqtt import subscribe as mqtt_subscribe

broker = '127.0.0.1'
port = 1883
topic = None
client_id = subprocess.check_output("hostname", shell=True).decode().strip()

def default_topic(client, userdata, message):
    global topic
    response = message.payload.decode()
    responseJSON = json.loads(response)
    if(responseJSON['hostname'] != client_id):
        return
    print(f"Received `{responseJSON['rack']}` from `{message.topic}` topic")
    topic = responseJSON['rack']


def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties=None):
    # For paho-mqtt 2.0.0, you need to add the properties parameter.
    # def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
            mqtt_subscribe.callback(default_topic,"default/gateway", qos=2)
        else:
            print("Failed to connect, return code %d\n", rc)
        
    # Set Connecting Client ID
    #client = mqtt_client.Client(client_id)
    
    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect_async(broker, port)
    return client


def main():
    osname = os.name
    if(osname == "posix"):
        client = connect_mqtt()
        client.loop_start()
        print("LINUX! :)")
        while topic is None:
            print("Waiting for topic...")
            time.sleep(5)
        while True:
            err, msg = subprocess.getstatusoutput('cat /sys/class/thermal/thermal_zone0/temp')
            temp = int(msg) / 1000
            print(f"Temp: {temp}ºC")
            cpu = psutil.cpu_percent()
            print(f"CPU: {cpu}%")
            msg = f"{{'hostname': '{client_id}', 'cpu': {cpu}, 'temp': {temp}}}"
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            time.sleep(5)
    elif(osname == "nt"):
        print("WINDOWS! :(")
        print("This script is only compatible with Linux systems. Exiting...")
    
if __name__ == "__main__":
    main()

