import numpy as np
import os
from meta_data import get_movie_titles


class IncorrectArrayType(Exception):
    def __init__(self, message, movie=None):
        super().__init__(message)
        self.movie = movie


class IncorrectArrayData(TypeError):
    def __init__(self, message, movie=None):
        super().__init__(message)
        self.movie = movie


class IncorrectShape(Exception):
    def __init__(self, message, movie=None):
        super().__init__(message)


class FileError(Exception):
    def __init__(self, message, inner_exception=None, movie=None):
        super().__init__(message)
        self.message = message
        self.inner_exception = inner_exception
        self.movie = movie


def create_txt_info(movie, seats_array: np.ndarray):
    if not isinstance(seats_array, np.ndarray):
        raise IncorrectArrayType('Incorrect array type, numpy array required', movie)
    try:
        return f'Title: {movie}\n' + '+'*45 + f'\nSeats taken: {int(seats_array.sum())}\n'
    except (TypeError, ValueError):
        raise IncorrectArrayData('Incorrect data type in array, integer required', movie)


def create_seats_array(movies, num_rows: int, num_seats: int):
    '''Creates an array made of zeros representing a free cinema hall'''

    if (not isinstance(num_rows, int)) or (not isinstance(num_seats, int)):
        raise IncorrectShape('The number of rows and seats must be an integer')

    if num_rows <= 0 or num_seats <= 0:
        raise IncorrectShape('The number of rows and seats must be a positive integer')

    try:
        for movie in movies:
            # Creating seats array
            seats_array = np.zeros([num_rows, num_seats], dtype=np.int8)

            # Adding report info to the file
            try:
                txt_info = create_txt_info(movie, seats_array)
                movie = str(movie)
                if ':' in movie:
                    # Replacing special characters for a valid filename
                    movie = movie.replace(':', '')

                # Saving the zeros array
                path = f'.\movies\{movie}.csv'
                # path = f'.\movies\{movie}{"" if movie[-4:] == ".csv" or movie[-4:] == ".txt" else ".csv"}'
                np.savetxt(path, seats_array, delimiter=',', fmt='%1d', header=txt_info)
                return
            except IncorrectArrayType as e:
                print(f'Could not create an array for {e.movie}')
            except FileNotFoundError:
                print('Directory could not be found')
                return
    except TypeError:
        print('Movies has to be an iterable object')
        return


def get_csv_data(chosen_movie):
    '''Loads the cinema hall array from a csv file'''
    if chosen_movie is None:
        return
    try:
        if isinstance(chosen_movie, str) and ':' in chosen_movie:
            # Replacing special characters for a valid filename
            chosen_movie = chosen_movie.replace(':', '')
        if os.stat(f'.\movies\{chosen_movie}.csv').st_size == 0:
            raise FileError(f'File for {chosen_movie} is empty', movie=chosen_movie)
        movie_array = np.genfromtxt(f'.\movies\{chosen_movie}.csv', delimiter=',', skip_header=4)
        return movie_array
    except OSError as e:  # if the file does not exist
        raise FileError(f'File or directory could not be found for {chosen_movie}', e, chosen_movie)


def save_csv_data(chosen_movie, seats_array):
    '''Saves the cinema hall array into a csv file'''
    if (chosen_movie is not None) and (seats_array is not None):
        if not isinstance(seats_array, np.ndarray):
            raise IncorrectArrayType('Incorrect array type, numpy array required', chosen_movie)
        try:
            # Adding report info to the file
            txt_info = create_txt_info(chosen_movie, seats_array)
            if isinstance(chosen_movie, str):
                # Replacing special characters for a valid filename
                chosen_movie = chosen_movie.replace(':', '')
                np.savetxt(f'.\movies\{chosen_movie}.csv', seats_array, delimiter=',', fmt='%1d', header=txt_info)
        except IncorrectArrayType as e:
            raise FileError(f'Could not create an array for {e.movie}, ({e})', e, e.movie)
        except IncorrectArrayData as e:
            raise FileError(f'Could not save the file for {e.movie}, ({e})', e, e.movie)
        except FileNotFoundError as e:
            raise FileError('Directory could not be found', e)
