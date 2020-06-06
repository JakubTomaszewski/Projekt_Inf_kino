'''
Menu Module
-----------

Module allows to create an interactive menu with movies
'''


import time
import curses


class TooSmallScreen(Exception):
    def __init__(self, message):
        super().__init__('Too small screen')


def display_menu(stdscr, selected_row_idx: int, movie_list):
    '''Displays all the movies on the stdscr menu

    Parameters
    ----------
    :param stdscr: curses.initscr()
        a window object representing the entire screen
    :param selected_row_idx: int
        index of a selected row
    :param movie_list: list, tuple
        array or tuple containing movie titles

    Raises
    ------
    :raises: TooSmallScreen:
        if curses.error occurs (if the screen is to small)
    :raises IndexError:
        if IndexError occurs
    '''

    # Clear the screen
    stdscr.clear()
    # Getting the screen size
    height, width = stdscr.getmaxyx()
    # Printing some info on the screen
    stdscr.addstr(2, 1, 'AVAILABLE FILMS:')
    stdscr.addstr(height - 2, 1, 'Press ESC to exit')
    # Printing each movie on the screen
    try:
        for i, row in enumerate(movie_list):
            # Setting movie title position
            x = width//2 - len(row)//2
            y = height//2 - len(movie_list)//2 + i  # Starting from the center
            if i == selected_row_idx:
                # Choosing the color pair 1 and turning it on
                stdscr.attron(curses.color_pair(1))
                # Printing movie title
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
    except curses.error:
        raise TooSmallScreen('The screen is too small')
    except IndexError:
        raise

    # Refreshing screen
    stdscr.refresh()


def main_menu(stdscr, movie_list):
    '''Creates an interactive menu with movies

    Parameters
    ----------
    :param stdscr: curses.initscr()
        a window object representing the entire screen
    :param movie_list: list, tuple
        array or tuple containing movie titles

    Returns
    -------
    :returns: str
        the chosen movie or returns None if ESC has been pressed

    Raises
    ------
    :raises TooSmallScreen:
        if display_menu() raised TooSmallScreen exception
    :raises IndexError
        if display_menu() raised IndexError exception
    '''

    curses.curs_set(0)
    # Initializing a color pair
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # background color, foreground color
    current_row_idx = 0

    # Checking if the movie list exists and if it contains any movies
    if len(movie_list) != 0 and movie_list is not None:
        try:
            # Displaying the menu
            display_menu(stdscr, current_row_idx, movie_list)
        except (TooSmallScreen, IndexError):
            raise
    else:
        print('No movies available :(')
        return

    # Display the available options
    while True:
        # Taking input from the user
        key = stdscr.getch()
        # Clearing the screen
        stdscr.clear()
        if key == curses.KEY_UP and current_row_idx > 0:  # go up
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < (len(movie_list) - 1):  # go down
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in {10, 13}:  # if Enter key, the movie has been chosen
            chosen_movie = movie_list[current_row_idx]
            stdscr.addstr(0, 0, f'The chosen movie is: "{chosen_movie}"')
            stdscr.refresh()
            # Displaying the window for 2 seconds
            time.sleep(2)
            # Returning the chosen movie
            return chosen_movie
        elif key == 27:  # The ESC key
            return  # returning None if the ESC key is pressed

        # Displaying the menu
        display_menu(stdscr, current_row_idx, movie_list)
        stdscr.refresh()  # refreshing the screen
