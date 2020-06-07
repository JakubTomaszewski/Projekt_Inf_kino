'''
Visualisation Module
--------------------

This module allows:
    -visualisation of a cinema hall for a specific movie
    -booking seats for a specific movie
'''


import cv2
from os import system
from time import sleep
import numpy as np
from load_save_data import IncorrectArrayData, IncorrectShape, FileError, IncorrectArrayType


class IncorrectlyChosenSeats(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class IncorrectFont(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class IncorrectCoordinates(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def display_chosen_seats(chosen_seats=None):
    '''Prints the chosen seats

    Parameters
    ----------
    :param chosen_seats: object with indices in format (row, seat)
        an object containing coordinates of chosen seats in format (row, seat)

    Returns
    -------
    :returns: None if the seats have not been chosen

    Raises
    ------
    :raises IncorrectlyChosenSeats
        if the single seat coordinates are in incorrect format or if a ValueError or TypeError occurs
    '''

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


def validate_num_places(seats_array: np.ndarray, num_places):
    '''Validates the number of places to book

    Parameters
    ----------
    :param seats_array: numpy array
        a 2 dimensional numpy array representing a cinema hall in format [[row], [row]]
        where row is a 1 dimensional array containing zeros (free place) or ones (taken seat) ex. [1, 0, 0, 0, 1]
    :param num_places: str or int

    Returns
    -------
    :returns: num_places as integer if the num_places is a positive integer not larger than the sum of seats_array
    else
    :returns: None

    Raises
    ------
    :raises IncorrectArrayType:
        if the seats_array is not a numpy array or if incorrect data type in array occurs
    :raises ValueError:
        if num_places is not int even after conversion

    '''

    try:
        # If num_places is a string, try to convert it to an integer
        if isinstance(num_places, str):
            num_places = int(num_places)
        # If the seats_array is not a numpy array, raise an exception
        if not isinstance(seats_array, np.ndarray):
            raise IncorrectArrayType('Incorrect array type, numpy array required')

        # Calculating free places in the seats array - the maximum places that you can book
        free_seats = (seats_array.shape[0] * seats_array.shape[1]) - seats_array.sum()

        # If num_places is not and integer or it is smaller than 0 raise ValueError
        if not isinstance(num_places, int) or num_places < 0:
            raise ValueError
        elif free_seats < num_places:  # if num_places is bigger than the number of free seats
            print('Not enough free places for this movie :(\n')
            sleep(2)
            return None
        else:
            return num_places
    except ValueError:
        print('The number of places to book has to be a positive integer!\n')
        sleep(2)
        return None
    except TypeError:
        raise IncorrectArrayData('Incorrect data type in array, integer required')


def say_goodbye():
    '''Says goodbye and destroys the image windows'''

    print('See you next time!!')
    sleep(2)
    # If the reservation is correct destroy the window
    cv2.destroyAllWindows()
    # Clear the screen
    # LINUX
    system('clear')
    # WINDOWS
    # system('cls')


def finalize_booking(places_array):
    '''Prints thank you, destroys all image windows, summarizes the booking process

    Parameters
    ----------
    :param places_array: list or numpy array
        array of chosen seats (their coordinates) in format [(row, seat), (row, seat)]

    Raises
    ------
    :raises IncorrectlyChosenSeats if display_chosen_seats() raised such exception
    '''

    # If the reservation is correct destroy the window
    cv2.destroyAllWindows()
    # Clear the screen
    # LINUX
    system('clear')
    # WINDOWS
    # system('cls')
    try:
        print('\nThank you for your reservation :)')
        display_chosen_seats(places_array)  # display the chosen seats
    except IncorrectlyChosenSeats:
        raise
    sleep(2)
    # Clear the screen
    # LINUX
    system('clear')
    # WINDOWS
    # system('cls')


def validate_row(row, row_indices, seats_array):
    '''Checks if the row is in the keys of row_indices and if the row number is smaller than the array shape

    Parameters
    ----------
    :param row: str
        string representing a row index in a cinema hall
    :param row_indices: dict
        dictionary representing row indices in format {row_label: index} ex. {'A':0, 'B':1}
    :param seats_array: numpy array
        a 2 dimensional numpy array representing a cinema hall in format [[row], [row]]
        where row is a 1 dimensional array containing zeros (free place) or ones (taken seat) ex. [1, 0, 0, 0, 1]

    Returns
    -------
    :returns True if the row is is in row_indices keys
    else
    :returns False

    Raises
    ------
    :raises IncorrectArrayType:
        if the seats_array is not a numpy array
    '''

    if not isinstance(seats_array, np.ndarray):
        raise IncorrectArrayType('Incorrect array type, numpy array required')
    if isinstance(row, str):
        row = row.strip().upper()

    # Row has to be contained in keys and can't be larger than the cinema hall array size
    if (row in row_indices.keys()) and (row_indices[row] < seats_array.shape[0]):
        return True
    else:
        return False


def validate_place(place: int, seats_array: np.ndarray):
    '''Checks if the place is a positive integer smaller than the places in one row of seats array

    Parameters
    ----------
    :param place: int
        place in a cinema hall (in the seats_array row)
    :param seats_array: numpy array
        a 2 dimensional numpy array representing a cinema hall in format [[row], [row]]
        where row is a 1 dimensional array containing zeros (free place) or ones (taken seat) ex. [1, 0, 0, 0, 1]

    Returns
    -------
    :returns True if the place is an integer between 0 and seats_array.shape[1]
    else
    :returns False

    Raises
    ------
    :raises IncorrectArrayType:
        if the seats_array is not a numpy array
    '''

    if not isinstance(seats_array, np.ndarray):
        raise IncorrectArrayType('Incorrect array type, numpy array required')

    if isinstance(place, int) and (place >= 1) and (place <= seats_array.shape[1]):
        return True
    else:
        return False


def book_seats(seats_array, row_indices, num_places):
    '''Creates and returns an array with the chosen seats for the movie

    Parameters
    ----------
    :param seats_array: numpy array
        a 2 dimensional numpy array representing a cinema hall in format [[row], [row]]
        where row is a 1 dimensional array containing zeros (free place) or ones (taken seat) ex. [1, 0, 0, 0, 1]
    :param row_indices: dict
        dictionary representing row indices in format {row_label: index} ex. {'A':0, 'B':1}
    :param num_places: int
        number of places to book

    Returns
    -------
    :returns: numpy array
        returns a modified seats_array

    Raises
    ------
    :raises IncorrectArrayData:
        if the array contains illegal characters (only 0 and 1 permitted)
    :raises IncorrectShape:
        if the seats_array shape does not match row indices
    '''

    # Creating ann array for the chosen places
    places = []
    i = 1  # Seat number for customer's information
    while len(places) != num_places:  # while num_places aren't correctly chosen
        print(f'\nChoosing {i} place\t(If you make a mistake, type -1)')
        # If place is not taken:
        row = input('Row: ').strip().upper()
        try:
            if validate_row(row, row_indices, seats_array):
                place = int(input('Place number: '))
                if validate_place(place, seats_array):  # place has to be between 1 and seats_array.shape[1]
                    # Checking if the seat is not taken
                    if seats_array[row_indices[row], place - 1] == 0:
                        seats_array[row_indices[row], place - 1] = 1
                        # if the choice is correct add the seat to the chosen seats list, thus increase its length
                        places.append((row, place))
                        i += 1  # Increment i representing the seat number for customer's information
                    elif seats_array[row_indices[row], place - 1] == 1:
                        print('This place is already taken! Please choose another one')
                        continue
                    else:
                        raise IncorrectArrayData('Incorrect array, should contain zeros and ones')
                else:
                    raise ValueError  # raise the value error - place has to be an int from 1 to seats_array.shape[1]
            else:  # incorrect row
                print('Incorrect row!')
        except ValueError:  # place has to be an int from 1 to seats_array.shape[1]
            print(f'The place number has to be a positive integer between 1 and {seats_array.shape[1]}!\n')
        except IncorrectArrayType:
            raise
        except IndexError:
            raise IncorrectShape('Array shape does not match row indices')

    # Finalize the booking
    try:
        finalize_booking(places)
        return seats_array  # returns a modified array
    except IncorrectlyChosenSeats:
        print('Could not book the seats')


def display_text_info(scr, movie, font, seats_array: np.ndarray, margin_x):
    '''Adds text representing the movie title and number of taken seats to the screen

    Parameters
    ----------
    :param scr: numpy array
        3 dimensional numpy array representing a screen
    :param movie:
        the chosen movie
    :param font: int
        a font used for text, an integer or cv2 font
    :param seats_array: numpy array
        a 2 dimensional numpy array representing a cinema hall in format [[row], [row]]
        where row is a 1 dimensional array containing zeros (free place) or ones (taken seat) ex. [1, 0, 0, 0, 1]
    :param margin_x: int
        left margin of the cinema hall image

    Returns
    -------
    :returns: screen with added informational text

    Raises
    ------
    :raises IncorrectCoordinates:
        if the margin_x parameter is < 0
    :raises IncorrectArrayType:
        if the seats_array is not a numpy array
    :raises IncorrectArrayData:
        if the array contains illegal characters (only 0 and 1 permitted)
    :raises IncorrectFont:
        if the font is not an integer or a cv2 font
    '''

    if margin_x < 0:
        raise IncorrectCoordinates('Incorrect coordinates! A positive integer required')

    try:
        if not isinstance(seats_array, np.ndarray):
            raise IncorrectArrayType

        taken_seats = int(seats_array.sum())  # getting all the taken seats
    except (TypeError, ValueError):
        raise IncorrectArrayData('Incorrect data type in array, numeric required', movie)

    screen_with_text = scr.copy()  # making a copy of the screen array

    try:
        # Display title
        screen_with_text = cv2.putText(screen_with_text, movie, (margin_x, 35), font, 0.7, (255, 255, 255), 1)
        # Display taken places
        screen_with_text = cv2.putText(screen_with_text, f'Seats taken: {taken_seats}', (margin_x, 60), font, 0.7, (255, 255, 255), 1)
        return screen_with_text  # return the screen with text info added
    except TypeError:
        raise IncorrectFont('Incorrect font, integer or cv2 font required')


def create_square(screen, square_x_first, square_y_first, square_x_second, square_y_second, color, space=0):
    '''Creates a square representing one place

    Parameters
    ----------
    :param screen: numpy array
        3 dimensional numpy array representing a screen
    :param square_x_first: int
        first x coordinate for the square
    :param square_y_first: int
        first y coordinate for the square
    :param square_x_second: int
        second x coordinate for the square
    :param square_y_second: int
        second y coordinate for the square
    :param color: tuple
        square color as a BGR tuple in format (blue, green, red) - each integer value in the range 0-255
    :param space: int, optional
        space between each square (default is 0)

    Returns
    -------
    :returns: screen with a square of specific color added

    Raises
    ------
    :raises IncorrectCoordinates:
        if one of following parameters: square_x_first, square_y_first, square_x_second, square_y_second, space is < 0
    '''
    if min(square_x_first, square_y_first, square_x_second, square_y_second, space) < 0:
        raise IncorrectCoordinates('Incorrect coordinates! A positive integer required')

    new_screen = cv2.rectangle(screen, (space + square_x_first, space + square_y_first),
                               (square_x_second, square_y_second), color, -1)
    return new_screen


def display_row_indices(screen, font, row_indices, j: int, margin_x, margin_y):
    '''Displays the index of "j" row on the given screen

    Parameters
    ----------
    :param screen: numpy array
        3 dimensional numpy array representing a screen
    :param font: int
        a font used for text, an integer or cv2 font
    :param row_indices: dict
        dictionary representing row indices in format {row_label: index} ex. {'A':0, 'B':1}
    :param j: int
        index of a row
    :param margin_x: int
        left margin of the cinema hall image
    :param margin_y: int
        upper margin of the cinema hall image

    Returns
    -------
    :returns: screen with a "j" row index added

    Raises
    ------
    :raises IncorrectCoordinates:
        if the margin_x or margin_y parameter is < 0
    :raises IncorrectShape:
        if the array contains more rows than the keys of row_indices
    :raises IncorrectFont:
        if the font is not an integer or a cv2 font
    '''

    if min(margin_x, margin_y) < 0:
        raise IncorrectCoordinates('Incorrect margin! A positive integer required')

    try:
        new_screen = cv2.putText(screen, f'{tuple(row_indices.keys())[j]}', (margin_x - 10, margin_y - 20 + 37 * (j + 1)),
                                 font, 0.5, (255, 255, 255), 1)
        return new_screen
    except IndexError:
        raise IncorrectShape('Incorrect array shape, too many rows')
    except TypeError:
        raise IncorrectFont('Incorrect font, integer or cv2 font required')


def display_key_info(screen, font, margin_x, screen_height):
    '''Adds text info on the screen about the ESC and ENTER keys

    Parameters
    ----------
    :param screen: numpy array
        3 dimensional numpy array representing a screen
    :param font: int
        a font used for text, an integer or cv2 font
    :param margin_x: int
        left margin of the cinema hall image
    :param screen_height: int
        height of the screen

    Returns
    -------
    :returns: screen with a key info added

    Raises
    ------
    :raises IncorrectCoordinates:
        if the margin_x or screen_height parameter is < 0
    :raises IncorrectFont:
        if the font is not an integer or a cv2 font
    '''

    if min(margin_x, screen_height) < 0:
        raise IncorrectCoordinates('Incorrect margin or screen height! A positive integer required')

    try:
        # Adding text how to escape
        new_screen = cv2.putText(screen, 'Press ESC to exit', (margin_x, screen_height - 7),
                                 font, 0.5, (255, 255, 255), 1)
        # Adding text how to book seats
        new_screen = cv2.putText(screen, 'Press ENTER to book places', (margin_x, screen_height - 27),
                                 font, 0.5, (255, 255, 255), 1)
        return new_screen
    except TypeError:
        raise IncorrectFont('Incorrect font, integer or cv2 font required')


def display_screen(scr, font, margin_x, scr_width):
    '''Draws a blue rectangle and displays info about the screen location in the cinema hall

    Parameters
    ----------
    :param scr: numpy array
        3 dimensional numpy array representing a screen
    :param font: int
        a font used for text, an integer or cv2 font
    :param margin_x: int
        left margin of the cinema hall image
    :param scr_width: int
        width of the screen array

    Returns
    -------
    :returns: screen with SCREEN location info added

    Raises
    ------
    :raises IncorrectCoordinates:
        if the margin_x or scr_width parameter is < 0
    :raises IncorrectFont:
        if the font is not an integer or a cv2 font
    '''

    if min(margin_x, scr_width) < 0:
        raise IncorrectCoordinates('Incorrect margin or screen width! A positive integer required')

    try:
        # Adding a blue rectangle at the screen top - movie screen
        new_scr = cv2.rectangle(scr, (margin_x, 0),
                                (scr_width - margin_x, 12), (255, 0, 0), -1)
        # Adding a movie screen description
        new_scr = cv2.putText(scr, 'SCREEN', (scr_width//2, 10), font, 0.4,
                              (255, 255, 255), 1)
        return new_scr
    except TypeError:
        raise IncorrectFont('Incorrect font, integer or cv2 font required')


def create_row(row, j: int, screen, font, margin_x, margin_y, space=0):
    '''Creates a seats row made of squares and numbers the places.
    If the seats is 0, creates a green square, else creates a red square

    Parameters
    ----------
    :param row: list or numpy array
        1 dimensional array containing zeros (free place) or ones (taken seat) ex. [1, 0, 0, 0, 1]
    :param j: int
        index of a row
    :param screen: numpy array
        3 dimensional numpy array representing a screen
    :param font: int
        a font used for text, an integer or cv2 font
    :param margin_x: int
        left margin of the cinema hall image
    :param margin_y: int
        upper margin of the cinema hall image
    :param space: int, optional
        space between each square (default is 0)

    Raises
    ------
    :raises IncorrectCoordinates:
        if the margin_x, margin_y or space parameter is < 0
    :raises IncorrectFont:
        if create_square() raised an IncorrectFont exception
    '''

    if min(margin_x, margin_y, space) < 0:
        raise IncorrectCoordinates('Incorrect margin or space! A positive integer required')

    # Setting square (each place) parameters
    square_height = 35
    square_width = 25

    try:
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
    except TypeError:
        raise IncorrectFont('Incorrect font, integer or cv2 font required')
    except IncorrectCoordinates:
        raise


def display_image(movie, screen, seats_param: np.ndarray, row_indices):
    '''Displays the cinema hall image with seats

    Waits for a pressed key:
        - if ENTER - proceed to the booking process
        - if ESC - close the window and go back to the menu
    returns the result of book_seats() which is an array of booked seats in format (row, place)

    Parameters
    ----------
    :param movie:
        the chosen movie, if move is None: return None
    :param screen: numpy array
        3 dimensional numpy array representing a screen
    :param seats_param: numpy array
        a 2 dimensional numpy array representing a cinema hall in format [[row], [row]]
        where row is a 1 dimensional array containing zeros (free place) or ones (taken seat) ex. [1, 0, 0, 0, 1]
    :param row_indices: dict
        dictionary representing row indices in format {row_label: index} ex. {'A':0, 'B':1}

    Returns
    -------
    :return: booked_seats_array
        the result of book_seats() which is an array of booked seats in format [(row, place), (row, place)]

    Raises
    ------
    :raises IncorrectArrayType:
        if the seats_array is not a numpy array
    :raises IncorrectShape
        if the seats_param shape[0] array does not match the length of row_indices
    :raises IncorrectArrayData:
        if the array contains illegal characters (only 0 and 1 permitted)
    '''

    if movie is None:
        return

    if not isinstance(seats_param, np.ndarray):
        raise IncorrectArrayType('Incorrect array type, numpy array required', movie)

    if len(row_indices) < seats_param.shape[0]:
        raise IncorrectShape('Array shape does not match row indices')

    while True:
        # Showing the cinema hall image
        cv2.imshow(f'Seats for {movie}', screen)
        # Getting the pressed key
        key = cv2.waitKey(0) & 0xFF
        if key == 27:  # if the pressed key is ESC exit, destroy the window and break the loop
            cv2.destroyAllWindows()
            break
        elif key in {10, 13}:  # if ENTER key - start the booking
            try:
                # if the cinema hall array is not full
                if seats_param.sum() != (seats_param.shape[0] * seats_param.shape[1]):
                    print('Proceeding to place booking')
                    sleep(1.5)
                    # LINUX
                    system('clear')
                    # WINDOWS
                    # system('cls')

                    while True:
                        # Get the number of places to book
                        num_places = input('How many places you want to book?: ')
                        # Validate if the number of places to book is correct
                        num_places = validate_num_places(seats_param, num_places)
                        if num_places is not None:
                            break
                    if num_places == 0:
                        say_goodbye()
                        return
                    booked_seats = book_seats(seats_param, row_indices, num_places)  # return the new array with chosen seats
                    return booked_seats
                else:
                    print('No available places for this movie :(')
                    sleep(2)
                    cv2.destroyAllWindows()
                    return
            except (ValueError, TypeError):
                raise IncorrectArrayData('Incorrect data type in array, integer required', movie)
            except (IncorrectArrayData, IncorrectShape, IncorrectArrayType):
                raise


def show_seats(scr, seats_param: np.ndarray, row_indices, movie, screen_height, screen_width):
    '''Displays the cinema hall with all places
    returns the result of display_image() which is an array of booked seats in format (row, place)

    Parameters
    ----------
    :param scr: numpy array
        3 dimensional numpy array representing a screen
    :param seats_param: numpy array
        a 2 dimensional numpy array representing a cinema hall in format [[row], [row]]
        where row is a 1 dimensional array containing zeros (free place) or ones (taken seat) ex. [1, 0, 0, 0, 1]
    :param row_indices: dict
        dictionary representing row indices in format {row_label: index} ex. {'A':0, 'B':1}
    :param movie:
        the chosen movie, if move is None: return None
    :param screen_height: int
        height of the screen
    :param screen_width: int
        width of the screen

    Returns
    -------
    :returns: None if the movie wasn't chosen (if the movie is None)
    else
    :returns: the result of display_image() which is an array of booked seats in format (row, place)

    Raises
    ------
    :raises IncorrectArrayData
        if the length of seats_param array is 0
        or if it occurs in following functions:
        display_text_info()
        display_image()
    :raises FileError
        if IncorrectShape occurs in following functions:
        display_screen(),
        create_row(),
        display_key_info(),
        display_row_indices()
    :raises IncorrectFont
        if it occurs in the functions above and display_text_info(), display_image()
    :raises IncorrectCoordinates
        if it occurs in the functions above and display_text_info(), display_image()
    :raises IncorrectArrayType
        if it occurs in following functions:
        display_text_info()
        display_image()
    :raises IncorrectShape
        if it occurs in following functions:
        display_text_info()
        display_image()

    '''

    if len(seats_param) == 0:
        raise IncorrectArrayData('The movie array is empty', movie)
    if screen_height <= 0 or screen_width <= 0:
        return
    if movie is None:  # if the move wasn't chosen
        return

    # Setting screen parameters
    margin_x = screen_height // 5
    margin_y = 110
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

        # Show the screen
        display_screen(new_screen, font, margin_x, screen_width)
    except IncorrectShape as e:
        raise FileError('Array shape does not match row indices', e, movie)
    except (IncorrectFont, IncorrectCoordinates):
        raise

    try:
        # Displaying text info on the screen
        new_screen = display_text_info(new_screen, movie, font, seats_param, margin_x)

        # Returning chosen seats or None if the pressed key was ESC (exit from the seat booking section)
        booked_seats = display_image(movie, new_screen, seats_param, row_indices)
        return booked_seats
    except (IncorrectArrayData, IncorrectArrayType, IncorrectShape):
        raise
    except (IncorrectFont, IncorrectCoordinates):
        raise
