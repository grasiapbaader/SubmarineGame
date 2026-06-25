import pygame

from Code.Const import WIN_WIDTH, WIN_HEIGHT, C_WHITE, C_CYAN, C_GOLD


class Commands:
    def __init__(self, window):
        self.window = window

    def run(self):
        img = pygame.image.load('./asset/Commands.png')
        img_scaled = pygame.transform.scale(img, (WIN_WIDTH, WIN_HEIGHT))

        while True:
            self.window.blit(img_scaled, (0, 0))

            self.command_text("COMMANDS", 40, C_CYAN, (WIN_WIDTH // 2, 50))

            self.command_text("W - Move Up", 25, C_WHITE, (WIN_WIDTH // 2, 110))
            self.command_text("S - Move Down", 25, C_WHITE, (WIN_WIDTH // 2, 140))
            self.command_text("A - Move Left", 25, C_WHITE, (WIN_WIDTH // 2, 170))
            self.command_text("D - Move Right", 25, C_WHITE, (WIN_WIDTH // 2, 200))

            self.command_text("Collect treasures to earn points. Avoid sharks and explosives", 20, C_GOLD,
                              (WIN_WIDTH // 2, 260))
            self.command_text("ESC to go back", 20, C_WHITE, (WIN_WIDTH // 2, 285))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_RETURN:
                        return

    def command_text(self, text, size, color, center):
        font = pygame.font.SysFont("impact", size)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=center)
        self.window.blit(surf, rect)
