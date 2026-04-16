import json
import uuid

def gen_id():
    return str(uuid.uuid4())

broker_id = gen_id()
tab_id = gen_id()
ui_tab_id = gen_id()
ui_group_id = gen_id()

flow = [
    {
        "id": tab_id,
        "type": "tab",
        "label": "Pub/Sub Smart Home",
        "disabled": False,
        "info": ""
    },
    {
        "id": broker_id,
        "type": "mqtt-broker",
        "name": "HiveMQ Public",
        "broker": "broker.hivemq.com",
        "port": "1883",
        "clientid": "antigravity_" + gen_id()[:8],
        "autoConnect": True,
        "usetls": False,
        "protocolVersion": "4",
        "keepalive": "60",
        "cleansession": True,
        "birthTopic": "",
        "birthQos": "0",
        "birthPayload": "",
        "closeTopic": "",
        "closeQos": "0",
        "closePayload": "",
        "willTopic": "",
        "willQos": "0",
        "willPayload": ""
    },
    {
        "id": ui_tab_id,
        "type": "ui_tab",
        "name": "Smart Home Hub",
        "icon": "dashboard",
        "disabled": False,
        "hidden": False
    },
    {
        "id": ui_group_id,
        "type": "ui_group",
        "name": "Live Data Feed",
        "tab": ui_tab_id,
        "order": 1,
        "disp": True,
        "width": "6",
        "collapse": False
    },
    # Publisher 1: Temperature
    {
        "id": gen_id(),
        "type": "inject",
        "z": tab_id,
        "name": "Temp Trigger",
        "props": [{"p": "payload"}],
        "repeat": "5",
        "crontab": "",
        "once": False,
        "topic": "",
        "payload": "",
        "payloadType": "date",
        "x": 150,
        "y": 100,
        "wires": [["func_temp"]]
    },
    {
        "id": "func_temp",
        "type": "function",
        "z": tab_id,
        "name": "Gen Temperature",
        "func": "msg.payload = (Math.random() * 10 + 20).toFixed(1);\nreturn msg;",
        "outputs": 1,
        "noerr": 0,
        "x": 350,
        "y": 100,
        "wires": [["mqtt_out_temp"]]
    },
    {
        "id": "mqtt_out_temp",
        "type": "mqtt out",
        "z": tab_id,
        "name": "Pub: Temp",
        "topic": "smarthome/sensors/temperature",
        "qos": "0",
        "retain": "false",
        "broker": broker_id,
        "x": 550,
        "y": 100,
        "wires": []
    },
    # Publisher 2: Humidity
    {
        "id": gen_id(),
        "type": "inject",
        "z": tab_id,
        "name": "Hum Trigger",
        "props": [{"p": "payload"}],
        "repeat": "7",
        "crontab": "",
        "once": False,
        "topic": "",
        "payload": "",
        "payloadType": "date",
        "x": 150,
        "y": 160,
        "wires": [["func_hum"]]
    },
    {
        "id": "func_hum",
        "type": "function",
        "z": tab_id,
        "name": "Gen Humidity",
        "func": "msg.payload = Math.floor(Math.random() * 20 + 40);\nreturn msg;",
        "outputs": 1,
        "noerr": 0,
        "x": 350,
        "y": 160,
        "wires": [["mqtt_out_hum"]]
    },
    {
        "id": "mqtt_out_hum",
        "type": "mqtt out",
        "z": tab_id,
        "name": "Pub: Humidity",
        "topic": "smarthome/sensors/humidity",
        "qos": "0",
        "retain": "false",
        "broker": broker_id,
        "x": 550,
        "y": 160,
        "wires": []
    },
    # Publisher 3: Status (Retained Demo)
    {
        "id": gen_id(),
        "type": "inject",
        "z": tab_id,
        "name": "Set Status Online",
        "props": [{"p": "payload"}],
        "repeat": "",
        "crontab": "",
        "once": True,
        "onceDelay": 0.1,
        "topic": "",
        "payload": "Online",
        "payloadType": "str",
        "x": 160,
        "y": 240,
        "wires": [["mqtt_out_status"]]
    },
    {
        "id": "mqtt_out_status",
        "type": "mqtt out",
        "z": tab_id,
        "name": "Pub: Status (QoS 1, Retain)",
        "topic": "smarthome/status",
        "qos": "1",
        "retain": "true",
        "broker": broker_id,
        "x": 420,
        "y": 240,
        "wires": []
    },
    # Subscriber 1: Wildcard Sensors
    {
        "id": "mqtt_in_wildcard",
        "type": "mqtt in",
        "z": tab_id,
        "name": "Sub: Sensors Wildcard (#)",
        "topic": "smarthome/sensors/#",
        "qos": "0",
        "datatype": "auto",
        "broker": broker_id,
        "x": 210,
        "y": 380,
        "wires": [["switch_node", "debug_wildcard"]]
    },
    {
        "id": "debug_wildcard",
        "type": "debug",
        "z": tab_id,
        "name": "Debug: Sensor Logs",
        "active": True,
        "tosidebar": True,
        "console": False,
        "tostatus": False,
        "complete": "true",
        "targetType": "full",
        "x": 450,
        "y": 340,
        "wires": []
    },
    {
        "id": "switch_node",
        "type": "switch",
        "z": tab_id,
        "name": "Route by Topic",
        "property": "topic",
        "propertyType": "msg",
        "rules": [
            {"t": "eq", "v": "smarthome/sensors/temperature", "vt": "str"},
            {"t": "eq", "v": "smarthome/sensors/humidity", "vt": "str"}
        ],
        "checkall": "true",
        "repair": False,
        "outputs": 2,
        "x": 440,
        "y": 380,
        "wires": [["gauge_temp", "chart_temp"], ["gauge_hum"]]
    },
    {
        "id": "gauge_temp",
        "type": "ui_gauge",
        "z": tab_id,
        "name": "Temp Gauge",
        "group": ui_group_id,
        "order": 1,
        "width": 0,
        "height": 0,
        "gtype": "gage",
        "title": "Temperature (°C)",
        "label": "units",
        "format": "{{value}}",
        "min": 0,
        "max": "50",
        "colors": ["#00b500", "#e6e600", "#ca3838"],
        "seg1": "",
        "seg2": "",
        "x": 670,
        "y": 340,
        "wires": []
    },
    {
        "id": "chart_temp",
        "type": "ui_chart",
        "z": tab_id,
        "name": "Temp Chart",
        "group": ui_group_id,
        "order": 2,
        "width": 0,
        "height": 0,
        "label": "Temperature History",
        "chartType": "line",
        "legend": "false",
        "xformat": "HH:mm:ss",
        "interpolate": "linear",
        "nodata": "",
        "dot": False,
        "ymin": "15",
        "ymax": "35",
        "removeOlder": 1,
        "removeOlderPoints": "",
        "removeOlderUnit": "60",
        "cutout": 0,
        "colors": ["#1f77b4", "#aec7e8", "#ff7f0e", "#2ca02c", "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5"],
        "x": 670,
        "y": 380,
        "wires": [[]]
    },
    {
        "id": "gauge_hum",
        "type": "ui_gauge",
        "z": tab_id,
        "name": "Hum Gauge",
        "group": ui_group_id,
        "order": 3,
        "width": 0,
        "height": 0,
        "gtype": "donut",
        "title": "Humidity (%)",
        "label": "units",
        "format": "{{value}}",
        "min": 0,
        "max": "100",
        "colors": ["#00b500", "#e6e600", "#ca3838"],
        "seg1": "",
        "seg2": "",
        "x": 670,
        "y": 420,
        "wires": []
    },
    # Subscriber 2: Status
    {
        "id": "mqtt_in_status",
        "type": "mqtt in",
        "z": tab_id,
        "name": "Sub: Status (Retained Demo)",
        "topic": "smarthome/status",
        "qos": "1",
        "datatype": "auto",
        "broker": broker_id,
        "x": 220,
        "y": 500,
        "wires": [["text_status", "debug_status"]]
    },
    {
        "id": "debug_status",
        "type": "debug",
        "z": tab_id,
        "name": "Debug: Status",
        "active": True,
        "tosidebar": True,
        "console": False,
        "tostatus": False,
        "complete": "payload",
        "targetType": "msg",
        "x": 440,
        "y": 460,
        "wires": []
    },
    {
        "id": "text_status",
        "type": "ui_text",
        "z": tab_id,
        "group": ui_group_id,
        "order": 4,
        "width": 0,
        "height": 0,
        "name": "System Status",
        "label": "Status",
        "format": "{{msg.payload}}",
        "layout": "row-spread",
        "x": 440,
        "y": 500,
        "wires": []
    }
]

with open('flows.json', 'w') as f:
    json.dump(flow, f, indent=2)

print("flows.json created.")

