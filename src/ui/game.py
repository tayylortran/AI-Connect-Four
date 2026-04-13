import pygame
import sys
import src.ui.constants as C
from src.connect4 import (
    create_board, drop_piece, is_valid_location,
    get_next_open_row, get_valid_locations, winning_move,
    pick_best_move, ROWS, COLS, PLAYER_PIECE, AI_PIECE, EMPTY
)


def _count_leaves(node):
    if not node.children:
        return 1
    return sum(_count_leaves(c) for c in node.children)


def _layout(node, x0, x1, y, y_step, pos):
    pos[id(node)] = (int((x0 + x1) / 2), int(y))
    if not node.children:
        return
    total = _count_leaves(node)
    x = x0
    for child in node.children:
        share = (x1 - x0) * _count_leaves(child) / total
        _layout(child, x, x + share, y + y_step, y_step, pos)
        x += share


def _score_color(score):
    if score is None:
        return (80, 80, 80)
    clamped = max(-300, min(300, score))
    t = (clamped + 300) / 600  # 0.0 = red, 1.0 = green
    return (int(220 * (1 - t)), int(180 * t), 30)


def draw_tree(screen, root):
    px = C.WIDTH
    pw = C.TREE_PANEL_WIDTH
    ph = C.HEIGHT

    pygame.draw.rect(screen, (22, 22, 22), (px, 0, pw, ph))
    pygame.draw.line(screen, (60, 60, 60), (px, 0), (px, ph), 2)

    title = C.FONT_SMALL.render("Minimax Tree (depth 3)", True, C.WHITE)
    screen.blit(title, (px + 10, 8))

    if root is None:
        msg = C.FONT_SMALL.render("Waiting for CPU turn...", True, (120, 120, 120))
        screen.blit(msg, (px + 10, ph // 2))
        return

    margin = 10
    y_top = 50
    y_step = (ph - y_top - 60) / 3

    pos = {}
    _layout(root, px + margin, px + pw - margin, y_top, y_step, pos)

    # Edges
    def draw_edges(node):
        if id(node) not in pos:
            return
        nx, ny = pos[id(node)]
        for child in node.children:
            if id(child) not in pos:
                continue
            cx, cy = pos[id(child)]
            color = (55, 55, 55) if child.pruned else (100, 100, 100)
            pygame.draw.line(screen, color, (nx, ny), (cx, cy), 1)
            draw_edges(child)

    draw_edges(root)

    # Nodes
    radii = [16, 12, 8, 6]

    def draw_nodes(node, depth):
        if id(node) not in pos:
            return
        x, y = pos[id(node)]
        r = radii[min(depth, len(radii) - 1)]

        if node.pruned:
            fill = (45, 45, 45)
            border = (75, 75, 75)
        else:
            fill = _score_color(node.score)
            border = C.YELLOW if node.maximizing else C.RED

        pygame.draw.circle(screen, fill, (x, y), r)
        pygame.draw.circle(screen, border, (x, y), r, 2)

        if not node.pruned and node.score is not None and depth <= 1 and C.FONT_TINY:
            s = node.score
            text = "W" if s >= 1000000 else ("L" if s <= -1000000 else str(s))
            lbl = C.FONT_TINY.render(text, True, C.WHITE)
            screen.blit(lbl, lbl.get_rect(center=(x, y)))

        if depth == 1 and node.col is not None and C.FONT_TINY:
            lbl = C.FONT_TINY.render(f"col {node.col}", True, (180, 180, 180))
            screen.blit(lbl, lbl.get_rect(center=(x, y - r - 7)))

        for child in node.children:
            draw_nodes(child, depth + 1)

    draw_nodes(root, 0)

    # Legend
    ly = ph - 75
    items = [
        (C.YELLOW, "AI move (maximizing)"),
        (C.RED,    "Player move (minimizing)"),
        ((75, 75, 75), "Pruned (alpha-beta)"),
    ]
    for i, (color, label) in enumerate(items):
        lx = px + 16
        cy = ly + i * 22
        pygame.draw.circle(screen, color, (lx, cy), 6)
        lbl = C.FONT_TINY.render(label, True, (180, 180, 180))
        screen.blit(lbl, (lx + 12, cy - 6))


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
    winner_piece = None
    is_draw = False
    turn = PLAYER_PIECE
    hover_col = COLS // 2
    tree_root = None

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
            draw_tree(screen, tree_root)
            pygame.display.update()
            pygame.time.wait(500)
            col, tree_root = pick_best_move(board, AI_PIECE)

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
        if mode == "cpu":
            draw_tree(screen, tree_root)

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
