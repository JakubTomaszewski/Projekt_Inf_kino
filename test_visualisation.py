import pytest
from visualisation import (display_chosen_seats,
                           get_num_places,
                           book_seats,
                           display_text_info,
                           create_square,
                           display_row_indices,
                           display_key_info,
                           display_screen,
                           create_row,
                           display_image,
                           show_seats,
                           IncorrectlyChosenSeats
                           )


def test_display_chosen_seats():
    with pytest.raises(IncorrectlyChosenSeats):
        display_chosen_seats(34)

    with pytest.raises(IncorrectlyChosenSeats):
        display_chosen_seats(((1, 2, 3), (1, 2, 3)))

    assert display_chosen_seats(None) is None


def test_get_num_places():
    # INPUT
    pass


def test_book_seats():
    # INPUT
    pass


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


