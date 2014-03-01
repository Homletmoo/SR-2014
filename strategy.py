from math import sin, cos, atan, radians, degrees, sqrt, pi
from time import sleep, time

from sr import INPUT_PULLUP

from geometry import Vec2
from position import position_from_zone, compute_directions_for
from movements import move_straight, turn, move_to_point


def scan_corner(robot, zone):
    """
        Checks to see if the robot is near the given zone corner.
        If the robot is not, it is moved there.
        Then, the robot rotates and gather as a list of markers.
    """
    target = Vec2(*position_from_zone(zone, 2.2)[:2])
    if robot.position.dist(target) > 0.5:
        move_to_point(robot, target.x, target.y)
    
    print 'Scanning corner for markers...'
    markers_in_sight = robot.see()
    while not markers_in_sight:
        turn(robot)
        sleep(0.5)
        markers_in_sight = robot.see()
    return markers_in_sight[0]

def line_up_to(marker, robot, dist=0.4):
    """
        Moves the robot dist metres in front of a given marker.
    """
    print 'Lining up to marker:'
    dist, angle1, angle2 = compute_directions_for(marker, d=dist)
    print '    dist=%.2f, angle1=%.2f, angle2=%.2f' % (dist, angle1, angle2)
    turn(robot, angle1)
    sleep(0.75)
    move_straight(robot, dist)
    sleep(0.75)
    turn(robot, angle2)
    
def move_till_touch(robot):
    """
        Moves the robot forward at a constant rate until a
        switch is triggered.
    """
    robot.ruggeduinos[0].pin_mode(11, INPUT_PULLUP)
    touching_marker = lambda: robot.ruggeduinos[0].digital_read(11)
    
    robot.motors[0].m0.power = 30
    robot.motors[0].m1.power = 30
    
    start = time()
    print 'Moving into marker...'
    while not touching_marker(): pass
    print '    marker touched.'
    
    robot.motors[0].m0.power = 0
    robot.motors[0].m1.power = 0
    
    # Update robot.position with distance moved.
    robot.position.move((time() - start) / 5)
    