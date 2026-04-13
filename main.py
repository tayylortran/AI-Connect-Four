import pygame
from src.ui.constants import SIZE, init_fonts
from src.ui.welcome import run_welcome
from src.game_loop import run_game


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("AI Connect Four")
    init_fonts()

    while True:
        mode = run_welcome(screen)        # "pvp" or "cpu"
        result = run_game(screen, mode)   # "restart" or "menu"
        # "restart" loops back to game, "menu" loops back to welcome
        while result == "restart":
            result = run_game(screen, mode)


if __name__ == "__main__":
    main()