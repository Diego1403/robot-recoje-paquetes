#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
import ujson
import time
import umqtt.robust as mqtt
#from umqtt.robust import MQTTClient


# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)


# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Define the map
map_string = "0202000105030705000200041109060110031000000200080101100110000106010701"
map_data = []


# Function to drive along the path
def drive_along_path(path):
    for node in path:
        row, col = node
        # Convert row and col to x and y coordinates on the map
        x = (col - 1) * 28 + 14
        y = (row - 1) * 28 + 14
        # Drive to the next point on the path
        # Adjust the robot's position based on x and y coordinates
# Deliver package at the second pickup/delivery point

# New part to connect to the server
broker_address = "192.168.48.245"
broker_port = 1883
topic_map = "map"
topic_map_send = "grupoN/send_package"

def add_package(pos_x_recojo, pos_y_recojo, pos_x_destino, pos_y_destino):
    # Add package handling logic here
    print("New package added!")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(topic_map_send)
    else:
        print("Failed to connect to MQTT broker")

def on_message(client, topic, message):
    try:
        payload = ujson.loads(message)
        pos_x_recojo = payload.get("pos_x_recojo")
        pos_y_recojo = payload.get("pos_y_recojo")
        pos_x_destino = payload.get("pos_x_destino")
        pos_y_destino = payload.get("pos_y_destino")
        add_package(pos_x_recojo, pos_y_recojo, pos_x_destino, pos_y_destino)
    except Exception as e:
        print("Error:", e)

mqtt_client = mqtt.MQTTClient("robot", broker_address, port=broker_port)
mqtt_client.set_callback(on_message)
mqtt_client.connect()
mqtt_client.subscribe(topic_map_send)
mqtt_client.set_callback(on_message)


#Valores de prueba

pos_robot_x=0
pos_robot_y=0

recogidax=3
recogiday=4

entregax=4
entregay=5




for i in range(0, len(map_string), 10):  
    fila = []
    for j in range(i, i+10, 2): 
        fila.append(int(map_string[j:j+2]))
    map_data.append(fila)
import math

def move_directly(pos_robot_x, pos_robot_y, objx, objy):

    # Calculate differences in the x and y coordinates
    dx = objx - pos_robot_x
    dy = objy - pos_robot_y
    
    # Calculate the distance using the Pythagorean theorem
    distance = math.sqrt(dx**2 + dy**2)
    
    angle = math.degrees(math.atan2(dy, dx))
    

    robot.turn(angle)
    
    # Move straight to the target
    robot.straight(distance * 280 )  # Assuming 280 is the scale for each unit in your grid system
    
    # Update the current position
    return map_data[objx][objy]

# Example of using the function
while pos_robot_x != recogidax or pos_robot_y != recogiday:
    next_tile = move_directly(pos_robot_x, pos_robot_y, recogidax, recogiday)
    pos_robot_x, pos_robot_y = recogidax, recogiday  # Update position

while pos_robot_x != entregax or pos_robot_y != entregay:
    next_tile = move_directly(pos_robot_x, pos_robot_y, entregax, entregay)
    pos_robot_x, pos_robot_y = entregax, entregay  # Update position