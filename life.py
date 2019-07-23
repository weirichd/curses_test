import numpy as np

import curses
import time


def update_life(X):
    """
    I admit I stole this from somewhere, but ONLY after 
    taking the time to figure out how it works!
    """
    n_neighbors = sum(np.roll(np.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
    return (n_neighbors == 3) | (X & (n_neighbors == 2))


def board_run(stdscr):
    stdscr.nodelay(True)

    board = np.random.randint(0, 2, size=(10, 10))

    go = True

    while(go):
        # Update
        c = stdscr.getch()
        if c == ord('q'):
            go = False

        board = update_life(board)

        # Render
        stdscr.clear()

        for i in np.ndindex(board.shape):
            stdscr.addstr(*i, "{}".format(' ' if board[i] == 0 else '#'))
            stdscr.refresh()

        # Sleep
        time.sleep(1)


if __name__ == '__main__':
    curses.wrapper(board_run)
