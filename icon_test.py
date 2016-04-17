import locale
import curses
import icons

# curses color pairs
PAIR_RED = 1
PAIR_GREEN = 2
PAIR_BLUE = 3
PAIR_YELLOW = 4
PAIR_CYAN = 5
PAIR_WHITE = 6
PAIR_BLACK = 7

PAIR_BLACK_BLUE = 8


def initCurses():

    locale.setlocale(locale.LC_ALL, '')

    # init curses interface
    stdscr = curses.initscr()

    # colors
    curses.start_color()
    curses.init_pair(PAIR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(PAIR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(PAIR_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(PAIR_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(PAIR_CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(PAIR_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(PAIR_BLACK, curses.COLOR_BLACK, curses.COLOR_BLACK)

    curses.init_pair(PAIR_BLACK_BLUE, curses.COLOR_BLACK, curses.COLOR_BLUE)

    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0)  # no cursor

    return stdscr


def endCurses():
    # terminate curses application
    curses.nocbreak()
    curses.echo()
    stdscr.keypad(0)
    curses.endwin()


if __name__ == '__main__':
    stdscr = initCurses()

    x = 0
    y = 0

    for icon in icons.brokenClouds, icons.clear, icons.default, icons.fewClouds, icons.mist, icons.rain,icons.scatteredClouds, icons.snow, icons.storm:
        icons.drawIcon(x,y, icon, stdscr)
        x = x + icons.iconWidth + 1
        if x > 50:
            x = 0
            y = y + icons.iconHeight + 1

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
    endCurses()
