'''
Load_Save_Data Module
-----------------

This module allows:
    -creating numpy arrays representing seats in a cinema hall
    -loading csv files into numpy arrays representing seats in a cinema hall
    -saving numpy arrays representing seats in a cinema hall into csv files

'''


import numpy as np
import string
import os


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
    '''Creates text info about a specific movie containing its title and number of taken seats (sum of seats_array)

    Parameters
    ----------
    :param movie: str
        movie title
    :param seats_array: numpy array
        a 2 dimensional numpy array representing a cinema hall in format [[row], [row]]
        where row is a 1 dimensional array containing zeros (free place) or ones (taken seat) ex. [1, 0, 0, 0, 1]

    Returns
    -------
    :return: text info about the move and seats taken (sum of the seats_array)

    Raises
    ------
    :raises IncorrectArrayType:
        if the seats_array is not a numpy array
    :raises IncorrectArrayData:
        if the array contains illegal characters (only 0 and 1 permitted)
    '''

    if not isinstance(seats_array, np.ndarray):
        raise IncorrectArrayType('Incorrect array type, numpy array required', movie)
    try:
        return f'Title: {movie}\n' + '+'*45 + f'\nSeats taken: {int(seats_array.sum())}\n'
    except (TypeError, ValueError):
        raise IncorrectArrayData('Incorrect data type in array, integer required', movie)


def create_seats_array(movies, num_rows: int, num_seats: int):
    '''Creates an array made of zeros representing a free cinema hall for each movie in movies

    Parameters
    ----------
    :param movies: list
        1 dimensional list of movie titles
    :param num_rows: int
        number of rows
    :param num_seats: int
        number of seats

    Returns
    -------
    :return: None if FileNotFoundError or TypeError is raised

    Raises
    ------
    :raises IncorrectShape:
        if num_rows or num_seats is not an integer or is < 0
    '''

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
                movie = repair_title(movie)

                # Saving the zeros array
                path = f'.\movies\{movie}.csv'
                np.savetxt(path, seats_array, delimiter=',', fmt='%1d', header=txt_info)
            except IncorrectArrayType as e:
                print(f'Could not create an array for {e.movie}')
            except FileNotFoundError:
                print('Directory could not be found')
                return
    except TypeError:
        print('Movies has to be an iterable object')
        return


def get_csv_data(chosen_movie, path):
    '''Loads the cinema hall array from a csv file and returns it as a numpy array

    Parameters
    ----------
    :param chosen_movie: str
        chosen movie title
    :param path: str
        path to chosen_movie csv file

    Returns
    -------
    :return: numpy array representing a cinema hall array

    Raises
    ------
    :raises FileError:
        if the chosen_movie csv file is empty
        or if OSError is raised (file or directory could not be found)
        or if TypeError is raised (incorrect path)
    '''

    if chosen_movie is None:
        return
    try:
        if os.stat(path).st_size == 0:
            raise FileError(f'File for {chosen_movie} is empty', movie=chosen_movie)
        movie_array = np.genfromtxt(path, delimiter=',', skip_header=4)
        return movie_array
    except OSError as e:  # if the file does not exist
        raise FileError(f'File or directory could not be found for {chosen_movie}', e, chosen_movie)
    except TypeError as e:
        raise FileError(f'Incorrect path for {chosen_movie}', e, chosen_movie)


def save_csv_data(chosen_movie, seats_array, path):
    '''Saves the cinema hall array into a csv file

    Parameters
    ----------
    :param chosen_movie: str
        chosen movie title
    :param seats_array: numpy array
        a 2 dimensional numpy array representing a cinema hall in format [[row], [row]]
        where row is a 1 dimensional array containing zeros (free place) or ones (taken seat) ex. [1, 0, 0, 0, 1]
    :param path: str
        path to chosen_movie csv file

    Raises
    ------
    :raises FileError:
        if one of the following exceptions is raised:
        IncorrectArrayType,
        IncorrectArrayData,
        FileNotFoundError
        TypeError
    '''

    if (chosen_movie is not None) and (seats_array is not None):
        if not isinstance(seats_array, np.ndarray):
            raise IncorrectArrayType('Incorrect array type, numpy array required', chosen_movie)
        try:
            # Adding report info to the file
            txt_info = create_txt_info(chosen_movie, seats_array)

            # Saving the zeros array
            np.savetxt(path, seats_array, delimiter=',', fmt='%1d', header=txt_info)
        except IncorrectArrayType as e:
            raise FileError(f'Could not create an array for {e.movie}, ({e})', e, e.movie)
        except IncorrectArrayData as e:
            raise FileError(f'Could not save the file for {e.movie}, ({e})', e, e.movie)
        except FileNotFoundError as e:
            raise FileError('Directory could not be found', e)
        except TypeError as e:
            raise FileError(f'Incorrect path for {chosen_movie}', e, chosen_movie)


def repair_title(chosen_movie):
    '''Returns a chosen_movie title without incorrect (illegal) characters for a filename

    Parameters
    ----------
    :param chosen_movie: str
        chosen movie title

    Returns
    -------
    :return: str
        a valid title for a filename

    Raises
    ------
    :raises FileError:
        if ValueError or TypeError is raised
    '''

    try:
        valid_chars = "-_.()[] %s%s" % (string.ascii_letters, string.digits)
        # Replacing special characters for a valid filename
        valid_chosen_movie = ''.join((c for c in chosen_movie if c in valid_chars))
        return valid_chosen_movie
    except (ValueError, TypeError):
        raise FileError(f'Incorrect movie title: {chosen_movie}', chosen_movie)
