import paho.mqtt.client as mqtt
import time
import sys

logs = []

def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe("smarthome/sensors/#")
    client.subscribe("smarthome/status")

def on_message(client, userdata, msg):
    log_line = f"[{time.strftime('%H:%M:%S')}] TOPIC: {msg.topic} | QoS: {msg.qos} | RETAIN: {msg.retain} | PAYLOAD: {msg.payload.decode()}"
    logs.append(log_line)
    with open('mqtt_logs.txt', 'a') as f:
        f.write(log_line + "\n")
    if len(logs) >= 8:
        sys.exit(0)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()
