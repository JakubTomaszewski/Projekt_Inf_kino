import numpy as np
import pytest
from load_save_data import (create_txt_info,
                            create_seats_array,
                            get_csv_data,
                            save_csv_data,
                            IncorrectArrayType,
                            IncorrectArrayData,
                            IncorrectShape,
                            FileError,
                            repair_title)


def test_create_txt_info():
    assert create_txt_info('Teletubisie', np.array([0, 0, 1, 0])) == 'Title: Teletubisie\n' + '+'*45 + f'\nSeats taken: 1\n'

    with pytest.raises(IncorrectArrayType):
        create_txt_info('Teletubisie', [1, 2, 3])

    with pytest.raises(IncorrectArrayType):
        create_txt_info(3, 3.5)

    with pytest.raises(IncorrectArrayData):
        create_txt_info('Teletubisie', np.array(['2', 2, 34]))


def test_create_seats_array():
    movies = ['film', 'przykladowy', 'Polska']
    num_rows = 2
    num_seats = 23
    create_seats_array(movies, num_rows, num_seats)

    movies = 5
    num_rows = 3
    num_seats = 3
    create_seats_array(movies, num_rows, num_seats)


def test_create_seats_array_two():
    with pytest.raises(IncorrectShape):
        movies = 'filmy'
        num_rows = 2
        num_seats = 3.4
        create_seats_array(movies, num_rows, num_seats)

        movies = ('filmy1', 'film2')
        num_rows = 'rząd'
        num_seats = 3
        create_seats_array(movies, num_rows, num_seats)

        movies = ('filmy1', 'film2')
        num_rows = -3
        num_seats = 3
        create_seats_array(movies, num_rows, num_seats)

        movies = ('filmy1', 'film2')
        num_rows = 3
        num_seats = 0
        create_seats_array(movies, num_rows, num_seats)


def test_get_csv_data():
    assert get_csv_data(None, '.\random\path') is None

    with pytest.raises(FileError):
        get_csv_data('pusty_plik.csv', '.\movies\pusty_plik.csv')

    with pytest.raises(FileError):
        get_csv_data('film którego nie ma', 'ścieżka do filmu którego nie ma')
        get_csv_data(0, 0)
        get_csv_data(':', ':')


def test_save_csv_data():
    with pytest.raises(FileError):
        save_csv_data(';:::::;', np.array([23]), ';:::movie::;')
        save_csv_data('movie', np.array([23]), ';:::movie::;')

    save_csv_data(None, 12, '.\test_movies\mov')
    save_csv_data('film', None, '.\test_movies\mov')

    with pytest.raises(IncorrectArrayType):
        save_csv_data('film', [12], '.\test_movies\mov')

    with pytest.raises(IncorrectArrayType):
        save_csv_data('film', 'lista', '.\test_movies\mov')

    with pytest.raises(FileError):
        save_csv_data('film', np.array(['a', 2, 3]), '.\test_movies\mov')


def test_repair_title():
    assert repair_title('') == ''
    assert repair_title(':.movie:') == '.movie'
    assert repair_title(':0:.movie:') == '0.movie'
    assert repair_title('%invalid%') == 'invalid'

    with pytest.raises(FileError):
        repair_title(23)
        repair_title([1, 2, 3])



