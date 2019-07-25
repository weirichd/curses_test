import numpy as np

import curses
import time


def spill_matrix(i, j, size):
    result = np.zeros(size, dtype=int)

    for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        try:
            ind = i + d[0], j + d[1]
            result[ind] = 1
        except Exception:
            pass

    result[i,j] = -4

    return result


def spill_piles(sandpile):
    while sandpile.max() > 3:
        for index, s in np.ndenumerate(sandpile):
            if s > 3:
                sandpile = sandpile + spill_matrix(*index, sandpile.shape)
    return sandpile


def render_board(board, window):
    for i in np.ndindex(board.shape):
        screen_pos = i[0] + 3, i[1] + 5
        b = board[i]
        window.addstr(*screen_pos, '{}'.format(b), curses.color_pair(b + 1))


def board_run(stdscr):
    stdscr.nodelay(True)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    board = np.zeros((15, 15), dtype=int)
#   Uncomment the next line to use a random matrix to start with
#    board = np.random.randint(0, 2, size=(15, 15))

    go = True

    while(go):
        # Update
        c = stdscr.getch()
        if c == ord('q'):
            go = False

        board[7, 7] = board[7, 7] + 1
        board = spill_piles(board)

        # Render
        stdscr.clear()

        stdscr.addstr(1, 5, "Sandpiles. Press Q to quit")

        render_board(board, stdscr)

        stdscr.refresh()

        # Sleep
        time.sleep(.1)


if __name__ == '__main__':
    curses.wrapper(board_run)
