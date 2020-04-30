from load_save_data import get_csv_data, save_csv_data
from visualisation import show_seats
import curses
from menu import main_menu
import numpy as np


rows = 7
seats = 30


# Setting screen parameters
screen_height = 410
screen_width = 850

# Creating screen for cv2
screen = np.zeros([screen_height, screen_width, 3], np.uint8)


while True:  # loop assures we return to the selecting movies menu
    # Getting the chosen movie from the menu
    chosen_movie = curses.wrapper(main_menu)
    # If a movie wasn't chosen, break from the loop
    if not chosen_movie:
        break

    # Creating seats array
    seats_array = get_csv_data(chosen_movie)

    # Showing the cinema hall
    booked_seats_array = show_seats(screen, seats_array, chosen_movie)

    # Saving the new cinema hall array
    save_csv_data(chosen_movie, booked_seats_array)

