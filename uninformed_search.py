# ----------------------------------------------------------------------
# Name:     uninformed_search
# Purpose:  Implement bread first search(BFS) and UCS graph search algorithms
# ----------------------------------------------------------------------
import data_structures # a private proprietary dependent class

def bfs(problem):
    """
    Breadth first graph search algorithm
    returns a solution for the given search problem
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    :return: list of actions representing the solution to the quest
            or None if there is no solution
    """
    closed = set()  # keep track of our explored states
    fringe = data_structures.Queue() # for dfs, the fringe is a queue
    state = problem.start_state()
    root = data_structures.Node(state)
    fringe.push(root)
    while True:
        if fringe.empty():
            return None  # Failure -  no solution was found
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.actions()
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                child_node = data_structures.Node(child_state, node, action)
                fringe.push(child_node)


def ucs(problem):
    """
    Uniform cost first graph search algorithm
    returns a solution for the given search problem
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    :return: list of actions representing the solution to the quest
    """
    closed = set()  # keep track of our explored states
    fringe = data_structures.PriorityQueue() # for ucs, the fringe is a priorityQueue
    state = problem.start_state()
    root = data_structures.Node(state)
    fringe.push(root, root.cumulative_cost)
    while True:
        if fringe.empty():
            return None  # Failure -  no solution was found
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.actions()
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                child_node = data_structures.Node(child_state, node, action)
                child_node.cumulative_cost = node.cumulative_cost + action_cost
                fringe.push(child_node,child_node.cumulative_cost)

