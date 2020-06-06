from menu import display_menu, main_menu
import curses


def test_display_menu():
    display_menu(curses.initscr(), 1, ['film1', 'film2', 'film3'])
    display_menu(curses.initscr(), 5, ['film1', 'film2', 'film3'])
    display_menu(curses.initscr(), 5, ('film1', 'film2', 'film3'))


def test_main_menu():
    main_menu(curses.initscr(), ['film1', 'film2', 'film3'])

    assert main_menu(curses.initscr(), []) is None
    assert main_menu(curses.initscr(), None) is None


