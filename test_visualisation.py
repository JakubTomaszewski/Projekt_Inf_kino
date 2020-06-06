import cv2
import pytest
import curses
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
                           IncorrectFont,
                           IncorrectCoordinates
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
    assert validate_num_places(seats_array, 28) == 28
    assert validate_num_places(seats_array, 0) == 0

    assert validate_num_places(seats_array, 29) is None  # max 2*14 = 28
    assert validate_num_places(seats_array, -2) is None
    assert validate_num_places(seats_array, 1.2) is None
    assert validate_num_places(seats_array, [1]) is None


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


def test_display_text_info():
    seats_array = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    scr = np.zeros([20, 20, 3], np.uint8)
    font = cv2.FONT_HERSHEY_DUPLEX

    assert display_text_info(scr, 'a movie', font, seats_array, 15) is not scr
    assert display_text_info(scr, 'a movie', 4, seats_array, 15) is not scr

    with pytest.raises(IncorrectFont):
        display_text_info(scr, 'a movie', 'incorrect font', seats_array, 15)

    inc_seats_array = np.array([['0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, '0', 0, 0, 0, '0', 0, 0, 0, 0, 0, 0]])

    with pytest.raises(IncorrectArrayData):
        display_text_info(scr, 'a movie', font, inc_seats_array, 15)

    with pytest.raises(IncorrectCoordinates):
        display_text_info(scr, 'a movie', font, inc_seats_array, -1)


def test_create_square():
    scr = np.zeros([20, 20, 3], np.uint8)

    assert create_square(scr, 10, 10, 15, 15, (0, 255, 0)) is scr

    with pytest.raises(IncorrectCoordinates):
        create_square(scr, -10, 10, 15, 15, (0, 255, 0))


def test_display_row_indices():
    scr = np.zeros([20, 20, 3], np.uint8)
    font = cv2.FONT_HERSHEY_DUPLEX
    row_indices = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3
    }

    display_row_indices(scr, font, row_indices, 3, 2, 5)

    with pytest.raises(IncorrectCoordinates):
        display_row_indices(scr, font, row_indices, 3, -1, -5)

    with pytest.raises(IncorrectFont):
        display_row_indices(scr, 'inc font', row_indices, 3, 2, 5)

    with pytest.raises(IncorrectShape):
        display_row_indices(scr, font, row_indices, 10, 2, 5)


def test_display_key_info():
    scr = np.zeros([20, 20, 3], np.uint8)
    font = cv2.FONT_HERSHEY_DUPLEX

    display_key_info(scr, font, 10, 100)

    with pytest.raises(IncorrectCoordinates):
        display_key_info(scr, font, -10, 100)
        display_key_info(scr, font, 10, -100)

    with pytest.raises(IncorrectFont):
        display_key_info(scr, 'inc font', 10, 100)


def test_display_screen():
    scr = np.zeros([20, 20, 3], np.uint8)
    font = cv2.FONT_HERSHEY_DUPLEX

    with pytest.raises(IncorrectCoordinates):
        display_screen(scr, font, -10, 200)
        display_screen(scr, font, 10, -200)

    with pytest.raises(IncorrectFont):
        display_screen(scr, 'inc font', 10, 200)


def test_create_row():
    scr = np.zeros([20, 20, 3], np.uint8)
    font = cv2.FONT_HERSHEY_DUPLEX
    row = [0, 1, 0, 0, 0]

    with pytest.raises(IncorrectCoordinates):
        create_row(row, 2, scr, font, 15, -12)
        create_row(row, 2, scr, font, -15, 12)
        create_row(row, 2, scr, font, 15, 12, -3)

    with pytest.raises(IncorrectFont):
        create_row(row, 0, scr, 'inc font', 15, 12, 3)


def test_display_image():
    scr = np.zeros([20, 20, 3], np.uint8)
    row_indices = {
        'A': 0,
        'B': 1,
        'C': 2
    }
    seats_array = np.array([[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]])

    assert display_image(None, scr, seats_array, row_indices) is None

    inc_row_indices = {
        'A': 0,
        'B': 1
    }
    with pytest.raises(IncorrectShape):
        display_image('movie', scr, seats_array, inc_row_indices)


def test_display_image_list():
    scr = np.zeros([20, 20, 3], np.uint8)
    row_indices = {
        'A': 0,
        'B': 1,
        'C': 2
    }
    seats_array = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]]

    with pytest.raises(IncorrectArrayType):
        display_image('movie', scr, seats_array, row_indices)


def test_show_seats():
    scr = np.zeros([20, 20, 3], np.uint8)
    row_indices = {
        'A': 0,
        'B': 1,
        'C': 2
    }
    seats_array = np.array([[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]])

    assert show_seats(scr, seats_array, row_indices, None, 200, 300) is None
    assert show_seats(scr, seats_array, row_indices, 'movie', -200, 300) is None
    assert show_seats(scr, seats_array, row_indices, 'movie', 200, -300) is None
    assert show_seats(scr, seats_array, row_indices, 'movie', 200, 0) is None
    assert show_seats(scr, seats_array, row_indices, 'movie', 0, 20) is None

    empty_seats_array = np.array([])

    with pytest.raises(IncorrectArrayData):
        show_seats(scr, empty_seats_array, row_indices, 'movie', 20, 20)
