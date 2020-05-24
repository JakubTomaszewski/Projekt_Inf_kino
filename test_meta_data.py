import numpy as np
from meta_data import get_movie_titles


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
