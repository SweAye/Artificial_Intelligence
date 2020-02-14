# ----------------------------------------------------------------------
# Name:     sudoku
# Purpose:  Sudoko puzzle solver with Backtracking search and AC-3 Algorithm
# ----------------------------------------------------------------------
import csp # a private proprietary dependent class

def get_constrains(neighbors):
    """
    Create the constrains function for CSP.
    :param neighbors: the neighbors of a CSP problem, a dictionary
        representing binary constraints.
        The dictionary keys are variable names and the values are sets
        containing all the variables that are connected to the key.
        (Variables are connected if they both appear in a constraint)
    :return:  a function that takes as arguments two variables
        and two values: f(var1, val1, var2, val2).
        The function must return True if var1 and var2 satisfy the
        constraint when their respective values are val1 and val2.
    """
    def constrains(var1, val1, var2, val2):
        if var1 in neighbors[var2] and val1 == val2:
            return False
        else:
            return True
    return constrains

def get_neighbors(variables):
    """
    get the neighbors for a CSP object.
    :param variables: a list of tuples representing all possible combinations in the puzzle.
    :return: a dictionary representing binary constraints.
        The dictionary keys are variable names and the values are sets
        containing all the variables that are connected to the key.
        (Variables are connected if they both appear in a constraint)
    """
    block3 = []
    x = y = [0, 3, 6]
    for i in x:
        l = []
        for j in y:
            l = [(a, b) for a in range(i, i + 3) for b in range(j, j + 3)]
            block3.append(l)

    blocks = [[(a, b) for a in range(0, 9)] for b in range(0, 9)] + [[(a, b) for b in range(0, 9)] for a in
                                                                     range(0, 9)] + block3

    neighbors = {}
    for x in variables:
        nei = set()
        for b in blocks:
            if x in b:
                nei.update(b)
        nei.discard(x)
        neighbors[x] = nei
    return neighbors

def build_csp(puzzle):
    """
    Create a CSP object representing the puzzle.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: CSP object
    """
    # Enter your code here and remove the pass statement below
    variables = [(a,b) for a in range(0,9) for b in range(0,9)]
    domain = {}
    for x in variables:
        if x in puzzle:
            domain[x] = {puzzle[x]}
        else:
            domain[x] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    neighbors = get_neighbors(variables)
    constraint = get_constrains(neighbors)

    mySudoku = csp.CSP(domain, neighbors, constraint)
    return mySudoku

def q1(puzzle):
    """
    Solve the given puzzle with basic backtracking search
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    mysudoku = build_csp(puzzle)
    solution = mysudoku.backtracking_search()
    return solution, mysudoku

def q2(puzzle):
    """
    Solve the given puzzle with backtracking search and AC-3 as
    a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    mysudoku = build_csp(puzzle)
    mysudoku.ac3_algorithm()
    solution = mysudoku.backtracking_search()
    return solution, mysudoku


def q3(puzzle):
    """
    Solve the given puzzle with backtracking search and MRV ordering and
    AC-3 as a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    mysudoku = build_csp(puzzle)
    mysudoku.ac3_algorithm()
    solution = mysudoku.backtracking_search("MRV")
    return solution, mysudoku
