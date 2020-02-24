#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os  # for time functions
from search import *  # for search engines
# for Sokoban specific classes and problems
from sokoban import SokobanState, Direction, PROBLEMS


table = {}
boxstate = {}
allObstacles = []
def sokoban_goal_state(state):
    '''
    @return: Whether all boxes are stored.
    '''
    for box in state.boxes:
        if box not in state.storage:
            return False
    return True


def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.

    rval = 0
    for box in state.boxes:
        min_dist = state.width * state.height
        if box not in state.storage:
            for storage in state.storage:
                dist = abs(box[0] - storage[0]) + abs(box[1] - storage[1])
                if dist < min_dist:
                    min_dist = dist
        rval += min_dist
    return rval


# SOKOBAN HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    count = 0
    for box in state.boxes:
        if box not in state.storage:
            count += 1
    return count


def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.

    global table
    global boxstate
    global allObstacles

    if state.action == "START":
        table = {}
        boxstate = {}
        allObstacles = []
        #Combining obstacles with the outer wall
        for x in range (-1,state.width):
            allObstacles.append((x,-1))
            allObstacles.append((x,state.height))
        for x in range (-1,state.height):
            allObstacles.append((-1,x))
            allObstacles.append((state.width,x))
        for i in state.obstacles:
            allObstacles.append(i)
        state.print_state()
    if state.hashable_state() in table:
        return float("inf")
    else:
        table[state.hashable_state()] = 1 #for cycle checking

    # #prevent robot from moving repeatitively
    # if state.parent is not None:
    #     if state.parent.parent is not None:
    #         if state.boxes == state.parent.boxes:
    #             if state.robots == state.parent.parent.robots:
    #                 return float("inf")
    if str(set(state.boxes)) in boxstate:
        if state.boxes == state.parent.boxes:
            return boxstate[str(set(state.boxes))] + len(state.boxes)
        return boxstate[str(set(state.boxes))]


    else:
        rval = 0

        #Creating an array of mannhaten distances between boxes and storage spaces
        for box in state.boxes:
            temp_storage = []
            temp_robot = []
            #Checking cases where boxes are in the corner which is not a storage site
            if isCorner(state, box, allObstacles) is True: return float("inf")
            #if checkEdge(state, box, allObstacles) is True: return float("inf")
            for storage in state.storage:
                temp_storage.append(abs(box[0] - storage[0]) + abs(box[1] - storage[1]))
            rval = rval + min(temp_storage)

        # for robot in state.robots:
        #     for box in state.boxes:
        #         temp_robot.append(abs(robot[0] - box[0]) + abs(robot[1] - box[1]))
        #     rval = rval + 0.5*min(temp_robot)

        boxstate[str(set(state.boxes))] = rval

    return rval

def isCorner(state, box, allObstacles):
    #if the thing (robot or box) is surrounded by obstacles, the herustic cost for moving that thing should be large
    x = box[0]
    y = box[1]
    up, down, left, right = (x, y-1), (x, y+1), (x-1, y), (x+1, y)

    #check if the box is at a corner
    if up in allObstacles and left in allObstacles and box not in state.storage:
        return True
    if up in allObstacles and right in allObstacles and box not in state.storage:
        return True
    if down in allObstacles and left in allObstacles and box not in state.storage:
        return True
    if down in allObstacles and right in allObstacles and box not in state.storage:
        return True
    return False

def checkEdge(state, box, allObstacles):
    # Check if box is either at the leftmost or rightmost wall, and check if storage is not along that wall
    if box in state.storage: return False

    else:
        for storage in state.storage:
            if ((box[0] == 0) or (box[0] == state.width - 1)) and (box[0] - storage[0] == 0):
                return False
    # Check if box is either at the topmost or bottommost wall, and check if storage is not along that wall
            elif ((box[1] == state.height - 1) or (box[1] == 0)) and (box[1] - storage[1] == 0):
                return False
    return True

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.

    fval = sN.gval + weight * sN.hval

    return fval


def anytime_weighted_astar(initial_state, heur_fn, weight=1.5, timebound=8):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    #Set time timebound
    time = os.times()[0]
    endtime = time + timebound
    new_timebound = timebound
    weight = 10
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    search = SearchEngine(strategy='custom', cc_level='full')
    search.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)

    costbound = (float("inf"),float("inf"),float("inf"))
    best_result = False
    #keep track of number of iterations
    #iter = 0
    while time < endtime:
        result = search.search(new_timebound, costbound)
        time_elapsed = os.times()[0] - time
        time = os.times()[0]
        new_timebound = new_timebound - time_elapsed
        if result is not False:
            if result.gval< costbound[0]:
                costbound = (result.gval, result.gval, result.gval) #we only care aboud gval when doing best first search.[0] = gval, [1] = hval, [2] = fval = gval+hval
                best_result = result
        else:
            break

    return best_result

    return False


def anytime_gbfs(initial_state, heur_fn, timebound=8):
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    #Set time timebound
    time = os.times()[0]
    endtime = time + timebound
    new_timebound = timebound

    #wrapped_fval_function = (lambda sN: fval_function(sN, 1))
    #cc = default, cyclechecking is on and = FULL
    search = SearchEngine(strategy = 'best_first', cc_level = 'full')
    search.init_search(initial_state, sokoban_goal_state, heur_fn)#only the

    #init the costbound with infinity
    costbound = (float("inf"),float("inf"),float("inf"))
    best_result = False

    while time < endtime:
        result = search.search(new_timebound, costbound)
        time_elapsed = os.times()[0] - time
        time = os.times()[0]
        new_timebound = new_timebound - time_elapsed
        #prune nodes that have higher gvals
        if result is not False:
            if result.gval < costbound[0]:
                costbound = (result.gval, result.gval, result.gval) #we only care aboud gval when doing best first search.[0] = gval, [1] = hval, [2] = fval = gval+hval
                best_result = result
        else:
            break
    return best_result
