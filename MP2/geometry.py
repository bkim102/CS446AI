# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *



def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position of the arm link, (x-coordinate, y-coordinate)
    """
    start_x, start_y = start
    angle_rad = math.radians(angle)
    x_pos =  math.cos(angle_rad) * length + start_x
    y_pos = start_y - math.sin(angle_rad) * length

    end = (x_pos, y_pos)

    return end



def doesArmTouchObstacles(armPos, obstacles):
    """Determine whether the given arm links touch obstacles

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            obstacles (list): x-, y- coordinate and radius of obstacles [(x, y, r)]

        Return:
            True if touched. False it not.
     """


    for arm_i in armPos:
        arm_start , arm_end = arm_i
        arm_s_x, arm_s_y = arm_start
        arm_e_x, arm_e_y = arm_end

        for obs_i in (obstacles):
            
            obs_x, obs_y, obs_r = obs_i
            
            #function to determine minimum distance between a infinite line and a dot
            
            ca_1 = (arm_e_y - arm_s_y) * obs_x - (arm_e_x - arm_s_x) * obs_y
            ca_2 = arm_e_x * arm_s_y - arm_e_y * arm_s_x
            ca_3 = ((arm_e_y - arm_s_y)**2 + (arm_e_x - arm_s_x)**2)**(0.5)

            dis_from_dot = abs(ca_1 + ca_2) / ca_3
            '''check special case when inf line touches the obstacle but out of arm length
                idea is the closest possible false alarm is when the obstacle is directly tangent 
                to the line on either edge. through pythagorian theorem, if we calculate the distance squared from
                each end to the obstacle summed, then compare with the line length squared, every time when the sum is 
                greater than the line length swuared, it means it was a false alarm.
                '''
            if dis_from_dot <= obs_r:
                #check special case when inf line touches but out of arm length
                #idea is anytime the triangle between the line and the obstacle center is greater than a right triangle,
                #it might trigger a false alarm.
                len_line = (arm_e_x - arm_s_x)**2 + (arm_e_y - arm_s_y)**2
                len_s2o = (arm_s_x - obs_x)**2 + (arm_s_y - obs_y)**2
                len_e2o = (arm_e_x - obs_x)**2 + (arm_e_y - obs_y)**2
                if len_line <= len_e2o + len_s2o:
                    if obs_r >= ((arm_e_x - obs_x)**2 + (arm_e_y - obs_y)**2)**(0.5):
                        return True
                    if obs_r >= ((arm_s_x - obs_x)**2 + (arm_s_y - obs_y)**2 )**(0.5):
                        return True
                        
                else:
                    return True
    return False

def doesArmTouchGoals(armEnd, goals):
    """Determine whether the given arm links touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]

        Return:
            True if touched. False it not.
    """
    pos_x , pos_y = armEnd
    for cur_goal in goals:
        goal_x, goal_y, r = cur_goal
        if ((pos_x - goal_x)**2 + (pos_y - goal_y)**2) <= r**2:
            return True
    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False it not.
    """
    window_x_min = 0
    window_y_min = 0
    window_x_max, window_y_max = window

    for arm in armPos:
        arm_start, arm_end = arm
        arm_s_x, arm_s_y = arm_start
        arm_e_x, arm_e_y = arm_end

        if arm_e_x > window_x_max or arm_s_x > window_x_max or arm_e_y > window_y_max or arm_s_y > window_y_max:
            return False
        if arm_e_x < window_x_min or arm_s_x < window_x_min or arm_e_y <window_y_min or arm_s_y < window_y_min:
            return False
    return True

