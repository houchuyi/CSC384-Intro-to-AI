from cspbase import *
from propagators import *
import itertools
from futoshiki_csp import *
from random import *
from pprint import pprint


# 教授没给 Test cases 那就自己来

def solve_futo(model, board, propType, trace=False, var_ord=None):
    csp, var_array = model(board)
    solver = BT(csp)
    if trace:
        solver.trace_on()
    if propType == 'BT':
        solver.bt_search(prop_BT, var_ord)
    elif propType == 'FC':
        solver.bt_search(prop_FC, var_ord)
    elif propType == 'GAC':
        solver.bt_search(prop_GAC, var_ord)

    result = []
    for vars in var_array:
        result.append([])
        for var in vars:
            # print(var.assignedValue, end=" ")
            result[-1].append(var.get_assigned_value())
        # print()
    return result
        

def test_csp_futo(model, board, trace,  var_ord=None, bt_limit=5, fc_limit=9, gac_limit=10):
    n = len(board)
    failed = 0
    if n <= bt_limit:
        print("=======================================================")
        print("Plain Bactracking on futoshiki")
        res=solve_futo(model, board, 'BT', trace, var_ord)
        if verify_result(board, res): print("-- PASS --")
        else: 
            print("-- FAILED --")
            failed += 1
    
    if n <= fc_limit:
        print("=======================================================")
        print("Forward Checking futoshiki")
        res=solve_futo(model, board, 'FC', trace, var_ord)
        if verify_result(board, res): print("-- PASS --")
        else: 
            print("-- FAILED --")
            failed += 1
    
    if n <= gac_limit:
        print("=======================================================")
        print("GAC futoshiki")
        res = solve_futo(model, board, 'GAC', trace, var_ord)
        if verify_result(board, res): print("-- PASS --")
        else: 
            print("-- FAILED --")
            failed += 1
        print("=======================================================")
    return failed

def brute_force_fill_boards(board, n, i):
    if i == n * n: return board, True
    x = i // n
    y = i % n
    dom = [v + 1 for v in range(n)]

    # check constraints
    for pi in range(n):
        for pj in range(n):
            if board[pi][pj] == 0: break;
            if (pi == x and pj != y) or (pi != x and pj == y):
                if board[pi][pj] in dom: dom.remove(board[pi][pj])
    
    while len(dom) > 0:
        fill = choice(dom)
        board[x][y] = fill
        new_board, check = brute_force_fill_boards(board, n, i+1)
        if check:
            return new_board, True
        dom.remove(fill)
    return board, False


def generate_random_board(n, n_ineq=-1, n_remain=-1):
    # generate random board with size n x n
    # the result may not be distinct
    board = [[0 for _ in range(n)] for __ in range(n)]
    board, _ = brute_force_fill_boards(board, n, 0)
    print("random_board {0}x{0}\n".format(n))
    pprint(board)

    # generate random inequality
    num_ineq = n * (n - 1) if n_ineq == -1 else n_ineq # ranint(1, n * (n - 1))
    all_tuples = []
    for i in range(n):
        for j in range(n - 1):
            t = (i, j)
            all_tuples.append(t)
    ineq_tuples = set(sample(all_tuples, num_ineq))

    # combine table with ineq
    ineq_board = []
    for i in range(n):
        ineq_board.append([])
        row = ineq_board[-1]
        for j in range(n):
            row.append(board[i][j])
            if j != n - 1:
                ineq = '.'
                if (i, j) in ineq_tuples:
                    ineq = '<' if board[i][j] < board[i][j+1] else '>'
                row.append(ineq)
    print("random_ineq_board:\n")
    pprint(ineq_board)

    # remove random numbers
    num_remain_num = 0 if n_remain == -1 else n_remain # ranint(1, n * (n - 1))
    all_tuples = []
    for i in range(n):
        for j in range(n):
            t = (i, j)
            all_tuples.append(t)
    remain_tuples = set(sample(all_tuples, num_remain_num))
    res_board = ineq_board
    for i in range(n):
        for j in range(n):
            if (i, j) not in remain_tuples:
                res_board[i][j * 2] = 0
    
    print("random_game_board:\n")
    pprint(res_board)
    return res_board


