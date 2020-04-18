import time
import curses
from meta_data import get_movie_titles


def display_menu(stdscr, selected_row_idx):
    '''Displays all the movies'''
    # Clear the screen
    stdscr.clear()
    # Getting the screen size
    height, width = stdscr.getmaxyx()
    # Printing some info on the screen
    stdscr.addstr(2, 1, 'DOSTĘPNE FILMY:')
    stdscr.addstr(height - 2, 1, 'Aby wyjsc nacisnij ESC')
    # Printing each movie on the screen
    for i, row in enumerate(movie_list):
        x = width//2 - len(row)//2
        y = height//2 - len(movie_list)//2 + i  # Starting from the center
        if i == selected_row_idx:
            # Choosing the color pair 1 and turning it on
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    # Refreshing screen
    stdscr.refresh()


def main_menu(stdscr):
    '''Creates an interactive menu with movies'''
    curses.curs_set(0)
    # Initializing a color pair
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # background color, foreground color
    current_row_idx = 0

    # Showing the menu
    display_menu(stdscr, current_row_idx)

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
        elif key == curses.KEY_ENTER or key in [10, 13]:  # if Enter key, the movie has been chosen
            chosen_movie = movie_list[current_row_idx]
            stdscr.addstr(0, 0, f'Wybrany film to: "{chosen_movie}"')
            stdscr.refresh()
            # Displaying the window for 2 seconds
            time.sleep(2)
            # Returning the chosen movie
            return chosen_movie
        elif key == 27:  # The ESC key
            break

        display_menu(stdscr, current_row_idx)
        stdscr.refresh()


url = 'https://gist.githubusercontent.com/tiangechen/b68782efa49a16edaf07dc2cdaa855ea/raw/0c794a9717f18b094eabab2cd6a6b9a226903577/movies.csv'

# Getting an array of movie titles
movie_list = get_movie_titles(url)
# print(movie_list)
