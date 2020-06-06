'''
Meta_Data Module
-----------------

This module contains functions, which allow getting titles of movies from csv files
'''


import pandas as pd
import numpy as np
import os


def get_movie_titles(url: str):
    '''Returns a numpy array with titles of movies

    Parameters
    ----------
    :param url: str
        path or url to a data frame (csv file)

    Returns
    -------
    :return: numpy array
        numpy array with titles of movies
    '''

    try:
        # Loading movie data
        movies_df = pd.read_csv(url)
        # Getting only the titles column and some rows
        movie_titles = movies_df.loc[60:, 'Film']
        # Dropping duplicate rows
        movie_titles = movie_titles.drop_duplicates()
        # Transforming it to a numpy array
        movie_titles_array = movie_titles.values
        return movie_titles_array
    except FileNotFoundError:
        print('File or URL could not be found')
    except ValueError:
        print('Incorrect path')


def get_titles_dir(path=None):
    '''Returns an array with titles of movies from a specific directory

    Parameters
    ----------
    :param path: str
        path to a directory with files, None - current directory

    Returns
    -------
    :return: list
        array with titles of movies
    '''

    if path is None:
        return
    try:
        movies = [''.join(movie.split('.')[:-1]) for movie in np.array(os.listdir(path))]
        return movies
    except PermissionError:
        print('Could not open the directory')
    except OSError:
        print('Incorrect path')
