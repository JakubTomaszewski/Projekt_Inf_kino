import cv2
from os import system


def display_chosen_seats(chosen_seats):
    '''Prints the chosen seats'''
    print('Wybrane miejsca: ')
    for seat in chosen_seats:
        print(f'Rząd {seat[0]} Miejsce {seat[1]}')


def reserve_seats(seats_array):
    '''Books seats for the movie'''
    num_places = int(input('Ile miejsc zarezerwowac?: '))
    places = []
    i = 1
    while len(places) != num_places:
        print(f'Wybór miejsca {i}')
        # If place is not taken:
        row = input('Rząd: ').upper()  # Row has to be in dict keys
        if row in row_indices.keys():
            try:
                place = int(input('Numer miejsca: '))  # place has to be between 1 and 30
                if (place >= 1) and (place <= 30):
                    # Checking if the seat is not taken
                    if seats_array[row_indices[row], place - 1] != 1:
                        seats_array[row_indices[row], place - 1] = 1
                        places.append((row, place))
                        i += 1
                    else:
                        print('To miejsce jest już zajęte!')
                        continue
                else:
                    raise ValueError
            except ValueError:
                print('Miejsce musi byc numerem całkowitym od 1 do 30!')
        else:
            print('Nieprawidłowy rząd!')

    system('cls')
    print('Dziekujemy za rezerwacje :)')
    display_chosen_seats(places) #
    return seats_array  # returns a modified array


def display_text_info(scr, movie, font, seats_param):
    '''Displays the movie title and number of taken seats'''
    # Setting font
    taken_seats = int(seats_param.sum())
    screen_with_text = scr.copy()

    # Display title
    screen_with_text = cv2.putText(screen_with_text, movie, (margin_x, 35), font, 0.7, (255, 255, 255), 1)
    # Display taken places
    screen_with_text = cv2.putText(screen_with_text, f'Liczba osob: {taken_seats}', (margin_x, 60), font, 0.7, (255, 255, 255), 1)
    return screen_with_text


def show_seats(scr, seats_param, movie: str):
    '''Displays the cinema hall with all places'''
    if movie == None:
        print('Do zobaczenia nastepnym razem!')
        return

    assert isinstance(movie, str)
    new_screen = scr.copy()
    font = cv2.FONT_HERSHEY_DUPLEX

    for j, row in enumerate(seats_param):
        new_screen = cv2.putText(new_screen, f'{tuple(row_indices.keys())[j]}', (margin_x - 10, margin_y - 20 + 37 * (j+1)),
                                 font, 0.5, (255, 255, 255), 1)
        new_screen = cv2.putText(new_screen, 'Nacisnij ESC aby wyjsc', (margin_x, screen_height - 15),
                                 font, 0.5, (255, 255, 255), 1)
        for i, seat in enumerate(row):
            square_height = 35
            square_width = 25
            square_x_first = margin_x + square_width * i
            square_y_first = margin_y + square_height * j
            square_x_second = margin_x + square_width * (i + 1)
            square_y_second = margin_y + square_height * (j + 1)

            # Setting col label (seat numbers)
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

    # Adding a blue rectangle at the screen top - movie screen
    new_screen = cv2.rectangle(new_screen, (margin_x, 0),
                               (screen_width - margin_x, 12), (255, 0, 0), -1)
    # Adding a movie screen description
    new_screen = cv2.putText(new_screen, 'EKRAN', (screen_width//2, 10), font, 0.4,
                             (255, 255, 255), 1)

    # Displaying text info on the screen
    new_screen = display_text_info(new_screen, movie, font, seats_param)
    while True:  # showing the image
        cv2.imshow(f'Seats for {movie}', new_screen)
        key = cv2.waitKey(0) & 0xFF
        if key == 27:  # if the pressed key is ESC exit, destroy the window and break the loop
            cv2.destroyAllWindows()
            break
        elif key in (10, 13):  # Enter key
            print('Przechodzę do rezerwacji miejsc')
            return reserve_seats(seats_param)  # return the new array with chosen seats


# Setting screen parameters
screen_height = 410
screen_width = 850
margin_x = 50
margin_y = 120
space = 6

# Row indices
row_indices = {
                'A': 0,
                'B': 1,
                'C': 2,
                'D': 3,
                'E': 4,
                'F': 5,
                'G': 6
               }



# np.savetxt(f'{chosen_movie}.csv', seats, delimiter=',', fmt='%1d')
#
# movie_seats = np.loadtxt(f'{chosen_movie}.csv', delimiter=',')
# movie_seats = np.genfromtxt(f'{chosen_movie}.csv', delimiter=',')

'''
- Każdy film ma swój plik csv który wczytujemy w momencie wyboru i ukazujemy za pomocą funkcji show_seats().
np.savetxt(f'{chosen_movie}.csv', seats, delimiter=',')
movie_seats = np.genfromtxt(f'{chosen_movie}.csv', delimiter=',')
print(movie_seats)

+ Dorobić interaktywne menu za pomocą curses?
+ Dodać informacje gdzie znajduje się ekran

- Naprawić czcionkę polską!!!!
- Indeksowanie rzędów za pomocą liter i wykorzystać słownik do klucz:index np. 'a'.upper():0, 'b'.upper():1
- Zabezpieczyć jeśli miejsce jest zajęte!
'''

