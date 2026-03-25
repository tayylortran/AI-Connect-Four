import pygame
import sys
import src.ui.constants as C
from src.connect4 import (
    create_board, drop_piece, is_valid_location,
    get_next_open_row, winning_move, ROWS, COLS,
    PLAYER_PIECE, AI_PIECE, EMPTY
)


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


def run_game(screen, mode):
    clock = pygame.time.Clock()
    board = create_board()
    game_over = False
    turn = PLAYER_PIECE
    hover_col = COLS // 2

    while True:
        clock.tick(60)
        screen.fill(C.GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    return "menu"

            if not game_over:
                if event.type == pygame.MOUSEMOTION:
                    hover_col = event.pos[0] // C.SQUARESIZE
                    hover_col = max(0, min(COLS - 1, hover_col))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // C.SQUARESIZE
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, turn)

                        if winning_move(board, turn):
                            game_over = True
                        else:
                            turn = AI_PIECE if turn == PLAYER_PIECE else PLAYER_PIECE

        draw_board(screen, board)

        if not game_over:
            draw_hover(screen, hover_col, turn)
            if mode == "pvp":
                name = "Player 1 (Red)" if turn == PLAYER_PIECE else "Player 2 (Yellow)"
            else:
                name = "Your turn (Red)" if turn == PLAYER_PIECE else "CPU thinking..."
            label = C.FONT_SMALL.render(name, True, C.WHITE)
            screen.blit(label, (10, 8))
        else:
            if mode == "pvp":
                winner = "Player 1 (Red)" if turn == PLAYER_PIECE else "Player 2 (Yellow)"
            else:
                winner = "You win!" if turn == PLAYER_PIECE else "CPU wins!"
            color = C.RED if turn == PLAYER_PIECE else C.YELLOW
            show_message(screen, f"{winner}  |  R=Restart  ESC=Menu", color)

        pygame.display.update()