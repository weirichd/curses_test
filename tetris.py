import numpy as np
import curses
import time

PLAY_WIDTH = 10
PLAY_HEIGHT = 20
O_COLOR = 1
I_COLOR = 2
T_COLOR = 3
Z_COLOR = 4
S_COLOR = 5
J_COLOR = 6
L_COLOR = 7
BORDER_COLOR = 8


# Sprites
tetrominoes = [
    [  # 0
        np.array([[1, 1], [1, 1]])
    ],
    [  # I
        np.array([[0, 0, 2, 0], [0, 0, 2, 0], [0, 0, 2, 0], [0, 0, 2, 0]]),
        np.array([[0, 0, 0, 0], [2, 2, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0]]),
    ],
    [  # T
        np.array([[0, 3, 0], [3, 3, 3], [0, 0, 0]]),
        np.array([[0, 3, 0], [0, 3, 3], [0, 3, 0]]),
        np.array([[0, 0, 0], [3, 3, 3], [0, 3, 0]]),
        np.array([[0, 3, 0], [3, 3, 0], [0, 3, 0]]),
    ],
    [  # Z
        np.array([[4, 4, 0], [0, 4, 4], [0, 0, 0]]),
        np.array([[0, 0, 4], [0, 4, 4], [0, 4, 0]]),
    ],
    [  # S
        np.array([[0, 5, 5], [5, 5, 0], [0, 0, 0]]),
        np.array([[0, 5, 0], [0, 5, 5], [0, 0, 5]]),
    ],
    [  # J
        np.array([[6, 0, 0], [6, 6, 6], [0, 0, 0]]),
        np.array([[0, 6, 6], [0, 6, 0], [0, 6, 0]]),
        np.array([[0, 0, 0], [6, 6, 6], [0, 0, 6]]),
        np.array([[0, 6, 0], [0, 6, 0], [6, 6, 0]]),
    ],
    [  # L
        np.array([[0, 0, 7], [7, 7, 7], [0, 0, 0]]),
        np.array([[0, 7, 0], [0, 7, 0], [0, 7, 7]]),
        np.array([[0, 0, 0], [7, 7, 7], [7, 0, 0]]),
        np.array([[7, 7, 0], [0, 7, 0], [0, 7, 0]]),
    ]
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

    window.addstr(6, 6, "\u250f" + "\u2501" * PLAY_WIDTH + "\u2513", curses.color_pair(BORDER_COLOR))
    window.addstr(7 + PLAY_HEIGHT, 6, "\u2517" + "\u2501" * PLAY_WIDTH + "\u251b", curses.color_pair(BORDER_COLOR))
    for i in range(7, 7 + PLAY_HEIGHT):
        window.addstr(i, 6, "\u2503", curses.color_pair(BORDER_COLOR))
        window.addstr(i, 6 + PLAY_WIDTH + 1, "\u2503", curses.color_pair(BORDER_COLOR))


def draw_tetra(window, piece, position_x, position_y, rotation):
    rotation = rotation % len(tetrominoes[piece])

    for i in np.ndindex(tetrominoes[piece][rotation].shape):
        p = tetrominoes[piece][rotation][i]
        if p != 0:
            window.addstr(
                i[1] + position_y + 7,
                i[0] + position_x + 7,
                "\u2591",
                curses.color_pair(p)
            )


def board_run(stdscr):
    stdscr.nodelay(True)
    init_colors()
    curses.curs_set(0)

    # Initialize Game
    player_x, player_y = 0, 0
    rotation = 0
    current_piece = np.random.randint(7)
    frames_per_step = 10
    current_frame_number = 0

    go = True

    while go:
        # Update

        # Player Input
        c = stdscr.getch()
        if c == ord('q'):
            go = False
        if c == curses.KEY_LEFT:
            player_x = max(0, player_x - 1)  # TODO:  Actual Collision
        if c == curses.KEY_RIGHT:
            player_x = min(PLAY_WIDTH - 4, player_x + 1)  # TODO:  Actual Collision
        if c == curses.KEY_UP:
            rotation = rotation + 1

        # Advance Game State
        current_frame_number = current_frame_number + 1
        if current_frame_number == frames_per_step:
            current_frame_number = 0
            player_y = player_y + 1

        if player_y == PLAY_HEIGHT - 4:   # TODO:  Actual Collision
            player_x, player_y = 0, 0
            current_piece = np.random.randint(7)
            rotation = 0

        # Render
        stdscr.clear()

        draw_boarder(stdscr)
        draw_tetra(stdscr, current_piece, player_x, player_y, rotation)

        stdscr.refresh()

        # Sleep
        time.sleep(.03)


if __name__ == '__main__':
    curses.wrapper(board_run)
