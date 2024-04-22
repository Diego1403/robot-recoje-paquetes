import paho.mqtt.client as mqtt

# MQTT broker credentials
broker_address = "192.168.78.10"
broker_port = 1883
client_id = "your_client_id" # Change this to a unique identifier for your client
username = "" # If authentication is required, provide username
password = "" # If authentication is required, provide password

# Callback function to handle MQTT connection
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    # Subscribe to the map topic
    client.subscribe("map")
    

# Callback function to handle MQTT message reception
def on_message(client, userdata, msg):
    if msg.topic == "map":
        map_data = msg.payload.decode("utf-8") # Decode the received map data
# Process the received map data (decode the map structure, update robot's internal map, etc.)
        print("Received map data:", map_data)

# Create MQTT client instance
client = mqtt.Client(client_id=client_id)

# Set MQTT username and password if authentication is required
if username and password:
    client.username_pw_set(username, password)

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker_address, broker_port)

# Start MQTT network loop
client.loop_forever()