import pygame
import src.ui.constants as C
from src.connect4 import ROWS, COLS, PLAYER_PIECE, AI_PIECE, EMPTY


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
