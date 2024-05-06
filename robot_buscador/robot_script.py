#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
import ujson
import time
import umqtt.robust as mqtt
import math

# Initialize the motors
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)

# Initialize the drive base
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# MQTT settings
broker_address = "192.168.48.245"
broker_port = 1883
topic_map_send = "A3-467/grupoN/send_package"

# MQTT Client Setup
mqtt_client = mqtt.MQTTClient("robot", broker_address, port=broker_port)

def move_directly(objx, objy):
    # Assuming global variables for the robot's current position
    global pos_robot_x, pos_robot_y
    dx = objx - pos_robot_x
    dy = objy - pos_robot_y
    distance = math.sqrt(dx**2 + dy**2)
    angle = math.degrees(math.atan2(dy, dx))
    robot.turn(angle)
    robot.straight(distance * 280)  # Assuming 280 is the scale for each unit in your grid system
    pos_robot_x, pos_robot_y = objx, objy
def on_message(self, client, userdata, msg):
    try:
        payload = msg.decode("utf-8")  # Assuming message is byte array
        pickup, delivery = payload.split(";")
        pickup_row, pickup_col = map(int, pickup.split(","))
        delivery_row, delivery_col = map(int, delivery.split(","))
        move_directly(pickup_row, pickup_col)  # Move robot to pickup
        move_directly(delivery_row, delivery_col)  # Move robot to delivery
    except Exception as e:
        print("Error on message: ", str(e))

# Connect to the MQTT broker
mqtt_client.set_callback(on_message)
mqtt_client.connect()
mqtt_client.subscribe(topic_map_send)

# Initial robot position
pos_robot_x, pos_robot_y = 0, 0

try:
    while True:
        mqtt_client.check_msg()  # Check for new messages
        time.sleep(1)  # Sleep to prevent excessive CPU usage
except KeyboardInterrupt:
    print("Exiting...")
    mqtt_client.disconnect()