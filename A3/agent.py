"""
An AI player for Othello.

The game ends as soon as one of the players has no legal moves left.

The current player and the current disks on the board.
Throughout our implementation, Player 1 (dark) is represented using the integer 1, and Player 2 (light) is
represented using the integer 2.
"""

import random
import sys
import time

#global var for Caching
have_seen_this_before = {}


# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT
    (dark, light) = get_score(board)
    if color == 1: #dark
        return dark - light
    if color == 2: #light
        return light - dark
    else:
        return False

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT

    return compute_utility(board, color) #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    #IMPLEMENT
    max_color = color
    min_color = 3-color
    if caching == 1:
        if board in have_seen_this_before:
            return ([],have_seen_this_before[board])
    if get_possible_moves(board, min_color) == []:
        if not board in have_seen_this_before:
            have_seen_this_before[board] = compute_utility(board,max_color)
        return ([], compute_utility(board, max_color))
    if limit == 0:
        if not board in have_seen_this_before:
            have_seen_this_before[board] = compute_heuristic(board,max_color)
        return ([], compute_heuristic(board, max_color))
    if limit == -1:
        limit = limit
    else:
        limit = limit -1
    infinity = float('inf')
    minval = infinity
    suc_boards = []
    for m in get_possible_moves(board, min_color):
        suc_boards.append((play_move(board, min_color, m[0],m[1]),m))
    for state,m in suc_boards:
        a = minval
        minval = min(minval, minimax_max_node(state, max_color, limit, caching)[1])
        if a!= minval:
            move = m
    if not board in have_seen_this_before:
        have_seen_this_before[board] = minval
    return (move, minval)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT
    if caching == 1:
        if board in have_seen_this_before:
            return ([],have_seen_this_before[board])
    if get_possible_moves(board, color) == []:
        if not board in have_seen_this_before:
            have_seen_this_before[board] = compute_utility(board,color)
        return ([], compute_utility(board, color))
    if limit == 0:
        if not board in have_seen_this_before:
            have_seen_this_before[board] = compute_heuristic(board,color)
        return ([], compute_heuristic(board, color))
    if limit == -1:
        limit = limit
    else:
        limit = limit - 1
    infinity = float('inf')
    maxval = -infinity
    suc_boards = []
    for m in get_possible_moves(board, color):
        suc_boards.append((play_move(board, color, m[0],m[1]),m))
    for state,m in suc_boards:
        a = maxval
        maxval = max(maxval, minimax_min_node(state, color, limit, caching)[1])
        if a != maxval: #if maxval changed, we store the move
            move = m
    if not board in have_seen_this_before:
        have_seen_this_before[board] = maxval
    return (move,maxval)

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    #IMPLEMENT
    if get_possible_moves(board, color) == None or limit == 0:
        return ([],compute_utility(board,color))

    #Apply player's moves to get successor states
    #always max
    global have_seen_this_before
    (move,maxval)= minimax_max_node(board, color, limit, caching)

    return move #change this!

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    max_color = color
    min_color = 3-color
    if caching == 1:
        if board in have_seen_this_before:
            return ([],have_seen_this_before[board])
    if get_possible_moves(board, min_color) == []:
        if not board in have_seen_this_before:
            have_seen_this_before[board] = compute_utility(board,max_color)
        return ([],compute_utility(board,max_color))
    if limit == 0:
        if not board in have_seen_this_before:
            have_seen_this_before[board] = compute_heuristic(board,max_color)
        return ([],compute_heuristic(board,max_color))
    if limit == -1:
        limit = limit
    else:
        limit = limit - 1
    infinity = float('inf')
    val = infinity
    suc_boards = []
    move = []
    for m in get_possible_moves(board,min_color):
        new_board = play_move(board,min_color,m[0],m[1])
        suc_boards.append((new_board,m,compute_utility(new_board,max_color)))
    if ordering == 1:
        suc_boards = sorted(suc_boards, key=lambda x:x[2])
    for state,m,disks in suc_boards:
        a = val
        val = min(val, alphabeta_max_node(state,max_color,alpha, beta, limit, caching)[1])
        if val <= alpha:
            return (m,val)
        beta = min(beta, val)
        if a != val:
            move = m
    if not board in have_seen_this_before:
        have_seen_this_before[board] = val
    return (move,val)
    

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    if caching == 1:
        if board in have_seen_this_before:
            return ([],have_seen_this_before[board])
    if get_possible_moves(board, color) == []:
        if not board in have_seen_this_before:
            have_seen_this_before[board] = compute_utility(board,color)
        return ([],compute_utility(board,color))
    if limit == 0:
        if not board in have_seen_this_before:
            have_seen_this_before[board] = compute_heuristic(board,color)
        return ([],compute_heuristic(board, color))
    if limit == -1:
        limit = limit
    else:
        limit = limit - 1
    infinity = float('inf')
    val = -infinity
    suc_boards = []
    move = []
    for m in get_possible_moves(board,color):
        suc_boards.append((play_move(board,color,m[0],m[1]),m,compute_utility(play_move(board,color,m[0],m[1]),color)))
    if ordering == 1:
        suc_boards = sorted(suc_boards, key=lambda x:x[2])

    for state,m,disks in suc_boards:
        a = val
        val = max(val, alphabeta_min_node(state,color,alpha, beta, limit,caching)[1])
        if val >= beta:
            return (m,val)
        alpha = max(alpha, val)
        if a != val:
            move = m
    if not board in have_seen_this_before:
        have_seen_this_before[board] = val
    return (move,val)


def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    #IMPLEMENT
    if get_possible_moves(board, color) == None or limit == 0:
        return compute_utility(board,color)
    global have_seen_this_before
    infinity = float('inf')
    bestval = -infinity
    beta = infinity
    suc_boards = []
    for m in get_possible_moves(board,color):
        suc_boards.append((play_move(board,color,m[0],m[1]),m))
    for state, m in suc_boards:
        move, value = alphabeta_min_node(state, color, bestval, beta, limit-1, caching)
        if value > bestval:
            bestval = value
            bestmove = m

    return bestmove #change this!

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
    # board = ((0,0,0,0),(0,2,1,0),(0,1,2,0),(0,0,0,0))
    # select_move_alphabeta(board,1,-1,0,1)
