import cv2
from os import system
from time import sleep
import numpy as np


def display_chosen_seats(chosen_seats: list):
    '''Prints the chosen seats'''
    print('Chosen seats: ')
    for seat in chosen_seats:
        # Print the row and place
        print(f'Row {seat[0]} Place {seat[1]}')


def get_num_places():
    '''Assures the inserted number of places is an integer'''
    try:
        num_places = int(input('How many places you want to book?: '))
        if num_places < 0:
            raise ValueError
        return num_places
    except ValueError:
        print('The number of places to book has to be a positive integer!')
        sleep(1.5)
        return get_num_places()


def say_goodbye():
    '''Says goodbye and destroys the image windows'''
    print('See you next time!!')
    sleep(1.5)
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
    print('Thank you for your reservation :)')
    display_chosen_seats(places_array)  # display the chosen seats
    sleep(1.5)
    system('cls')


def book_seats(seats_array: list):
    '''Books seats for the movie'''
    # Get the number of places to book
    num_places = get_num_places()
    if num_places == 0:
        say_goodbye()
        return seats_array

    # Creating ann array for the chosen places
    places = []
    i = 1  # Seat number for customer's information
    while len(places) != num_places:  # while num_places aren't correctly chosen
        print(f'Choosing {i} place')
        # If place is not taken:
        row = input('Row: ').strip().upper()
        if row in row_indices.keys():  # Row has to be in dict keys A-G
            try:
                place = int(input('Place number: '))
                if (place >= 1) and (place <= 30):  # place has to be between 1 and 30
                    # Checking if the seat is not taken
                    if seats_array[row_indices[row], place - 1] != 1:
                        seats_array[row_indices[row], place - 1] = 1
                        # if the choice is correct add the seat to the chosen seats list, thus increase its length
                        places.append((row, place))
                        i += 1
                    else:
                        print('This place is already taken!\nPlease choose another one')
                        continue
                else:
                    raise ValueError  # raise the value error - place has to be an int from 1 to 30
            except ValueError:  # place has to be an int from 1 to 30
                print('The place number has to be a positive integer between 1 and 30!')
        else:  # incorrect row
            print('Incorrect row!')

    # Finalize the booking
    finalize_booking(places)
    return seats_array  # returns a modified array


def display_text_info(scr, movie: str, font, seats_array: np.ndarray):
    '''Displays the movie title and number of taken seats'''
    assert isinstance(movie, str)
    taken_seats = int(seats_array.sum())  # getting all the taken seats
    screen_with_text = scr.copy()  # making a copy of the screen array

    # Display title
    screen_with_text = cv2.putText(screen_with_text, movie, (margin_x, 35), font, 0.7, (255, 255, 255), 1)
    # Display taken places
    screen_with_text = cv2.putText(screen_with_text, f'Seats taken: {taken_seats}', (margin_x, 60), font, 0.7, (255, 255, 255), 1)
    return screen_with_text  # return the screen with text info added


def create_square(screen, square_x_first, square_y_first, square_x_second, square_y_second, color: tuple):
    '''Creates a square representing one place'''
    new_screen = cv2.rectangle(screen, (space + square_x_first, space + square_y_first),
                               (square_x_second, square_y_second), color, -1)
    return new_screen


def display_row_indices(screen, font, j: int):
    '''Displays the j row index'''
    new_screen = cv2.putText(screen, f'{tuple(row_indices.keys())[j]}', (margin_x - 10, margin_y - 20 + 37 * (j + 1)),
                             font, 0.5, (255, 255, 255), 1)
    return new_screen


def display_key_info(screen, font):
    '''Adds text info on the screen about the ESC and ENTER keys'''
    # Adding text how to escape
    new_screen = cv2.putText(screen, 'Press ESC to exit', (margin_x, screen_height - 7),
                             font, 0.5, (255, 255, 255), 1)
    # Adding text how to book seats
    new_screen = cv2.putText(screen, 'Press ENTER to book places', (margin_x, screen_height - 27),
                             font, 0.5, (255, 255, 255), 1)
    return new_screen


def display_screen(screen, font):
    '''Draws a blue rectangle and displays info about the screen location in the cinema hall'''
    # Adding a blue rectangle at the screen top - movie screen
    new_screen = cv2.rectangle(screen, (margin_x, 0),
                               (screen_width - margin_x, 12), (255, 0, 0), -1)
    # Adding a movie screen description
    new_screen = cv2.putText(screen, 'SCREEN', (screen_width//2, 10), font, 0.4,
                             (255, 255, 255), 1)
    return new_screen


def create_row(row: np.ndarray, j: int, screen, font):
    '''Creates a seats row made of squares'''
    for i, seat in enumerate(row):
        # Setting square (each place) parameters
        square_height = 35
        square_width = 25
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
            new_screen = create_square(screen, square_x_first, square_y_first, square_x_second, square_y_second, (0, 255, 0))
        else:
            # creating a red square
            new_screen = create_square(screen, square_x_first, square_y_first, square_x_second, square_y_second, (0, 0, 255))


def display_image(movie: str, screen, seats_param: np.ndarray):
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
            print('Proceeding to place booking')
            return book_seats(seats_param)  # return the new array with chosen seats


def show_seats(scr, seats_param: np.ndarray, movie: str):
    '''Displays the cinema hall with all places'''
    if movie is None:  # if the move wasn't chosen
        return

    assert isinstance(movie, str)
    assert isinstance(seats_param, np.ndarray)
    new_screen = scr.copy()  # making a copy of the screen array
    # Setting a font
    font = cv2.FONT_HERSHEY_DUPLEX

    # Creating a square for each seat in a row
    for j, row in enumerate(seats_param):
        # Adding row indices
        new_screen = display_row_indices(new_screen, font, j)

        # Adding text how to exit and how to book seats
        new_screen = display_key_info(new_screen, font)

        # Creates a row
        create_row(row, j, new_screen, font)

    # Show the screen
    display_screen(new_screen, font)

    # Displaying text info on the screen
    new_screen = display_text_info(new_screen, movie, font, seats_param)

    # Returning chosen seats or None if the pressed key was ESC (exit from the seat booking section)
    return display_image(movie, new_screen, seats_param)


# Setting screen parameters
screen_height = 410
screen_width = 850
margin_x = 50
margin_y = 120
space = 6

# Row indices as keys and their numeric indices as values
row_indices = {
                'A': 0,
                'B': 1,
                'C': 2,
                'D': 3,
                'E': 4,
                'F': 5,
                'G': 6
               }
