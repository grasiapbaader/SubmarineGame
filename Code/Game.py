import pygame

from Code.Commands import Commands
from Code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from Code.Menu import Menu
from Code.Level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in [MENU_OPTION[0]]:
                level = Level(self.window)
                level.run()
            elif menu_return in [MENU_OPTION[1]]:
                commands = Commands(self.window)
                commands.run()
            elif menu_return in [MENU_OPTION[2]]:
                pygame.quit()
                quit()
