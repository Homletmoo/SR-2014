from time import sleep, time
from traceback import print_exc
import math
from sr import Robot

from log import reset_log
from movements import Tracker, turn
from strategy import get_token_from_corner, token_to_slot
        

def main():
    robot = Robot()
    robot.position = Tracker(robot.zone)
    reset_log(robot)

    while 1:
        try:
            token_to_slot(robot, robot.zone)
            zone = 0
            slot = 1
            while slot < 4:
                i = (robot.zone + zone) % 4
                j = (robot.slot + slot) % 4
                if get_token_from_corner(robot, zone):
                    token_to_slot(robot, slot)
                    j += 1
                i += 1
            log(robot, "All slots filled!")
        except:
            print_exc()
            reset_log(robot)
            print '\nRestarting in 2s...\n'
            sleep(2)


main()
