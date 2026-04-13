import pygame
import sys
import src.ui.constants as C
from src.connect4 import (
    create_board, drop_piece, is_valid_location,
    get_next_open_row, get_valid_locations, winning_move,
    ROWS, COLS, PLAYER_PIECE, AI_PIECE
)
from src.ai import pick_best_move
from src.ui.game import draw_board, draw_hover, show_message


def run_game(screen, mode):
    clock = pygame.time.Clock()
    board = create_board()
    game_over = False
    winner_piece = None
    is_draw = False
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

                if (
                    event.type == pygame.MOUSEBUTTONDOWN and
                    (mode == "pvp" or turn == PLAYER_PIECE)
                ):
                    col = event.pos[0] // C.SQUARESIZE
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, turn)

                        if winning_move(board, turn):
                            game_over = True
                            winner_piece = turn
                        elif not get_valid_locations(board):
                            game_over = True
                            is_draw = True
                        else:
                            turn = AI_PIECE if turn == PLAYER_PIECE else PLAYER_PIECE

        if mode == "cpu" and not game_over and turn == AI_PIECE:
            draw_board(screen, board)
            pygame.display.update()
            pygame.time.wait(500)
            col = pick_best_move(board, AI_PIECE)

            if col is None:
                game_over = True
                is_draw = True
            elif is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    game_over = True
                    winner_piece = AI_PIECE
                elif not get_valid_locations(board):
                    game_over = True
                    is_draw = True
                else:
                    turn = PLAYER_PIECE

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
            if is_draw:
                winner = "Draw game!"
                color = C.WHITE
            elif mode == "pvp":
                winner = "Player 1 (Red)" if winner_piece == PLAYER_PIECE else "Player 2 (Yellow)"
                color = C.RED if winner_piece == PLAYER_PIECE else C.YELLOW
            else:
                winner = "You win!" if winner_piece == PLAYER_PIECE else "CPU wins!"
                color = C.RED if winner_piece == PLAYER_PIECE else C.YELLOW
            show_message(screen, f"{winner}  |  R=Restart  ESC=Menu", color)

        pygame.display.update()
