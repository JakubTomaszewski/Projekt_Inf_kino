import time
import curses

movie_list = ['A WIĘC WOJNA', 'ABRAHAM LINCOLN: ŁOWCA WAMPIRÓW', 'ABSOLUTNIE FANTASTYCZNE: FILM', 'ACH ŚPIJ KOCHANIE', 'AD ASTRA', 'ADOLF H. JA WAM POKAŻĘ', 'ADRENALINA 2. POD NAPIĘCIEM', 'ADWOKAT', 'AFONIA I PSZCZOŁY', 'AFTER', 'AGENCI', 'AGENT I PÓŁ']


def display_menu(stdscr, selected_row_idx):
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
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < (len(movie_list) - 1):
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]: #  Enter key
            chosen_movie = movie_list[current_row_idx]
            stdscr.addstr(0, 0, f'Wybrany film to: "{chosen_movie}"')
            stdscr.refresh()
            # Displaying the window for 2 seconds
            time.sleep(2)
            # Returning the chosen movie
            return chosen_movie
        elif key == 27: #  The ESC key
            break

        display_menu(stdscr, current_row_idx)
        stdscr.refresh()


# def main(stdscr):
#     # Disabling the cursor blinking
#     curses.curs_set(0)
#     # Initializing a color pair
#     curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)  # background color, foreground color
#
#     height, width = stdscr.getmaxyx()
#     text = 'Hello!'
#
#     # Setting window size
#     x = width//2 - len(text)//2
#     y = height//2
#
#     # Choosing the color pair 1 and turning it on
#     stdscr.attron(curses.color_pair(1))
#     # Adding text to our window
#     stdscr.addstr(y, x, text)
#     # Turning off the color pair
#     stdscr.attroff(curses.color_pair(1))
#     # Refreshing the window
#     stdscr.refresh()
#     # Displaying the window for 3 seconds
#     time.sleep(3)

# chosen_movie = curses.wrapper(main_menu)
# print(chosen_movie)