import numpy as np
import cv2
# import csv


def display_movies(movies_list):
    for movie in movies_list:
        print('+++++++++++++++++++++++++++++++')
        print(movie)


def display_text_info(scr, movie, font):
    '''Displays the movie title and number of taken seats'''
    # Setting font
    taken_seats = int(seats.sum())
    screen_with_text = scr.copy()

    # Display title
    screen_with_text = cv2.putText(screen_with_text, movie, (margin_x, 35), font, 0.7, (255, 255, 255), 1)
    # Display taken places
    screen_with_text = cv2.putText(screen_with_text, f'Liczba osob: {taken_seats}', (margin_x, 60), font, 0.7, (255, 255, 255), 1)
    return screen_with_text


def show_seats(scr, seats_param, movie: str, indices):
    assert isinstance(movie, str)
    new_screen = scr.copy()
    font = cv2.FONT_HERSHEY_DUPLEX
    j = 0

    for row in seats_param:
        i = 0
        new_screen = cv2.putText(new_screen, f'{tuple(indices.keys())[j]}', (margin_x - 10, margin_y - 20 + 37 * (j+1)),
                                 font, 0.5, (255, 255, 255), 1)
        new_screen = cv2.putText(new_screen, 'Nacisnij ESC aby wyjsc', (margin_x, screen_height - 15),
                                 font, 0.5, (255, 255, 255), 1)
        for seat in row:
            square_height = 35
            square_width = 25
            square_x_first = margin_x + square_width * i
            square_y_first = margin_y + square_height * j
            square_x_second = margin_x + square_width * (i + 1)
            square_y_second = margin_y + square_height * (j + 1)

            # Col label
            if j == 0:
                new_screen = cv2.putText(new_screen, f'{i + 1}', (square_x_first + 5, square_y_first - 5),
                                         font, 0.5, (255, 255, 255), 1)
            if seat == 0:
                # creating a green square
                new_screen = cv2.rectangle(new_screen, (space + square_x_first, space + square_y_first), (square_x_second, square_y_second),
                                       (0, 255, 0), -1)
            else:
                # creating a red square
                new_screen = cv2.rectangle(new_screen, (space + square_x_first, space + square_y_first), (square_x_second, square_y_second),
                                       (0, 0, 255), -1)
            i += 1
        j += 1
    # Adding the screen position
    new_screen = cv2.rectangle(new_screen, (margin_x, 0),
                               (screen_width - margin_x, 7), (255, 0, 0), -1)
    new_screen = cv2.putText(new_screen, 'EKRAN', (screen_width//2, 10), font, 0.4,
                             (255, 255, 255), 1)

    new_screen = display_text_info(new_screen, movie, font)
    while True:
        cv2.imshow(f'Seats for {movie}', new_screen)
        if cv2.waitKey(0) & 0xFF == 27: # if the pressed key is ESC exit and destroy the window
            cv2.destroyAllWindows()
            break


# Automate it with selenium?
movies = ['A WIĘC WOJNA', 'ABRAHAM LINCOLN: ŁOWCA WAMPIRÓW', 'ABSOLUTNIE FANTASTYCZNE: FILM', 'ACH ŚPIJ KOCHANIE', 'AD ASTRA', 'ADOLF H. JA WAM POKAŻĘ', 'ADRENALINA 2. POD NAPIĘCIEM', 'ADWOKAT', 'AFONIA I PSZCZOŁY', 'AFTER', 'AGENCI', 'AGENT I PÓŁ']

display_movies(movies)

chosen_movie = 'A WIEC WOJNA'

screen_height = 410
screen_width = 850

seats = np.zeros([7, 30], dtype=np.int)
screen = np.zeros([screen_height, screen_width, 3], np.uint8)

row_indices = {
                'A': 0,
                'B': 1,
                'C': 2,
                'D': 3,
                'E': 4,
                'F': 5,
                'G': 6
               }

seats[4,5] = 1
seats[4,6] = 1

margin_x = 50
margin_y = 120
space = 6


show_seats(screen, seats, chosen_movie, row_indices)

chosen_movie = 'DRUGI FILM'
seats[4,5] = 1
seats[4,7] = 1
show_seats(screen, seats, chosen_movie, row_indices)

np.savetxt(f'{chosen_movie}.csv', seats, delimiter=',')
movie_seats = np.genfromtxt(f'{chosen_movie}.csv', delimiter=',')
print(movie_seats)

'''
- Każdy film ma swój plik csv który wczytujemy w momencie wyboru i ukazujemy za pomocą funkcji show_seats().
np.savetxt(f'{chosen_movie}.csv', seats, delimiter=',')
movie_seats = np.genfromtxt(f'{chosen_movie}.csv', delimiter=',')
print(movie_seats)

- Indeksowanie rzędów za pomocą liter i wykorzystać słownik do klucz:index np. 'a'.upper():0, 'b'.upper():1
- Dorobić interaktywne menu za pomocą curses?
- Dodać informacje gdzie znajduje się ekran
'''

