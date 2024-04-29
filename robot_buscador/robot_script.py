#!/usr/bin/env pybricks-micropython


from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S4)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Define the map
map_string="0202000105030705000200041109060110031000000200080101100110000106010701"
map_data = []


for i in range(0, len(map_string), 10):  
    fila = []
    for j in range(i, i+10, 2): 
        fila.append(int(map_string[j:j+2]))
    map_data.append(fila)

# Define function to find path using A* algorithm
def find_path(start, end, map_data):
    grid = Grid(matrix=map_data)
    start_node = grid.node(start[1], start[0])
    end_node = grid.node(end[1], end[0])
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, _ = finder.find_path(start_node, end_node, grid)
    return path

# Test run
start = (6, 0)  # Starting position
pickup1 = (4, 3)  # First pickup/delivery point
pickup2 = (2, 5)  # Second pickup/delivery point

# Find path to first pickup/delivery point
path_to_pickup1 = find_path(start, pickup1, map_data)
print("Path to first pickup/delivery point:", path_to_pickup1)

# Find path to second pickup/delivery point
path_to_pickup2 = find_path(pickup1, pickup2, map_data)
print("Path to second pickup/delivery point:", path_to_pickup2)

# Function to drive along the path
def drive_along_path(path):
    for node in path:
        row, col = node
        # Convert row and col to x and y coordinates on the map
        x = (col - 1) * 50 + 25
        y = (row - 1) * 50 + 25
        # Drive to the next point on the path
        # Adjust the robot's position based on x and y coordinates

# Drive along the path to the first pickup/delivery point
drive_along_path(path_to_pickup1)

# Deliver package at the first pickup/delivery point

# Drive along the path to the second pickup/delivery point
drive_along_path(path_to_pickup2)

# Deliver package at the second pickup/delivery point