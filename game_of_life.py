#!/usr/bin/env python

import itertools


DEAD = False
ALIVE = True
BOARD_SIZE = 4

NEIGHBOR_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def get_neighbors(board, x, y):
    return [{'x': x + xt, 'y': y + yt, 'value': board[x + xt][y + yt]} for (xt,yt) in NEIGHBOR_OFFSETS if BOARD_SIZE > x + xt >= 0 and BOARD_SIZE > y + yt >= 0]


def get_neighbors_by_liveliness(board, x, y, liveliness):
    return [neighbor for neighbor in get_neighbors(board, x, y) if neighbor['value'] == liveliness]


def make_board(x, y, cell_value_fn):
    return [[cell_value_fn(i, j) for j in xrange(y)] for i in xrange(x)]


def next_cell_state(curr_cell_state, live_neighbors_count):
    return curr_cell_state and (live_neighbors_count == 2 or live_neighbors_count == 3) \
        or live_neighbors_count == 3

    
def transition(board):
    # closures
    def next_cell_value_fn(x, y):
        curr_cell_state = board[x][y]
        live_neighbors_count = len(get_neighbors_by_liveliness(board, x, y, ALIVE))
        return next_cell_state(curr_cell_state, live_neighbors_count)

    return make_board(BOARD_SIZE, BOARD_SIZE, next_cell_value_fn)


def game(init_board):
    board = init_board
    while True:
        yield board
        board = transition(board)


def setup_game(seed):
    def seed_fn(x, y):
        return (x, y) in seed

    return game(make_board(BOARD_SIZE, BOARD_SIZE, seed_fn))


def print_board(board):
    for _ in xrange(BOARD_SIZE):
            print('-'),
    for i in xrange(BOARD_SIZE):
        for j in xrange(BOARD_SIZE):
            if board[i][j] == ALIVE:
                print("o"),
            else:
                print(" "),
        print("")

def play_game():
    seed = set([(1,2),(2,2),(3,2)])
    
    g = setup_game(seed)

    generations_count = 10

    for board in itertools.islice(g, generations_count):
        print_board(board)

if __name__ == '__main__':
    play_game()
