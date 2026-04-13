import pygame
import src.ui.constants as C
from src.connect4 import ROWS, COLS, PLAYER_PIECE, AI_PIECE, EMPTY


def draw_board(screen, board):
    pygame.draw.rect(screen, C.BLUE, (0, C.SQUARESIZE, C.WIDTH, ROWS * C.SQUARESIZE), border_radius=12)

    for r in range(ROWS):
        for c in range(COLS):
            cx = c * C.SQUARESIZE + C.SQUARESIZE // 2
            cy = (r + 1) * C.SQUARESIZE + C.SQUARESIZE // 2

            piece = board[r][c]
            if piece == EMPTY:
                color = C.DARK_BLUE
            elif piece == PLAYER_PIECE:
                color = C.RED
            else:
                color = C.YELLOW

            pygame.draw.circle(screen, C.BLACK, (cx + 2, cy + 2), C.RADIUS)
            pygame.draw.circle(screen, color, (cx, cy), C.RADIUS)

            if piece != EMPTY:
                pygame.draw.circle(screen, C.WHITE,
                                   (cx - C.RADIUS // 4, cy - C.RADIUS // 4), C.RADIUS // 5)


def draw_hover(screen, col, turn):
    color = C.RED if turn == PLAYER_PIECE else C.YELLOW
    cx = col * C.SQUARESIZE + C.SQUARESIZE // 2
    cy = C.SQUARESIZE // 2
    pygame.draw.circle(screen, color, (cx, cy), C.RADIUS)


def show_message(screen, text, color):
    overlay = pygame.Surface((C.WIDTH, C.SQUARESIZE), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    label = C.FONT_LARGE.render(text, True, color)
    rect = label.get_rect(center=(C.WIDTH // 2, C.SQUARESIZE // 2))
    screen.blit(label, rect)
