#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary
      all-different constraints for both the row and column constraints.

'''
from cspbase import *
import itertools

'''Transfer the board to a csp, '''

def futoshiki_csp_model_1(futo_grid):
    ##IMPLEMENT

    # Initiallize variables and constraints
    var_array, consList= initVarsCons(futo_grid)

    #make a list of vars
    variables = varList(var_array)

    #initialize csp
    futo_csp = CSP("Futoshiki_1", variables)

    #use itertools and condition funcitons to find satisfying tuples
    #iterate through all Constraints, C = [Constraint, condition]
    cons = []
    for C in consList:
        sat_tuples = []
        if C[1] == '>':
            condition = x_greater_y
        if C[1] == '<':
            condition = x_less_y
        for t in itertools.product(*get_relevant_domain(C[0].get_scope())):
            #NOTICE use of * to convert the list v to a sequence of arguments to product
            if condition(t):
                sat_tuples.append(t)
        C[0].add_satisfying_tuples(sat_tuples)
        cons.append(C[0])

    #Add column and row binary not equal Constraints
    #There are 2n^2 not equal constraints
    colRowCons = initColRowCons(var_array, len(consList))

    for C in colRowCons:
        sat_tuples = []
        for t in itertools.product(*get_relevant_domain(C.get_scope())):
            if x_not_equal_y(t):
                sat_tuples.append(t)
        C.add_satisfying_tuples(sat_tuples)
        cons.append(C)

    #Add constraints to CSP
    for C in cons:
        futo_csp.add_constraint(C)
    return futo_csp, var_array

def futoshiki_csp_model_2(futo_grid):
    ##IMPLEMENT
    # Initiallize variables and constraints
    var_array, consList= initVarsCons(futo_grid)

    #make a list of vars
    variables = varList(var_array)

    #initialize csp
    futo_csp = CSP("Futoshiki_2", variables)

    #use itertools and condition funcitons to find satisfying tuples
    #iterate through all Constraints, C = [Constraint, condition]
    cons = []
    for C in consList:
        sat_tuples = []
        if C[1] == '>':
            condition = x_greater_y
        if C[1] == '<':
            condition = x_less_y
        for t in itertools.product(*get_relevant_domain(C[0].get_scope())):
            #NOTICE use of * to convert the list v to a sequence of arguments to product
            if condition(t):
                sat_tuples.append(t)
        C[0].add_satisfying_tuples(sat_tuples)
        cons.append(C[0])

    allDiffCons = initAllDiffCons(var_array, len(cons))

    #All diff constraints, 2n
    for C in allDiffCons:
        sat_tuples = []
        for t in itertools.product(*get_relevant_domain(C.scope)):
            if allDiff(t):
                sat_tuples.append(t)
        C.add_satisfying_tuples(sat_tuples)
        cons.append(C)

    #Add constraints to CSP
    for C in cons:
        futo_csp.add_constraint(C)
    return futo_csp, var_array

def initVarsCons(board):
    var_array = []
    variables = []
    consList = []
    count = 1
    for i in range(len(board)):
        row = []
        for j in range(len(board[0])):
            #add Variables
            if type(board[i][j]) == int:
                if board[i][j] == 0:
                    row.append(Variable('B'+str(i)+str(j//2), list(range(1,len(board)+1))))
                elif board[i][j] != 0:
                    row.append(Variable('B'+str(i)+str(j//2), [board[i][j]]))
        for j in range(len(board[0])):
            #add constraints
            if type(board[i][j]) == str:
                if board[i][j] != '.':
                    consList.append([Constraint('C'+str(count), [row[j//2], row[(j+1)//2]]), board[i][j]])
                    count = count + 1

        var_array.append(row)
    return var_array, consList

def initColRowCons(var_array, count):
    rcons = []
    count = count + 1
    for row in var_array:
        for i in range(len(row)):
            for j in range(len(row)):
                if j>i:
                    rcons.append(Constraint('C'+str(count), [row[i],row[j]]))
                    count = count + 1
    for col in list(map(list, zip(*var_array))):
        for i in range(len(col)):
            for j in range(len(col)):
                if j>i:
                    rcons.append(Constraint('C'+str(count), [col[i],col[j]]))
                    count = count + 1

    return rcons

def initAllDiffCons(var_array, count):
    rcons = []
    count = count + 1
    for row in var_array:
        rcons.append(Constraint('C'+str(count), [row[i] for i in range(len(row))]))
        count = count + 1
    for col in list(map(list, zip(*var_array))):
        rcons.append(Constraint('C'+str(count), [col[i] for i in range(len(col))]))
        count = count + 1
        
    return rcons

def get_relevant_domain(variables):
    varDoms = []
    for v in variables:
        varDoms.append(v.domain())
        #varDoms.append(list(range(1,n+1)))
    return varDoms

def x_greater_y(xy):
    x = xy[0]
    y = xy[1]
    return (x>y)

def x_less_y(xy):
    x = xy[0]
    y = xy[1]
    return (x<y)

def x_not_equal_y(xy):
    x = xy[0]
    y = xy[1]
    return (x!=y)

def allDiff(x):
    if len(x) > len(set(x)):
        return False
    return True
def varList(var_array):
    rval = []
    for i in range(len(var_array)):
        for j in range(len(var_array)):
            rval.append(var_array[i][j])
    return rval
