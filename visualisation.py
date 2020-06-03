import cv2
from os import system
from time import sleep
import numpy as np
from load_save_data import IncorrectArrayData, IncorrectShape, FileError


class IncorrectlyChosenSeats(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def display_chosen_seats(chosen_seats):
    '''Prints the chosen seats'''
    if chosen_seats is None:
        print('No seats have been chosen')
        return
    try:
        print('Chosen seats: ')
        for seat in chosen_seats:
            if len(seat) != 2:
                raise IncorrectlyChosenSeats('Incorrect seats format, required (row, place)')
            # Print the row and place
            print(f'Row {seat[0]} Place {seat[1]}')
    except (ValueError, TypeError):
        raise IncorrectlyChosenSeats('Incorrect chosen seats array')


def get_num_places():
    '''Assures the inserted number of places is an integer'''
    try:
        num_places = int(input('How many places you want to book?: '))
        if num_places < 0:
            raise ValueError
        return num_places
    except ValueError:
        print('The number of places to book has to be a positive integer!')
        sleep(2)
        return get_num_places()


def say_goodbye():
    '''Says goodbye and destroys the image windows'''
    print('See you next time!!')
    sleep(2)
    # If the reservation is correct destroy the window
    cv2.destroyAllWindows()
    # Clear the screen
    system('cls')


def finalize_booking(places_array: list):
    '''Prints thank you, destroys all image windows, summarizes the booking process'''
    # If the reservation is correct destroy the window
    cv2.destroyAllWindows()
    # Clear the screen
    system('cls')
    try:
        print('Thank you for your reservation :)')
        display_chosen_seats(places_array)  # display the chosen seats
    except IncorrectlyChosenSeats:
        raise
    sleep(2)
    system('cls')


def get_row():
    pass


def book_seats(seats_array: list, row_indices, num_places):
    '''Books seats for the movie'''

    # Creating ann array for the chosen places
    places = []
    i = 1  # Seat number for customer's information
    while len(places) != num_places:  # while num_places aren't correctly chosen
        print(f'Choosing {i} place')
        # If place is not taken:
        row = input('Row: ').strip().upper()
        # Row has to be in dict keys and can't be larger than the cinema hall array size
        if (row in row_indices.keys()) and (row_indices[row] < seats_array.shape[0]):
            try:
                place = int(input('Place number: '))
                if (place >= 1) and (place <= seats_array.shape[1]):  # place has to be between 1 and 30
                    # Checking if the seat is not taken
                    if seats_array[row_indices[row], place - 1] == 0:
                        seats_array[row_indices[row], place - 1] = 1
                        # if the choice is correct add the seat to the chosen seats list, thus increase its length
                        places.append((row, place))
                        i += 1
                    elif seats_array[row_indices[row], place - 1] == 1:
                        print('This place is already taken!\nPlease choose another one')
                        continue
                    else:
                        raise IncorrectArrayData('Incorrect array, should contain zeros and ones')
                else:
                    raise ValueError  # raise the value error - place has to be an int from 1 to 30
            except ValueError:  # place has to be an int from 1 to 30
                print(f'The place number has to be a positive integer between 1 and {seats_array.shape[1]}!')
        else:  # incorrect row
            print('Incorrect row!')

    # Finalize the booking
    try:
        finalize_booking(places)
        return seats_array  # returns a modified array
    except IncorrectlyChosenSeats:
        print('Could not book the seats')


def display_text_info(scr, movie: str, font, seats_array: np.ndarray, margin_x):
    '''Displays the movie title and number of taken seats'''
    try:
        taken_seats = int(seats_array.sum())  # getting all the taken seats
        screen_with_text = scr.copy()  # making a copy of the screen array

        # Display title
        screen_with_text = cv2.putText(screen_with_text, movie, (margin_x, 35), font, 0.7, (255, 255, 255), 1)
        # Display taken places
        screen_with_text = cv2.putText(screen_with_text, f'Seats taken: {taken_seats}', (margin_x, 60), font, 0.7, (255, 255, 255), 1)
        return screen_with_text  # return the screen with text info added
    except ValueError:
        raise IncorrectArrayData('Incorrect data type in array, numeric required', movie)


def create_square(screen, square_x_first, square_y_first, square_x_second, square_y_second, color, space):
    '''Creates a square representing one place'''
    new_screen = cv2.rectangle(screen, (space + square_x_first, space + square_y_first),
                               (square_x_second, square_y_second), color, -1)
    return new_screen


def display_row_indices(screen, font, row_indices, j: int, margin_x, margin_y):
    '''Displays the j row index'''
    try:
        new_screen = cv2.putText(screen, f'{tuple(row_indices.keys())[j]}', (margin_x - 10, margin_y - 20 + 37 * (j + 1)),
                                 font, 0.5, (255, 255, 255), 1)
        return new_screen
    except IndexError:
        raise IncorrectShape('Incorrect array shape, too many rows')


def display_key_info(screen, font, margin_x, screen_height):
    '''Adds text info on the screen about the ESC and ENTER keys'''
    # Adding text how to escape
    new_screen = cv2.putText(screen, 'Press ESC to exit', (margin_x, screen_height - 7),
                             font, 0.5, (255, 255, 255), 1)
    # Adding text how to book seats
    new_screen = cv2.putText(screen, 'Press ENTER to book places', (margin_x, screen_height - 27),
                             font, 0.5, (255, 255, 255), 1)
    return new_screen


def display_screen(screen, font, margin_x, screen_width):
    '''Draws a blue rectangle and displays info about the screen location in the cinema hall'''
    # Adding a blue rectangle at the screen top - movie screen
    new_screen = cv2.rectangle(screen, (margin_x, 0),
                               (screen_width - margin_x, 12), (255, 0, 0), -1)
    # Adding a movie screen description
    new_screen = cv2.putText(screen, 'SCREEN', (screen_width//2, 10), font, 0.4,
                             (255, 255, 255), 1)
    return new_screen


def create_row(row: np.ndarray, j: int, screen, font, margin_x, margin_y, space):
    '''Creates a seats row made of squares'''
    # Setting square (each place) parameters
    square_height = 35
    square_width = 25
    
    for i, seat in enumerate(row):
        # Setting square position parameters
        square_x_first = margin_x + square_width * i
        square_y_first = margin_y + square_height * j
        square_x_second = margin_x + square_width * (i + 1)
        square_y_second = margin_y + square_height * (j + 1)

        # Setting col label (seat numbers)
        if j == 0:
            new_screen = cv2.putText(screen, f'{i + 1}', (square_x_first + 5, square_y_first - 5),
                                     font, 0.5, (255, 255, 255), 1)
        if seat == 0:
            # creating a green square
            new_screen = create_square(screen, square_x_first, square_y_first, square_x_second, square_y_second, (0, 255, 0), space)
        else:
            # creating a red square
            new_screen = create_square(screen, square_x_first, square_y_first, square_x_second, square_y_second, (0, 0, 255), space)


def display_image(movie: str, screen, seats_param: np.ndarray, row_indices):
    '''Displays the cinema hall image with seats'''
    while True:
        # Showing the cinema hall image
        cv2.imshow(f'Seats for {movie}', screen)
        # Getting the pressed key
        key = cv2.waitKey(0) & 0xFF
        if key == 27:  # if the pressed key is ESC exit, destroy the window and break the loop
            cv2.destroyAllWindows()
            break
        elif key in (10, 13):  # if ENTER key - start the booking
            try:
                # if the cinema hall array is not full
                if seats_param.sum() != (seats_param.shape[0] * seats_param.shape[1]):
                    print('Proceeding to place booking')

                    # Get the number of places to book
                    num_places = get_num_places()
                    if num_places == 0:
                        say_goodbye()
                        return

                    # get_row(seats_param, row_indices)
                    # get_seat(seats_param)
                    return book_seats(seats_param, row_indices, num_places)  # return the new array with chosen seats
                else:
                    print('No available places for this movie :(')
                    sleep(2)
                    cv2.destroyAllWindows()
                    return
            except ValueError:
                raise IncorrectArrayData('Incorrect data type in array, numeric required', movie)
            except IncorrectArrayData:
                raise


def show_seats(scr, seats_param: np.ndarray, row_indices, movie: str, screen_height, screen_width):
    '''Displays the cinema hall with all places'''
    if movie is None:  # if the move wasn't chosen
        return

    # Setting screen parameters
    margin_x = screen_height // 5
    margin_y = 120
    space = 6

    new_screen = scr.copy()  # making a copy of the screen array
    # Setting a font
    font = cv2.FONT_HERSHEY_DUPLEX

    try:
        # Creating a square for each seat in a row
        for j, row in enumerate(seats_param):
            # Adding row indices
            new_screen = display_row_indices(new_screen, font, row_indices, j, margin_x, margin_y)

            # Adding text how to exit and how to book seats
            new_screen = display_key_info(new_screen, font, margin_x, screen_height)

            # Creates a row
            create_row(row, j, new_screen, font, margin_x, margin_y, space)
    except IncorrectShape as e:
        raise FileError('Array shape does not match row indices', e, movie)

    # Show the screen
    display_screen(new_screen, font, margin_x, screen_width)

    try:
        # Displaying text info on the screen
        new_screen = display_text_info(new_screen, movie, font, seats_param, margin_x)

        # Returning chosen seats or None if the pressed key was ESC (exit from the seat booking section)
        return display_image(movie, new_screen, seats_param, row_indices)
    except IncorrectArrayData:
        raise
