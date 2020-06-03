import pandas as pd
import numpy as np
import os


def get_movie_titles(url: str):
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
    if path is None:
        return
    try:
        movies = [''.join(movie.split('.')[:-1]) for movie in np.array(os.listdir(path))]
        return movies
    except PermissionError:
        print('Could not open the directory')
    except OSError:
        print('Incorrect path')


# print(get_titles_dir('./movies'))