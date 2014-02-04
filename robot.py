from sr import *

import movements
from math import sin, cos, atan, radians, degrees, sqrt

def compute_directions(marker, d=1):
    """
    The function provides neccesary information to line up for marker
    'd' metres away from it

    Returns angle 'gamma'(radians) for robot to turn
    and move 'distance'meters forward to get 1m in front of the token
    and angle to turn towards the marker when it stops moving

    This function assumes angles are positive when marker is to the left
    of the robot and is turned away from it anti-clockwise

    """
    alpha = radians(marker.rot_y)
    beta = radians(marker.orientation.rot_y)
    X = marker.dist * sin(alpha)
    Y = marker.dist * cos(alpha)
    x = X - d*sin(beta)
    y = Y - d*cos(beta)
    gamma = atan(x / y)
    distance = sqrt(x*x+ y*y)
    return distance, gamma, alpha - gamma

def main():
    robot = Robot()
    markersInSight = robot.see()
    while markersInSight == []:
        movements.turn(robot)
        markersInSight = robot.see()

    marker = markersInSight[0]
    distance, angle1, angle2 = compute_directions(marker)

    movements.turn(robot, angle1)
    movements.move_straight(robot, distance)
    movements.turn(robot, angle2)

main()