from menu import display_menu
import curses


def test_display_menu():
    display_menu(curses.initscr(), 5)

test_display_menu()