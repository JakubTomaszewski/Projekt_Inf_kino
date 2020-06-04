import pytest
import numpy as np
from load_save_data import IncorrectArrayType, IncorrectArrayData, IncorrectShape
from visualisation import (display_chosen_seats,
                           validate_num_places,
                           book_seats,
                           validate_row,
                           validate_place,
                           display_text_info,
                           create_square,
                           display_row_indices,
                           display_key_info,
                           display_screen,
                           create_row,
                           display_image,
                           show_seats,
                           IncorrectlyChosenSeats,
                           )


def test_display_chosen_seats():
    with pytest.raises(IncorrectlyChosenSeats):
        display_chosen_seats(34)

    with pytest.raises(IncorrectlyChosenSeats):
        display_chosen_seats(((1, 2, 3), (1, 2, 3)))

    assert display_chosen_seats(None) is None

    display_chosen_seats(((1, 2), (1, 4)))


def test_validate_num_places():
    seats_array = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    assert validate_num_places(seats_array, 28) is True
    assert validate_num_places(seats_array, 0) is True

    assert validate_num_places(seats_array, 29) is False  # max 2*14 = 28
    assert validate_num_places(seats_array, -2) is False
    assert validate_num_places(seats_array, 1.2) is False
    assert validate_num_places(seats_array, [1]) is False


def test_validate_num_places_list():
    seats_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    with pytest.raises(IncorrectArrayType):
        validate_num_places(seats_array, 3)
        validate_num_places(None, 2)


def test_validate_num_places_str():
    seats_array = np.array([['0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, '0', 0, 0, 0, '0', 0, 0, 0, 0, 0, 0]])
    with pytest.raises(IncorrectArrayData):
        validate_num_places(seats_array, 3)


def test_display_text_info():
    pass


def test_create_square():
    pass


def test_display_row_indices():
    pass


def test_display_key_info():
    # a co jeśli ekran będzie zbyt mały?
    pass


def test_display_screen():
    pass


def test_create_row():
    # a co jeśli ekran będzie zbyt mały?
    pass


def test_show_seats_empty():
    pass


def test_show_seats_full():
    pass


def test_validate_row():
    row_indices = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3
    }

    seats_array = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    assert validate_row('a', row_indices, seats_array) is True
    assert validate_row('A', row_indices, seats_array) is True

    assert validate_row('c', row_indices, seats_array) is False  # because the array shape[1] is to small

    assert validate_row('f', row_indices, seats_array) is False
    assert validate_row(0, row_indices, seats_array) is False
    assert validate_row(None, row_indices, seats_array) is False

    empty_row_indices = {}

    assert validate_row('a', empty_row_indices, seats_array) is False
    assert validate_row(3, empty_row_indices, seats_array) is False
    assert validate_row(None, empty_row_indices, seats_array) is False


def test_validate_row_list():
    row_indices = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3
    }

    seats_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    with pytest.raises(IncorrectArrayType):
        validate_row('a', row_indices, seats_array)


def test_validate_place():
    seats_array = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    assert validate_place(3, seats_array) is True
    assert validate_place(14, seats_array) is True

    assert validate_place(15, seats_array) is False  # max is 14
    assert validate_place(0, seats_array) is False  # min is 1
    assert validate_place(-1, seats_array) is False  # min is 1
    assert validate_place(-0.5, seats_array) is False
    assert validate_place(0.5, seats_array) is False
    assert validate_place(2.3, seats_array) is False
    assert validate_place([2], seats_array) is False


def test_validate_place_list():
    seats_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    with pytest.raises(IncorrectArrayType):
        validate_place(3, seats_array)


def test_validate_place_str():
    seats_array = np.array([['0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, '0', 0, 0, 0, '0', 0, 0, 0, 0, 0, 0]])
    assert validate_place(3, seats_array) is True
