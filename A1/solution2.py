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
#IMPLEMENT
    '''a better sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    cost = 0
    if check_corners(state): return float("inf")
    cost += robot_beside_nothing(state)
    cost += distance(state)
    return cost

def distance(state):
  final_cost = 0
  robot_distance = float("inf")
  robot_position = state.robot
  for box in state.boxes:
    possible_storage = get_possible_storage(box, state)
    tempcost = []
    old_cost = float("inf")
    for possible in possible_storage:
      if box == possible:
        old_cost = 0
        break
      else:
        new_cost = calculate_simple_distance(box, possible, state)
        if new_cost <= old_cost:
          old_cost = new_cost
    final_cost +=old_cost
    if box not in possible_storage:
      final_cost += get_closeness(box,state)
      new_robot_distance = calculate_simple_distance(robot_position, box, state)
      if new_robot_distance<robot_distance:
        robot_distance = new_robot_distance
  if robot_distance != float("inf"):
    final_cost += robot_distance
  return final_cost

def get_closeness(box, state):
  cost = 0
  top = get_top(box)
  if top in state.obstacles: cost+=1
  if out_bound(top,state): cost+=1
  bottom = get_bottom(box)
  if bottom in state.obstacles: cost+=1
  if out_bound(bottom,state): cost+=1
  left = get_left(box)
  if left in state.obstacles: cost+=1
  if out_bound(left,state): cost+=1
  right = get_right(box)
  if right in state.obstacles: cost+=1
  if out_bound(right,state): cost+=1
  return cost

def out_bound(box, state):
  if box[0] <0: return True
  if box[1] <0: return True
  if box[0] >=state.width: return True
  if box[1] >=state.height: return True
  return False

def get_top(box):
  return (box[0],box[1]+1)
def get_bottom(box):
  return (box[0],box[1]-1)
def get_left(box):
  return (box[0]-1,box[1])
def get_right(box):
  return (box[0]+1,box[1])

def robot_beside_nothing(state):
  robot_position = state.robots
  cost = 0
  if (robot_position[0]+1, robot_position[1])  in state.boxes:
    test = (robot_position[0]+2, robot_position[1]) in state.boxes
    if test in state.boxes or test in state.obstacles:
      cost+= 2
    else:
      return cost
  if (robot_position[0]-1, robot_position[1])  in state.boxes:
    test = (robot_position[0]-2, robot_position[1]) in state.boxes
    if test in state.boxes or test in state.obstacles:
      cost+= 2
    else:
      return cost
  if (robot_position[0], robot_position[1]+1)  in state.boxes:
    test = (robot_position[0], robot_position[1]+2) in state.boxes
    if test in state.boxes or test in state.obstacles:
      cost+= 2
    else:
      return cost
  if (robot_position[0], robot_position[1]-1)  in state.boxes:
    test = (robot_position[0], robot_position[1]-2) in state.boxes
    if test in state.boxes or test in state.obstacles:
      cost+= 2
    else:
      return cost
  cost+=1
  if (robot_position[0]+1, robot_position[1]+1)  in state.boxes: return cost
  if (robot_position[0]-1, robot_position[1]-1)  in state.boxes: return cost
  if (robot_position[0]-1, robot_position[1]+1)  in state.boxes: return cost
  if (robot_position[0]+1, robot_position[1]-1)  in state.boxes: return cost
  return cost+2

def calculate_simple_distance(box, possible,state):
  return abs(box[0]-possible[0])+ abs(box[1]-possible[1])

def is_cornered(position, state):
  if position[0] == 0:
    if position[1] == 0: return True
    if position[1] == state.height-1: return True
    if (position[0], position[1]-1) in state.obstacles: return True
    if (position[0], position[1]+1) in state.obstacles: return True
    return False
  if position[0] == state.width-1:
    if position[1] == 0: return True
    if position[1] == state.height-1: return True
    if (position[0]-1, position[1]) in state.obstacles: return True
    if (position[0]+1, position[1]) in state.obstacles: return True
    return False
  testabove = (position[0]-1, position[1])
  testbelow = (position[0]+1, position[1])
  testleft = (position[0], position[1]-1)
  testright = (position[0], position[1]+1)
  if testabove in state.obstacles:
    if testleft in state.obstacles: return True
    if testright in state.obstacles: return True
  if testbelow in state.obstacles:
    if testleft in state.obstacles: return True
    if testright in state.obstacles: return True
  return False

def check_corners(state):
  for box in state.boxes:
    if is_cornered(box, state): return True
    # if is_edge(box, possible_storage,state): return True
  return False

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


def anytime_weighted_astar(initial_state, heur_fn, weight=1.5, timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    #Set time timebound
    time = os.times()[0]
    endtime = time + timebound
    new_timebound = timebound
    weight = 0
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    search = SearchEngine(strategy='custom', cc_level='full')
    search.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)

    costbound = (float("inf"),float("inf"),float("inf"))
    best_result = False
    #keep track of number of iterations
    #iter = 0
    while time < endtime:
        # if iter == 0:
        #     result = search.search(new_timebound, costbound)
        #     best_result = result
            #iter += 1
        # else:
        #     if result is not False:
        #         weight = 1.5 - 0.1 * iter
        #         if weight >0:
        #             wrapped_fval_function = (lambda sN: fval_function(sN, weight))
        #             search.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)
        #             result = search.search(new_timebound, costbound)
        #         else:
        #             wrapped_fval_function = (lambda sN: fval_function(sN, 0))
        #             search.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)
        #             result = search.search(new_timebound, costbound)
        result = search.search(new_timebound, costbound)
        time_elapsed = os.times()[0] - time
        time = os.times()[0]
        new_timebound = new_timebound - time_elapsed
        if result is not False:
            if result.gval < costbound[0]:
                costbound = (result.gval, result.gval, result.gval) #we only care aboud gval when doing best first search.[0] = gval, [1] = hval, [2] = fval = gval+hval
                best_result = result
        else:
            break

    return best_result

    return False


def anytime_gbfs(initial_state, heur_fn, timebound=10):
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
    search = SearchEngine(strategy = 'best_first', cc_level = 'default')
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
