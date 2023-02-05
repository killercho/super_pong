""" Main method for starting the game. """

from main_menu import Menu


def run_game() -> Menu:
    """Returns a menu object from which the game can be started."""
    return Menu()


if __name__ == "__main__":
    run_game()