def verify_result(input_board, res_board):
    # check any row, col conflict
    n = len(input_board)

    # for i in range(n):
    #     for j in range(n):
    #         print(res_board[i][j], end=' ')
    #         if j != n-1:
    #             print(input_board[i][j * 2 + 1], end=' ')
    #     print()

    for k in range(n):
        if set(range(1, n + 1)) != set(res_board[k]):
            print("board is conflict at row {}".format(k))
            pprint(res_board[k])
            return False

        col = [r[k] for r in res_board]
        if set(range(1, n + 1)) != set(col):
            print("board is conflict at row {}".format(k))
            pprint(col)
            return False
    
    # check ineq
    for i in range(n):
        for j in range(n - 1):
            sign = input_board[i][j * 2 + 1]
            if sign == '.': continue
            if (sign == '>' and res_board[i][j] < res_board[i][j+1]) or \
               (sign == '<' and res_board[i][j] > res_board[i][j+1]):
                print("Inequality error for res_board[{}][{}]=={} {} res_board[{}][{}]=={} at row {}: {} ".format(
                    i, j, res_board[i][j], sign, i, j+1, res_board[i][j+1], i, res_board[i]
                ))
                return False

    return True

if __name__ == "__main__":
    
    seed(1)
    boards = [
        [[0, '<', 0], [0, '.', 0]],
        generate_random_board(3),
        generate_random_board(4),
        generate_random_board(5, randint(5 * (5 - 1) // 2, 5 * (5 - 1)), randint(int(5 * 5 * 0.5), int(5 * 5 * 0.8))),
        generate_random_board(6, randint(6 * (6 - 1) // 2, 6 * (6 - 1)), randint(int(6 * 6 * 0.5), int(6 * 6 * 0.8))),
        generate_random_board(7, -1, 26),
        generate_random_board(8, -1, 32),
        generate_random_board(9, -1, 30),
        # generate_random_board(7, randint(7 * (7 - 1) // 2, 7 * (7 - 1)), randint(7 * 7 // 4, 7 * 7 // 2)),
        # generate_random_board(8, randint(8 * (8 - 1) // 2, 8 * (8 - 1)), randint(8 * 8 // 4, 8 * 8 // 2)),
        # generate_random_board(9, randint(9 * (9 - 1) // 2, 9 * (9 - 1)), randint(9 * 9 // 4, 9 * 9 // 2)),
    ]

    #trace = True
    trace = False
    failed = 0
    fail_baords = []
    for board in boards:
        
        _failed = 0
        print("New board size={}".format(len(board)))
        pprint(board)

        print("futoshiki_csp_model_1 Without mrv_var:")
        _failed += test_csp_futo(futoshiki_csp_model_1, board, trace)
        print("\n")

        print("futoshiki_csp_model_1 With mrv_var:")
        _failed += test_csp_futo(futoshiki_csp_model_1, board, trace, ord_mrv)
        print("\n")

        if (len(board) > 8): continue
        print("futoshiki_csp_model_2 Without mrv_var:")
        _failed += test_csp_futo(futoshiki_csp_model_2, board, trace, fc_limit=6)
        print("\n")

        print("futoshiki_csp_model_2 With mrv_var:")
        _failed += test_csp_futo(futoshiki_csp_model_2, board, trace, ord_mrv, fc_limit=6)
        print("\n")

        if _failed > 0:
            fail_baords.append(board)
            failed += _failed

    if failed == 0:
        print("ALL PASSED")
    else:
        print("FAILED {} times".format(failed))
        for b in fail_baords:
            pprint(b)