import pygame.image
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface

from Code.Const import WIN_WIDTH, C_WHITE, MENU_OPTION, C_BLUE, C_GOLD


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/Menu.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self, ):
        menu_option = 0
        pygame.mixer.music.load('./asset/Menu.mp3')
        pygame.mixer.music.play(-1)
        while True:
            # DRAW IMAGES
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(60, "SUBMARINE", C_WHITE, ((WIN_WIDTH / 2), 70))
            self.menu_text(60, "GAME", C_WHITE, ((WIN_WIDTH / 2), 130))
            self.menu_text(30, "Objective: reach a depth of 2000m", C_GOLD, (WIN_WIDTH / 2, 300))

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(25, MENU_OPTION[i], C_BLUE, ((WIN_WIDTH / 2), 200 + 30 * i))
                else:
                    self.menu_text(25, MENU_OPTION[i], C_WHITE, ((WIN_WIDTH / 2), 200 + 30 * i))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="impact", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)
