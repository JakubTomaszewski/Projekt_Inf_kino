import numpy as np
from meta_data import get_movie_titles


def create_txt_info(movie, seats_array):
    return f'Title: {movie}\n' + '+'*45 + f'\nSeats taken: {int(seats_array.sum())}\n'


def create_seats_array(movies: (np.ndarray, list), num_rows: int, num_seats: int):
    '''Creates an array made of zeros representing a free cinema hall'''
    assert isinstance(movies, (np.ndarray, list))
    assert isinstance(num_rows, int)
    assert isinstance(num_seats, int)

    for movie in movies:
        # Creating seats array
        seats_array = np.zeros([num_rows, num_seats], dtype=np.int8)

        # Adding report info to the file
        txt_info = create_txt_info(movie, seats_array)
        movie = movie.replace(':', '')  # Replacing special characters for a valid filename
        # Saving the zeros array
        np.savetxt(f'.\movies\{movie}.csv', seats_array, delimiter=',', fmt='%1d', header=txt_info)


def get_csv_data(chosen_movie: str):
    '''Loads the cinema hall array from a csv file'''
    if chosen_movie is not None:
        assert isinstance(chosen_movie, str)
        chosen_movie = chosen_movie.replace(':', '')  # Replacing special characters for a valid filename
        try:
            movie_array = np.genfromtxt(f'.\movies\{chosen_movie}.csv', delimiter=',', skip_header=4)
            return movie_array
        except FileNotFoundError:  # if the file does not exist
            create_seats_array([chosen_movie], rows, seats)


def save_csv_data(chosen_movie: str, seats_array: np.ndarray):
    '''Saves the cinema hall array into a csv file'''
    if seats_array is not None and chosen_movie is not None:
        assert isinstance(chosen_movie, str)
        assert isinstance(seats_array, np.ndarray)
        # Adding report info to the file
        txt_info = create_txt_info(chosen_movie, seats_array)
        chosen_movie = chosen_movie.replace(':', '')  # Replacing special characters for a valid filename
        np.savetxt(f'.\movies\{chosen_movie}.csv', seats_array, delimiter=',', fmt='%1d', header=txt_info)
