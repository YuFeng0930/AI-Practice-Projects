"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0

    for r in range(3):
        for c in range(3):
            if board[r][c] == X:
                count_x += 1
            elif board[r][c] == O:
                count_o += 1
    
    if count_x == count_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # (row, cell) is legal move if its position on the board is currently empty
    legal_actions = set()
    for row in range(3):
        for cell in range(3):
            if board[row][cell] == EMPTY:
                legal_actions.add((row, cell))

    return legal_actions
    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Illegal aciton")
    
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for cur_player in [O, X]:
        # Row
        for i in range(3):
            if board[i][0] == cur_player and board[i][1] == cur_player and board[i][2] == cur_player:
                return cur_player

        # Column
        for i in range(3):
            if board[0][i] == cur_player and board[1][i] == cur_player and board[2][i] == cur_player:
                return cur_player

        # Diagonal
        if board[0][0] == cur_player and board[1][1] == cur_player and board[2][2] == cur_player:
                return cur_player
        elif board[0][2] == cur_player and board[1][1] == cur_player and board[2][0] == cur_player:
                return cur_player

    return None

        
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    end = True
    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                end = False
                break
    
    return end


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    cur_player = player(board)

    if cur_player == X:
        v = - math.inf
        for action in actions(board):
            max_v = min_value(result(board, action))
            if max_v > v:
                optimal_move = action
                v = max_v
        return optimal_move

    elif cur_player == O:
        v = math.inf
        for action in actions(board):
            min_v = max_value(result(board, action))
            if min_v < v:
                optimal_move = action
                v = min_v
        return optimal_move


def max_value(board):
    if terminal(board):
        return utility(board)
    v = - math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v