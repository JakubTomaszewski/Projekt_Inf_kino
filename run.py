from load_save_data import get_csv_data, save_csv_data, FileError, IncorrectArrayData
from visualisation import show_seats
import curses
from menu import main_menu, TooSmallScreen
import numpy as np


# Setting screen parameters
screen_height = 700
screen_width = 1100

# Row indices as keys and their numeric indices as values
row_indices = {
                'A': 0,
                'B': 1,
                'C': 2,
                'D': 3,
                'E': 4,
                'F': 5,
                'G': 6,
                'H': 7,
                'I': 8,
                'J': 9,
                'K': 10,
                'L': 11,
                'M': 12,
                'N': 13,
                'O': 14,
                'P': 15,
}

# Creating screen for cv2
screen = np.zeros([screen_height, screen_width, 3], np.uint8)


while True:  # loop assures we return to the selecting movies menu
    # Getting the chosen movie from the menu
    try:
        chosen_movie = curses.wrapper(main_menu)
    except TooSmallScreen:
        print('Could not open the menu')
        break
    # If a movie wasn't chosen, break from the loop
    if not chosen_movie:
        break

    # Creating seats array
    try:
        seats_array = get_csv_data(chosen_movie)
        # Showing the cinema hall
        booked_seats_array = show_seats(screen, seats_array, row_indices, chosen_movie, screen_height, screen_width)
    except FileError as e:
        print(f'''An error occurred while loading the file for movie: {e.movie}
({e.inner_exception})''')
        break
    except IncorrectArrayData as e:
        print(f'An error occurred while loading the file for movie: {e.movie}')
        break

    try:
        # Saving the new cinema hall array
        save_csv_data(chosen_movie, booked_seats_array)
    except FileError as e:
        print(f'''An error occurred while saving the file for {e.movie}
({e.inner_exception})''')
        break


