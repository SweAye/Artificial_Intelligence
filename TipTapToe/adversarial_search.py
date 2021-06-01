# ----------------------------------------------------------------------
# Name:     adversarial_search
# Purpose:  Implement adversarial search algorithms
# ----------------------------------------------------------------------
"""
Adversarial search algorithms implementation

Your task for homework 6 is to implement:
1.  minimax
2.  alphabeta
3.  abdl (alpha beta depth limited)
"""
import random
import math  

def rand(game_state):
    """
    Generate a random move.
    :param game_state: GameState object
    :return:  a tuple representing the row column of the random move
    """
    done = False
    while not done:
        row = random.randint(0, game_state.size - 1)
        col = random.randint(0, game_state.size - 1)
        if game_state.available(row,col):
            done = True
    return row, col

def minimax(game_state):
    """
    Find the best move for our AI agent using the minimax algorithm.
    (searching the entire tree from the current game state)
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    moves = game_state.possible_moves()
    if not moves:
        return None
    return max(game_state.possible_moves(), key=lambda move: value(game_state.successor(move, 'AI'), 'user'))

def value(game_state, agent):
    """
    Calculate the minimax value for any state under the given agent's
    control.
    :param game_state: GameState object - state may be terminal or
    non-terminal
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """
    if game_state.is_win('AI'):
        return 1
    if game_state.is_win('user'):
        return -1
    if game_state.is_tie():
        return 0
    if agent is 'AI':
        return max_value(game_state)
    return min_value(game_state)

def max_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent)
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    return max(value(game_state.successor(move, 'AI'), 'user') for move in game_state.possible_moves())

def min_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user)
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    return min(value(game_state.successor(move, 'user'), 'AI') for move in game_state.possible_moves())

def alphabeta(game_state):
    """
    Find the best move for our AI agent using the minimax algorithm
    with alpha beta pruning.
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    moves = game_state.possible_moves()
    if not moves:
        return None
    a = -math.inf
    b = math.inf
    return max(game_state.possible_moves(), key=lambda move: ab_value(game_state.successor(move, 'AI'), 'user', a, b))

def ab_value(game_state, agent, alpha, beta):
    """
    Calculate the minimax value for any state under the given agent's
    control using alpha beta pruning
    :param game_state: GameState object - state may be terminal or
    non-terminal.
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """
    if game_state.is_win('AI'):
        return 1
    if game_state.is_win('user'):
        return -1
    if game_state.is_tie():
        return 0
    if agent is 'AI':
        return abmax_value(game_state, alpha, beta)
    return abmin_value(game_state, alpha, beta)

def abmax_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent) using alpha beta pruning
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    a = alpha
    v = -math.inf
    for move in game_state.possible_moves():
        v = max([v, ab_value(game_state.successor(move, 'AI'), 'user', a, beta)])
        if v >= beta:
            return v
        a = max(a, v)
    return v

def abmin_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user) using alpha beta pruning
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    b = beta
    v = math.inf
    for move in game_state.possible_moves():
        v = min([v, ab_value(game_state.successor(move, 'user'), 'AI', alpha, b)])
        if v <= alpha:
            return v
        b = min([b, v])
    return v

def abdl(game_state, depth):
    """
    Find the best move for our AI agent by limiting the alpha beta
    search the given depth and using the evaluation function
    game_state.eval()
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """

    a = -math.inf
    b = math.inf
    return max(game_state.possible_moves(),
               key=lambda move: abdl_value(game_state.successor(move, 'AI'), 'user', a, b, depth))

def abdl_value(game_state, agent, alpha, beta, depth):
    """
    Calculate the utility for any state under the given agent's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: GameState object - state may be terminal or
    non-terminal
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) utility of that state
    """
   # Replace  terminal utilities with an evaluation function for non - terminal positions
    if game_state.is_win('AI'):
        return max(1, game_state.eval())
        #return max(game_state.successor(move, 'AI').eval() for move in game_state.possible_moves())
    if game_state.is_win('user'):
        return min(-1, game_state.eval())
        #return min(game_state.successor(move, 'AI').eval() for move in game_state.possible_moves())
    if game_state.is_tie():
        return 0
    if depth == 0:
        return game_state.eval()

    if agent == 'AI':
        return abdlmax_value(game_state, alpha, beta, depth)
    return abdlmin_value(game_state, alpha, beta, depth)

def abdlmax_value(game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Max's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    a = alpha
    v = -math.inf
    for move in game_state.possible_moves():
        v = max([v, abdl_value(game_state.successor(move, 'AI'), 'user', a, beta, depth - 1)])
        if v >= beta:
            return v
        a = max(a, v)
    return v

def abdlmin_value( game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Min's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    b = beta
    v = math.inf
    for move in game_state.possible_moves():
        v = min([v, abdl_value(game_state.successor(move, 'user'), 'AI', alpha, b, depth - 1)])
        if v <= alpha:
            return v
        b = min([b, v])
    return v
