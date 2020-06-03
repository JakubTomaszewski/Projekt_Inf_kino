import numpy as np
from meta_data import get_movie_titles, get_titles_dir
import pytest


def test_get_movie_titles_correct():
    url = 'https://gist.githubusercontent.com/tiangechen/b68782efa49a16edaf07dc2cdaa855ea/raw/0c794a9717f18b094eabab2cd6a6b9a226903577/movies.csv'
    movie_titles_array = get_movie_titles(url)

    assert isinstance(movie_titles_array, (np.ndarray, list))


def test_get_movie_titles_incorrect_title():
    url = 'jakis film'
    movie_titles_array = get_movie_titles(url)


def test_get_movie_titles_incorrect_int():
    url = 23232
    movie_titles_array = get_movie_titles(url)


def test_get_movie_titles_incorrect_list():
    url = [23232, 223]
    movie_titles_array = get_movie_titles(url)


def test_get_titles_dir():
    titles = ['(500) Days of Summer.csv', '27 Dresses.csv', 'A Dangerous Method.csv', 'A Serious Man.csv', 'Across the Universe.csv', 'Beginners.csv', 'Dear John.csv', 'Enchanted.csv', 'Fireproof.csv', 'Four Christmases.csv', 'Ghosts of Girlfriends Past.csv', 'Gnomeo and Juliet.csv', 'Going the Distance.csv', 'Good Luck Chuck.csv', "He's Just Not That Into You.csv", 'High School Musical 3 Senior Year.csv', 'pelny_plik.csv', 'pusty_plik.csv']

    assert get_titles_dir('./movies') == titles


def test_get_titles_dir_inc_path():
    get_titles_dir('incorrect path')

    get_titles_dir('./movies/Dear John.csv')

    assert get_titles_dir() is None
