# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

from maze import Maze as mz
from queue import Queue


def solution_refiner(solution, maze):
    filtered = []
    i = len(solution) - 1  #start at end of list
    while i >= 0:
        if solution[i][1] in mz.getObjectives(maze):  #assume for now only one objective
            filtered.append(solution[i][1])
            break
        i -= 1
    key = solution[i][0]
    filtered.append(key)
    i -= 1
    while i >= 0:
        if solution[i][1] == key:
            key = solution[i][0]
            filtered.append(key)
        i -= 1
   # filtered.reverse()
    return filtered

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)

def find_neighbor(maze, cur_pos):
    neighbors =  []
    row, col = cur_pos
    if mz.isValidMove(maze, row-1, col): #UP
        neighbors.append((row-1, col))
    if mz.isValidMove(maze, row+1, col): #DOWN
        neighbors.append((row+1, col))
    if mz.isValidMove(maze, row, col+1): #RIGHT
        neighbors.append((row, col+1))
    if mz.isValidMove(maze, row, col-1): #LEFT
        neighbors.append((row, col-1))
    return neighbors

def bfs(maze):
    bfs_q = Queue()
    bfs_list = []
    visited = []
    path_unrefined = []
    path_refined = []
    objective_list= mz.getObjectives(maze)
    objective_cnt = 0
    bfs_q.put(mz.getStart(maze))
    while bfs_q:
        cur_pos = bfs_q.get()
        visited.append(cur_pos)
        #print("cur_pos:",cur_pos)
        if cur_pos in objective_list:
            objective_list.remove(cur_pos)
        #    print(f"Found objective at: {cur_pos}")
            if not objective_list:
            #    print("all objective visited")
                path_unrefined.append([cur_pos,cur_pos])
                path_refined = solution_refiner(path_unrefined, maze)
                path_refined.reverse()
                return path_refined, len(visited)

        neighbor_list = find_neighbor(maze, cur_pos)
        for next_pos in neighbor_list:
            if next_pos not in visited:
                if next_pos not in bfs_list:
                        bfs_list.append(next_pos)
                        bfs_q.put(next_pos)
                        path_unrefined.append([cur_pos,next_pos])

    # return path, num_states_explored
    return visited, 0


def dfs(maze):
    start_pos = mz.getStart(maze)
    objective_list= mz.getObjectives(maze)

    dfs_s = []
    visited = []
    path_unrefined = []
    path_refined = []

    dfs_s.append(start_pos)
    while dfs_s:
        cur_pos = dfs_s.pop()
        visited.append(cur_pos)
        #print("cur_pos:",cur_pos)
        if cur_pos in objective_list:
            objective_list.remove(cur_pos)
         #   print(f"Found objective at: {cur_pos}")
            if not objective_list:
          #      print("all objective visited")
                path_unrefined.append([cur_pos,cur_pos])
                path_refined = solution_refiner(path_unrefined, maze)
                path_refined.reverse()
                return path_refined, len(visited)

        neighbor_list = find_neighbor(maze, cur_pos)
        for next_pos in neighbor_list:
            if next_pos not in visited:
                dfs_s.append(next_pos)
                path_unrefined.append([cur_pos,next_pos])

    return visited, 0

def sort_neighbor_by_grade(maze, cur_pos, objective_list, neighbor_list):
    neighbor_grade = []
    for neighbor in neighbor_list:
        neigh_row, neigh_col = neighbor
        min_dist = 999999

        for row, col in objective_list:
            man_dist = abs(neigh_row - row) + abs(neigh_col - col)

        neighbor_grade.append(man_dist)

    neighbor_list =  [x for y, x in sorted(zip(neighbor_grade, neighbor_list))]
    neighbor_list.reverse()
    return neighbor_list

def greedy(maze):
    greedy_s = []
    visited = []
    path_unrefined = []
    path_refined = []
    objective_list= mz.getObjectives(maze)
    greedy_s.append(mz.getStart(maze))

    while greedy_s:
        cur_pos = greedy_s.pop()
        visited.append(cur_pos)
        #print("cur_pos:",cur_pos)
        if cur_pos in objective_list:
            objective_list.remove(cur_pos)
            #print(f"Found objective at: {cur_pos}")
            if not objective_list:
                #print("all objective visited")
                path_unrefined.append([cur_pos,cur_pos])
                path_refined = solution_refiner(path_unrefined, maze)
                path_refined.reverse()
                return path_refined, len(visited)

        neighbor_list = find_neighbor(maze, cur_pos)
        neighbor_list = sort_neighbor_by_grade(maze, cur_pos, objective_list, neighbor_list)

        for next_pos in neighbor_list:
            #print("next_pos in stack", next_pos)
            if next_pos not in visited:
                if next_pos not in greedy_s:
                    greedy_s.append(next_pos)
                    path_unrefined.append([cur_pos,next_pos])

    return [], 0

def mapDensity(maze): #for our optimal solution in our nonadmissible heuristic
    rows, cols = mz.getDimensions(maze)
    totalArea = rows * cols
    numWalls = 0
    for col in range(0, cols):
        for row in range(0, rows):
            if mz.isWall(maze, row, col) == True:
                numWalls += 1
    density = float(numWalls/totalArea)
    return density


def astar(maze):
    density = mapDensity(maze)
    #print(f"density: {density}")
    astar_s = []
    visited = []
    path_unrefined = []
    path_refined = []
    total_path = []
    start_pos = mz.getStart(maze)
    objective_list= mz.getObjectives(maze)
    objective_list_dyn = mz.getObjectives(maze)
    start_row, start_col = start_pos
    min_man_dist_0 = 99999999
    total_path.append(start_pos)
    for obj_init in objective_list:
        obj_init_row , obj_init_col = obj_init
        man_dist_0 = abs(start_row - obj_init_row) + abs(start_col - obj_init_col)
        if min_man_dist_0 > man_dist_0:
            min_man_dist_0 = man_dist_0

    astar_s.append((start_pos, 0 , 0 + min_man_dist_0, total_path))
    cur_visited = []
    while astar_s:
        astar_s.sort(key= lambda x:x[2])
        astar_s.reverse()
        cur_pos, g, f, total_path = astar_s.pop()
        cur_visited.append(cur_pos)
        visited.append(cur_pos)
        if cur_pos in objective_list_dyn:
            objective_list_dyn.remove(cur_pos)
            #print(f"Found objective at: {cur_pos}")
            cur_visited[:] = []
            astar_s[:] = []
            if not objective_list_dyn:
                #print("all objective visited")
                #print(total_path)
            #    return visited, len(visited)
                return total_path, len(visited)

        neighbor_list = find_neighbor(maze, cur_pos)
        for next_pos in neighbor_list:
        #    print("next_pos in stack", next_pos)
            if next_pos not in cur_visited:
                if next_pos not in astar_s:
                    neigh_row, neigh_col = next_pos
                    min_h = 9999999
                    for cur_obj in objective_list_dyn:
                        cur_obj_row, cur_obj_col = cur_obj
                        h = abs(neigh_row - cur_obj_row) + abs(neigh_col - cur_obj_col)
                        if h < min_h:
                            min_h = h
                    next_total_path = total_path.copy()
                    next_total_path.append(next_pos)
                    astar_s.append((next_pos, g+1, g+1+min_h, next_total_path))      #COMMENT OUT WHEN USING NONADMISSIBLE HEURISTIC
                    #astar_s.append((next_pos, g+1, g+1+(1 + (20*density)*min_h)))   #EXTRA CREDIT: NONADMISSIBLE HEURISTIC, UNCOMMENT TO ENABLE
                    path_unrefined.append([cur_pos,next_pos])










