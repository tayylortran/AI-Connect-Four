import pygame
import sys
import src.ui.constants as C
from src.ai import MinimaxAI


class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse)
        color = self.hover_color if is_hovered else self.color

        pygame.draw.rect(screen, C.BLACK, self.rect.move(4, 4), border_radius=12)
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, C.WHITE, self.rect, 2, border_radius=12)

        label = C.FONT_MEDIUM.render(self.text, True, C.WHITE)
        lrect = label.get_rect(center=self.rect.center)
        screen.blit(label, lrect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN and
            self.rect.collidepoint(event.pos)
        )


def run_ai_select(screen):
    clock = pygame.time.Clock()

    btn_w, btn_h = 320, 70
    center_x = C.WIDTH // 2 - btn_w // 2

    btn_easy   = Button(center_x, 230, btn_w, btn_h, "Easy (depth 2)",   (30, 140, 80),  (50, 170, 100))
    btn_medium = Button(center_x, 330, btn_w, btn_h, "Medium (depth 5)", (160, 120, 20), (200, 155, 30))
    btn_hard   = Button(center_x, 430, btn_w, btn_h, "Hard (depth 8)",   (180, 80, 20),  (220, 110, 40))
    btn_back   = Button(center_x, 530, btn_w, btn_h, "Back",             (80, 80, 80),   (110, 110, 110))

    while True:
        clock.tick(60)
        screen.fill(C.DARK_GRAY)

        title = C.FONT_LARGE.render("Choose Difficulty", True, C.YELLOW)
        screen.blit(title, title.get_rect(center=(C.WIDTH // 2, 100)))

        sub = C.FONT_SMALL.render("Select a Minimax difficulty to play against", True, (180, 180, 180))
        screen.blit(sub, sub.get_rect(center=(C.WIDTH // 2, 160)))

        btn_easy.draw(screen)
        btn_medium.draw(screen)
        btn_hard.draw(screen)
        btn_back.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_easy.is_clicked(event):
                return MinimaxAI(depth=2)
            if btn_medium.is_clicked(event):
                return MinimaxAI(depth=5)
            if btn_hard.is_clicked(event):
                return MinimaxAI(depth=8)
            if btn_back.is_clicked(event):
                return None

        pygame.display.update()


def run_welcome(screen):
    clock = pygame.time.Clock()

    btn_w, btn_h = 320, 70
    center_x = C.WIDTH // 2 - btn_w // 2

    btn_pvp  = Button(center_x, 300, btn_w, btn_h, "Player vs Player", C.BLUE, (60, 130, 220))
    btn_cpu  = Button(center_x, 410, btn_w, btn_h, "Player vs CPU", (160, 30, 180), (190, 60, 210))
    btn_quit = Button(center_x, 520, btn_w, btn_h, "Quit", (180, 30, 30), (220, 60, 60))

    while True:
        clock.tick(60)
        screen.fill(C.DARK_GRAY)

        title = C.FONT_LARGE.render("Connect Four", True, C.YELLOW)
        trect = title.get_rect(center=(C.WIDTH // 2, 130))
        screen.blit(title, trect)

        sub = C.FONT_SMALL.render("Choose a game mode to begin", True, (180, 180, 180))
        srect = sub.get_rect(center=(C.WIDTH // 2, 210))
        screen.blit(sub, srect)

        pygame.draw.circle(screen, C.RED,    (80, 80), 40)
        pygame.draw.circle(screen, C.YELLOW, (C.WIDTH - 80, 80), 40)
        pygame.draw.circle(screen, C.BLUE,   (80, C.HEIGHT - 80), 40)
        pygame.draw.circle(screen, C.RED,    (C.WIDTH - 80, C.HEIGHT - 80), 40)

        btn_pvp.draw(screen)
        btn_cpu.draw(screen)
        btn_quit.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_pvp.is_clicked(event):
                return "pvp", None
            if btn_cpu.is_clicked(event):
                ai = run_ai_select(screen)
                if ai is not None:
                    return "cpu", ai
            if btn_quit.is_clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()