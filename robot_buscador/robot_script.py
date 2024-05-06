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

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S4)

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

inicialx=6
inicialy=0

recogidax=3
recogiday=4

entregax=4
entregay=5



#Valores de prueba

inicialx=6
inicialy=0

recogidax=3
recogiday=4

entregax=4
entregay=5


for i in range(0, len(map_string), 10):  
    fila = []
    for j in range(i, i+10, 2): 
        fila.append(int(map_string[j:j+2]))
    map_data.append(fila)

# Define function to find path using A* algorithm

def movimiento(inix, iniy, objx, objy):
    if(objx < inix): #Movimiento hacia arriba
        robot.drive(280,0)
        robot.brake()
        inix=inix-1
        return map_data[inix-1][iniy]
    
    if(objy > iniy):
        robot.turn(90)
        robot.drive(280,0)
        robot.brake()
        iniy=iniy-1
        return map_data[inix][iniy+1]
    
    if(objy < iniy):
        robot.turn(360)
        robot.drive(280,0)
        robot.brake()
        iniy=iniy-1
        return map_data[inix][iniy+1]
        
    if(objx > inix):
        robot.turn(270)
        robot.drive(280,0)
        robot.brake()
        inix=inix-1
        return map_data[inix+1][iniy]




while True:
    mqtt_client.wait_msg()
    while(inicialx != recogidax and inicialy != recogiday):
        movimiento(inicialx,inicialy,recogidax,recogiday)
    while(inicialx != entregax and inicialy != entregay):
        movimiento(inicialx,inicialy,entregax,entregay)
    
    