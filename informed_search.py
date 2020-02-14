# ----------------------------------------------------------------------
# Name:     informed_search
# Purpose:  Implement A star algorithm and some heuristics
# ----------------------------------------------------------------------
import data_structures  # a private proprietary dependent class
import math

def astar(problem, heuristic):
    """
    A* graph search algorithm
    returns a solution for the given search problem
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py
    heuristic (a function) the heuristic function to be used
    :return: list of actions representing the solution to the quest
                or None if there is no solution
    """
    closed = set()
    fringe = data_structures.PriorityQueue()
    state = problem.start_state()
    root = data_structures.Node(state)
    fringe.push(root, root.cumulative_cost + heuristic(state, problem))

    while True:
        if fringe.empty():
            return None  # Failure -  no solution was found
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.actions()
        if node.state not in closed:
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                h = heuristic(child_state, problem)
                child_node = data_structures.Node(child_state, node, action)
                child_node.cumulative_cost = node.cumulative_cost + action_cost
                f = child_node.cumulative_cost + h
                fringe.push(child_node, f)

def null_heuristic(state, problem):
    """
    Trivial heuristic to be used with A*.
    Running A* with this null heuristic, gives us uniform cost search
    :param
    state: A state is represented by a tuple containing:
                the current position (row, column) of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: 0
    """
    return 0


def single_heuristic(state, problem):
    """
    Fill in the docstring here
    :param
    state: A state is represented by a tuple containing:
                the current position (row, column) of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest

    :return:
    """
    sammy, metals = state
    if not metals:
        return 0
    return manhattan_distance(sammy,metals[0])


def better_heuristic(state, problem):
    """
    Fill in the docstring here
    :param
    state: A state is represented by a tuple containing:
                the current position (row, column) of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return:
    """
    sammy, metals = state
    if not metals:
        return 0
    goal = metals[0]

    p1_x, p1_y = sammy
    p2_x, p2_y = goal

    if sammy[0] > goal[0]:
        x = problem.cost.get('N')
    if sammy[0] <= goal[0]:
        x = problem.cost.get('S')
    if sammy[1] > goal[1]:
        y = problem.cost.get('W')
    if sammy[1] <= goal[1]:
        y = problem.cost.get('E')

    total = x * abs(p1_x - p2_x) + y * abs(p1_y - p2_y)
    return total

def gen_heuristic(state, problem):
    """
    Fill in the docstring here
    :param
    state: A state is represented by a tuple containing:
                the current position (row, column) of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return:
    """
    '''sammy, metals = state
    if not metals:
        return 0

    p1_x, p1_y = sammy
    total = 0
    metals = sorted(metals, key = lambda x: manhattan_distance(sammy,x))
    for goal in metals:
        if sammy[0] > goal[0]:
            x = problem.cost.get('N')
        if sammy[0] <= goal[0]:
            x = problem.cost.get('S')
        if sammy[1] > goal[1]:
            y = problem.cost.get('W')
        if sammy[1] <= goal[1]:
            y = problem.cost.get('E')

        p2_x, p2_y = goal
        total += x * abs(p1_x - p2_x) + y * abs(p1_y - p2_y)
    return total / len(metals)'''

    sammy, metals = state
    if not metals:
        return 0
    current = sammy
    h=[]
    for goal in metals:
        p1_x, p1_y = current
        p2_x, p2_y = goal

        if sammy[0] > goal[0]:
            x = 4
        if sammy[0] <= goal[0]:
            x = 3
        if sammy[1] > goal[1]:
            y = 1
        if sammy[1] <= goal[1]:
            y = 5

        total = math.sqrt((x * (p1_x - p2_x)) ** 2 + (y * (p1_y - p2_y)) ** 2)
        h.append(total)
    return max(h)

def manhattan_distance(point1, point2):
    """
    Compute the Manhattan distance between two points.
    :param point1 (tuple) representing the coordinates of a point in a plane
    :param point2 (tuple) representing the coordinates of a point in a plane
    :return: (integer)  The Manhattan distance between the two points
    """
    # Enter your code here and remove the pass statement below
    p1_x, p1_y = point1
    p2_x, p2_y = point2
    return abs(p1_x - p2_x) + abs(p1_y - p2_y)