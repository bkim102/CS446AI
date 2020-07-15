
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.

        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """

    min_list = []
    max_list = []
    maze2D = []
    arm_num = len(Arm.getArmLimit(arm))
    print("in transformToMaze")
    # print(arm_num)

    for i in range(arm_num):
        # print(i)
        # print(Arm.getArmLimit(arm)[i][0])    
        min_list.append(Arm.getArmLimit(arm)[i][0])
        max_list.append(Arm.getArmLimit(arm)[i][1])
        # print(max_list)
    if(arm_num == 1):
        alpha_start = Arm.getArmAngle(arm)
        # print(max_list)
        for alpha in range(min_list[0], max_list[0] + 1, granularity):
            
            if True == Arm.setArmAngle(arm, [alpha]):
                # print(goals)
                print(alpha)
                if alpha_start[0] == alpha:
                    maze2D.append(START_CHAR)
                    print("saving start at ", alpha_start[0])
                elif False==isArmWithinWindow(Arm.getArmPos(arm), window):
                    maze2D.append(WALL_CHAR)
                    print("wall")
                elif doesArmTouchObstacles(Arm.getArmPos(arm), obstacles):
                    maze2D.append(WALL_CHAR)
                    print("obs")
                elif doesArmTouchGoals(Arm.getArmPos(arm)[-1][-1], goals):
                    print("goal")
                    maze2D.append(OBJECTIVE_CHAR)
                elif doesArmTouchObstacles(Arm.getArmPos(arm), goals):
                    print("goalovershoot")
                    maze2D.append(WALL_CHAR)

                else:
                    maze2D.append(SPACE_CHAR)
                    print("void")
            else:
                maze2D.append(WALL_CHAR)
        maze_construct= Maze(maze2D, [min_list[0]], granularity, 1)
        # Maze.setStart(maze_construct, (alpha_start))


    if(arm_num == 2):
        alpha_start, beta_start = Arm.getArmAngle(arm)
        for alpha in range(min_list[0], max_list[0] + 1, granularity):
            row_list = []
            for beta in range(min_list[1], max_list[1] + 1, granularity):
                if True == Arm.setArmAngle(arm, (alpha, beta)):
                    if alpha_start == alpha and beta_start == beta:
                        row_list.append(START_CHAR)
                        print("saving start at ", alpha_start, beta_start)
                    elif False==isArmWithinWindow(Arm.getArmPos(arm), window):
                        row_list.append(WALL_CHAR)
                    elif doesArmTouchObstacles(Arm.getArmPos(arm), obstacles):
                        row_list.append(WALL_CHAR)
                    elif doesArmTouchGoals(Arm.getArmPos(arm)[-1][-1], goals):
                        row_list.append(OBJECTIVE_CHAR)
                    elif doesArmTouchObstacles(Arm.getArmPos(arm), goals):
                        row_list.append(WALL_CHAR)
                    else:
                        row_list.append(SPACE_CHAR)
                else:
                    row_list.append(WALL_CHAR)
            maze2D.append(row_list)
        maze_construct= Maze(maze2D, [min_list[0], min_list[1]], granularity, 2)
        # Maze.setStart(maze_construct, (alpha_start, beta_start))


    if(arm_num == 3):
        alpha_start, beta_start, gamma_start = Arm.getArmAngle(arm)  
        print(alpha_start, beta_start, gamma_start )
        print(min_list, max_list)
        # x = 0
        for alpha in range(min_list[0], max_list[0] + 1, granularity):
        # for alpha in range(1):
            # print(alpha)
            
            row_list = []
            # for beta in range(1):
            # y = 0
            for beta in range(min_list[1], max_list[1] + 1, granularity):
                
                level_list = []
                # for gamma in range(1):
                # z = 0
                for gamma in range(min_list[2], max_list[2]+1, granularity):
                    if True == Arm.setArmAngle(arm, (alpha, beta, gamma)):
                        if alpha_start == alpha and beta_start == beta and gamma_start == gamma:
                            level_list.append(START_CHAR)
                            print("saving start at ", alpha_start, beta_start, gamma_start)
                        elif False==isArmWithinWindow(Arm.getArmPos(arm), window):
                            # if x== 30 and  y == 40:
                                # print("oob")
                            level_list.append(WALL_CHAR)
                        elif doesArmTouchObstacles(Arm.getArmPos(arm), obstacles):
                            level_list.append(WALL_CHAR)
                            # if x== 30 and  y == 40:
                                # print("obs")
                        elif doesArmTouchGoals(Arm.getArmPos(arm)[-1][-1], goals):
                            level_list.append(OBJECTIVE_CHAR)
                            # if x== 30 and  y == 40:
                                # print("goal")
                        elif doesArmTouchObstacles(Arm.getArmPos(arm), goals):
                            level_list.append(WALL_CHAR)
                            # if x== 30 and  y == 40:
                                # print("touch goal")
                        else:
                            level_list.append(SPACE_CHAR)
                            # if x== 30 and  y == 40:
                                # print("void")
                    else:
                        level_list.append(WALL_CHAR)
                    # z += 1 
                        # print(z)
                        # print ("a",level_list[2], "a")
                    
                row_list.append(level_list)
                # print(x,y,z)

                # y += 1
            maze2D.append(row_list)
            # x += 1
        # print(maze2D[30][40])
        maze_construct= Maze(maze2D, [min_list[0], min_list[1], min_list[2]], granularity, 3)
        # Maze.setStart(maze_construct, (alpha_start, beta_start))




    return maze_construct
