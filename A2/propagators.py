#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''
pruneList = []

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

############################################################################
def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    '''
    Input:
        csp: a constraint satisfication problem containing variables, constraints, etc
        newVar: a variable object
    Ouput:
        Boolen: True for solution, False for deadend
        pruneList: a list containing tuples (Var, value), values that had been pruned
    '''
    global pruneList
    pruneList = []
    #get previous assignments
    assignment = []
    Clist = []
    if newVar != None:
        Cons = csp.get_cons_with_var(newVar)
        for c in Cons:
            if c.get_n_unasgn() == 1:
                Clist.append(c)
        for C in Clist:
            assignment = [var.get_assigned_value() for var in C.get_scope()]
            V = C.get_unasgn_vars()[0]
            #get V index
            for i in range(len(assignment)):
                if assignment[i] == V.get_assigned_value():
                    index = i
            for d in V.cur_domain():
                assignment[index] = d
                if not C.check(assignment):
                    V.prune_value(d)
                    if (V,d) not in pruneList:
                        pruneList.append((V,d))
            if V.cur_domain() == []:
                return False, pruneList
        return True, pruneList

    elif newVar == None:
        Cons = csp.get_all_cons()
        for c in Cons:
            if c.get_n_unasgn() == 1:
                V = c.get_unasgn_vars()[0]
                assignment = [var.get_assigned_value() for var in c.get_scope()]
                #get V index
                for i in range(len(assignment)):
                    if assignment[i] == None:
                        index = i
                if index == None:
                    index = V.value_index()
                for d in V.cur_domain():
                    assignment[index] = d
                    if not c.check(assignment):
                        V.prune_value(d)
                        if (V,d) not in pruneList:
                            pruneList.append((V,d))
                if V.cur_domain() == []:
                    return False, pruneList
        return True, pruneList

###########################################################################
def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    '''
    Input:
        csp: a constraint satisfication problem containing variables, constraints, etc
        newVar: a variable object
    Ouput:
        Boolen: True for solution, False for deadend
        pruneList: a list containing tuples (Var, value), values that had been pruned
    '''
    global pruneList
    GACQueue = []
    pruneList = []

    if newVar != None:
        for c in csp.get_cons_with_var(newVar):
            GACQueue.append(c)

    elif newVar == None:
        for c in csp.get_all_cons():
            GACQueue.append(c)

    while len(GACQueue) != 0:
        C = GACQueue.pop(0) #FIFO
        for V in C.get_scope():
            for d in V.cur_domain():
                if findAssignment(C,V,d) == False:
                    V.prune_value(d)
                    pruneList.append((V, d))
                    if V.cur_domain() == []:
                        GACQueue.clear()
                        #V.restore_curdom()
                        return False, pruneList
                    else:
                        for CC in csp.get_cons_with_var(V):
                            if CC not in GACQueue:
                                GACQueue.append(CC)
    return True, pruneList

def findAssignment(C,V,d):
    '''
    Input:
        C: a constraint
        V: a variable
        d: a value
    Ouput:
        is_found: if any support is found return True, false otherwise
    '''
    is_found = False
    for A in C.get_scope():
        if A != V:
            if C.has_support(V,d) == True:
                is_found = True
    return is_found

##################################################################################
def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    #IMPLEMENT
    temp = {}
    for v in csp.get_all_unasgn_vars():
        temp[v] = v.cur_domain_size()
    #print(temp)
    rval = sorted(temp.items(), key=lambda x:x[1])
    #return the variable that has the least remaining values
    if rval != []:
        return rval[0][0]
    else:
        return None
###################################################################################
def printVarVal(csp):
    '''for printing the results after processing, for debugging'''
    for i in csp.get_all_vars():
        print(i,i.cur_domain())
