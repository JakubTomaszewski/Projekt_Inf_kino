import numpy as np


def create_seats_array(movies, num_rows, num_seats):
    for movie in movies:
        # Creating seats array
        seats_array = np.zeros([num_rows, num_seats], dtype=np.int8)
        movie = movie.replace(':', '')
        np.savetxt(f'.\movies\{movie}.csv', seats_array, delimiter=',', fmt='%1d')


def get_csv_data(chosen_movie):
    chosen_movie = chosen_movie.replace(':', '')
    movie_array = np.genfromtxt(f'.\movies\{chosen_movie}.csv', delimiter=',')
    return movie_array


def save_csv_data(chosen_movie, seats_array):
    if seats_array is not None:
        chosen_movie = chosen_movie.replace(':', '')
        np.savetxt(f'.\movies\{chosen_movie}.csv', seats_array, delimiter=',', fmt='%1d')


rows = 7
seats = 30
movie_list = ['A WIĘC WOJNA', 'ABRAHAM LINCOLN: ŁOWCA WAMPIRÓW', 'ABSOLUTNIE FANTASTYCZNE: FILM', 'ACH ŚPIJ KOCHANIE', 'AD ASTRA', 'ADOLF H. JA WAM POKAŻĘ', 'ADRENALINA 2. POD NAPIĘCIEM', 'ADWOKAT', 'AFONIA I PSZCZOŁY', 'AFTER', 'AGENCI', 'AGENT I PÓŁ']

# create_seats_array(movie_list, rows, seats)
