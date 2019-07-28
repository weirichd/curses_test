import numpy as np

import curses
import time

PLAY_WIDTH = 20
PLAY_HEIGHT = 35
O_COLOR = 1
I_COLOR = 2
T_COLOR = 3
Z_COLOR = 4
S_COLOR = 5
J_COLOR = 6
L_COLOR = 7
BORDER_COLOR = 8


tetrominoes = [
    np.array([[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    np.array([[0, 0, 2, 0], [0, 0, 2, 0], [0, 0, 2, 0], [0, 0, 2, 0]]),
    np.array([[0, 0, 3, 0], [0, 3, 3, 3], [0, 0, 0, 0], [0, 0, 0, 0]]),
    np.array([[0, 4, 4, 0], [0, 0, 4, 4], [0, 0, 0, 0], [0, 0, 0, 0]]),
    np.array([[0, 0, 5, 5], [0, 5, 5, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    np.array([[0, 6, 0, 0], [0, 6, 6, 6], [0, 0, 0, 0], [0, 0, 0, 0]]),
    np.array([[0, 0, 0, 7], [0, 7, 7, 7], [0, 0, 0, 0], [0, 0, 0, 0]]),
]


def init_colors():
    curses.init_pair(BORDER_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(O_COLOR, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(I_COLOR, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(T_COLOR, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(Z_COLOR, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(S_COLOR, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(J_COLOR, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(L_COLOR, curses.COLOR_BLACK, curses.COLOR_CYAN)


def draw_boarder(window):
    window.addstr(4, 10, "TETRIS - Press Q to quit")

    window.addstr(6, 6, "+" + "-" * PLAY_WIDTH + "+", curses.color_pair(BORDER_COLOR))
    window.addstr(7 + PLAY_HEIGHT, 6, "+" + "-" * PLAY_WIDTH + "+", curses.color_pair(BORDER_COLOR))
    for i in range(7, 7 + PLAY_HEIGHT):
        window.addstr(i, 6, "|", curses.color_pair(BORDER_COLOR))
        window.addstr(i, 6 + PLAY_WIDTH + 1, "|", curses.color_pair(BORDER_COLOR))


def draw_tetras(window):
    for j in range(7):
        for i in np.ndindex(tetrominoes[1].shape):
            window.addstr(i[1] + 10 + j*4, i[0] + 10, " ", curses.color_pair(tetrominoes[j][i]))


def board_run(stdscr):
    stdscr.nodelay(True)
    init_colors()

    go = True

    while(go):
        # Update
        c = stdscr.getch()
        if c == ord('q'):
            go = False

        # Render
        stdscr.clear()

        draw_boarder(stdscr)
        draw_tetras(stdscr)

        stdscr.refresh()

        # Sleep
        time.sleep(.1)


if __name__ == '__main__':
    curses.wrapper(board_run)
