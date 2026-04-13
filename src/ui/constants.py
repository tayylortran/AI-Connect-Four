import pygame

# Board
ROWS = 6
COLS = 7
SQUARESIZE = 100
RADIUS = SQUARESIZE // 2 - 6
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
TREE_PANEL_WIDTH = 650
SIZE = (WIDTH + TREE_PANEL_WIDTH, HEIGHT)

# Colors
BLACK     = (0,   0,   0)
WHITE     = (255, 255, 255)
BLUE      = (30,  100, 200)
RED       = (220, 50,  50)
YELLOW    = (240, 200, 0)
DARK_BLUE = (15,  50,  120)
GRAY      = (40,  40,  40)
DARK_GRAY = (25,  25,  25)
HOVER     = (70,  70,  70)

# Fonts (call init_fonts() after pygame.init())
FONT_LARGE  = None
FONT_MEDIUM = None
FONT_SMALL  = None
FONT_TINY   = None

def init_fonts():
    global FONT_LARGE, FONT_MEDIUM, FONT_SMALL, FONT_TINY
    FONT_LARGE  = pygame.font.SysFont("segoeui", 64, bold=True)
    FONT_MEDIUM = pygame.font.SysFont("segoeui", 36, bold=True)
    FONT_SMALL  = pygame.font.SysFont("segoeui", 26)
    FONT_TINY   = pygame.font.SysFont("segoeui", 11)