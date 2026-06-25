import random
import pygame
from pygame.surface import Surface
from pygame.font import Font
from pygame.rect import Rect

from Code.Const import (WIN_WIDTH, WIN_HEIGHT, MAX_DEPTH, SUB_MAX_LIFE,
                        SHARK_DAMAGE, MINE_DAMAGE, TREASURE_SCORE,
                        SHARK_SPAWN, MINE_SPAWN, TREASURE_SPAWN,
                        SCROLL_SPEED,
                        C_WHITE, C_RED, C_YELLOW, C_GREEN, C_DARK_BLUE, C_GOLD, C_GRAY,
                        )
from Code.EntityFactory import make


class Level:
    def __init__(self, window: Surface):
        self.window = window

        img = pygame.image.load('./asset/Underwater2.png').convert()
        img_scaled = pygame.transform.scale(img, (WIN_WIDTH, WIN_HEIGHT))
        self.bg_surf = pygame.Surface((WIN_WIDTH, WIN_HEIGHT * 2))
        self.bg_surf.blit(img_scaled, (0, 0))
        self.bg_surf.blit(img_scaled, (0, WIN_HEIGHT))
        self.bg_y = 0

        pygame.mixer.music.load('./asset/StartGame.mp3')
        pygame.mixer.music.play(-1)

        self.sub_surf = make('submarine')
        self.sub_rect = self.sub_surf.get_rect(
            centerx=WIN_WIDTH // 2,
            centery=WIN_HEIGHT // 2
        )

        self.sub_life = SUB_MAX_LIFE

        self.sharks = []
        self.mines = []
        self.treasures = []

        self.shark_timer = SHARK_SPAWN
        self.mine_timer = MINE_SPAWN
        self.treasure_timer = TREASURE_SPAWN

        self.depth = 0
        self.score = 0

        self.invuln = 0

        self.font_hud = pygame.font.SysFont('impact', 22)
        self.font_big = pygame.font.SysFont('impact', 48)
        self.font_small = pygame.font.SysFont('impact', 18)

        self.clock = pygame.time.Clock()

    def level_text(self, size: int, text: str, color: tuple, pos: tuple):
        font: Font = pygame.font.SysFont('impact', size)
        surf: Surface = font.render(text, True, color).convert_alpha()
        rect: Rect = surf.get_rect(left=pos[0], top=pos[1])
        self.window.blit(surf, rect)

    def level_text_center(self, size: int, text: str, color: tuple, center: tuple):
        font: Font = pygame.font.SysFont('impact', size)
        surf: Surface = font.render(text, True, color).convert_alpha()
        rect: Rect = surf.get_rect(center=center)
        self.window.blit(surf, rect)

    def spawn_shark(self):
        surf = make('shark')

        rect = surf.get_rect(
            left=random.randint(0, WIN_WIDTH - surf.get_width()),
            top=-surf.get_height()
        )

        direction = random.choice([-1, 1])
        if direction == 1:
            surf = pygame.transform.flip(surf, True, False)
        self.sharks.append({'surf': surf, 'rect': rect, 'direction': direction})

    def spawn_mine(self):
        surf = make('mine')
        rect = surf.get_rect(
            left=random.randint(20, WIN_WIDTH - surf.get_width() - 20),
            top=-surf.get_height()
        )
        self.mines.append({'surf': surf, 'rect': rect, 'tick': 0})

    def spawn_treasure(self):
        surf = make('treasure')
        rect = surf.get_rect(
            left=random.randint(20, WIN_WIDTH - surf.get_width() - 20),
            top=-surf.get_height()
        )
        self.treasures.append({'surf': surf, 'rect': rect})

    def move_sharks(self):
        for shark in self.sharks:
            shark['rect'].x += shark['direction'] * 2
            if shark['rect'].right >= WIN_WIDTH or shark['rect'].left <= 0:
                shark['direction'] *= -1
                shark['surf'] = pygame.transform.flip(shark['surf'], True, False)
            shark['rect'].y += SCROLL_SPEED

    def move_mines(self):
        for mine in self.mines:
            mine['tick'] += 1
            if mine['tick'] % 60 < 30:
                mine['rect'].y += 1
            else:
                mine['rect'].y -= 1
            mine['rect'].y += SCROLL_SPEED

    def move_treasures(self):
        for treasure in self.treasures:
            treasure['rect'].y += SCROLL_SPEED

    def draw_background(self):
        y0 = self.bg_y % (WIN_HEIGHT * 2)
        self.window.blit(self.bg_surf, (0, y0 - WIN_HEIGHT * 2))
        self.window.blit(self.bg_surf, (0, y0))

    def draw_hud(self):
        bar_w = 200
        bar_h = 30
        ratio = max(0, self.sub_life / SUB_MAX_LIFE)
        bar_x = 10
        bar_y = 10

        pygame.draw.rect(self.window, (30, 30, 60),
                         (bar_x, bar_y, bar_w, bar_h), border_radius=4)

        if ratio > 0.5:
            cor = C_GREEN
        elif ratio > 0.25:
            cor = C_YELLOW
        else:
            cor = C_RED

        pygame.draw.rect(self.window, cor,
                         (bar_x, bar_y, int(bar_w * ratio), bar_h), border_radius=4)
        pygame.draw.rect(self.window, C_WHITE,
                         (bar_x, bar_y, bar_w, bar_h), 2, border_radius=4)

        self.level_text(20, f' {self.sub_life}/{SUB_MAX_LIFE}', C_WHITE, (bar_x + 5, bar_y + 1))

        depth_surf = self.font_hud.render(f'{int(self.depth)}m', True, C_WHITE)
        self.window.blit(depth_surf, (WIN_WIDTH - depth_surf.get_width() - 8, 8))

        score_surf = self.font_hud.render(f'Score: {self.score}', True, C_GOLD)
        self.window.blit(score_surf, (8, WIN_HEIGHT - 30))

    def show_result(self, won: bool):
        self.window.fill(C_DARK_BLUE)

        if won:
            self.level_text_center(48, 'YOU WIN!', C_GOLD, (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 80))
        else:
            self.level_text_center(48, 'GAME OVER', C_RED, (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 80))

        self.level_text_center(22, f'Depth: {int(self.depth)} m', C_WHITE,
                               (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 10))
        self.level_text_center(22, f'Final Score: {self.score}', C_WHITE,
                               (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 25))
        self.level_text_center(18, 'Press ENTER to return menu', C_GRAY,
                               (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 70))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        waiting = False

    def run(self):
        while True:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'menu'

            keys = pygame.key.get_pressed()

            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.sub_rect.left > 0:
                self.sub_rect.x -= 3
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.sub_rect.right < WIN_WIDTH:
                self.sub_rect.x += 3
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.sub_rect.top > 0:
                self.sub_rect.y -= 3
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.sub_rect.bottom < WIN_HEIGHT:
                self.sub_rect.y += 3

            self.bg_y += SCROLL_SPEED
            self.depth += SCROLL_SPEED

            self.shark_timer -= 1
            if self.shark_timer <= 0:
                self.spawn_shark()
                self.shark_timer = SHARK_SPAWN

            self.mine_timer -= 1
            if self.mine_timer <= 0:
                self.spawn_mine()
                self.mine_timer = MINE_SPAWN

            self.treasure_timer -= 1
            if self.treasure_timer <= 0:
                self.spawn_treasure()
                self.treasure_timer = TREASURE_SPAWN

            self.move_sharks()
            self.move_mines()
            self.move_treasures()

            if self.invuln <= 0:
                for shark in self.sharks[:]:
                    if self.sub_rect.colliderect(shark['rect']):
                        self.sub_life -= SHARK_DAMAGE
                        self.sharks.remove(shark)
                        self.invuln = 45
                        break

            if self.invuln <= 0:
                for mine in self.mines[:]:
                    if self.sub_rect.colliderect(mine['rect']):
                        self.sub_life -= MINE_DAMAGE
                        self.mines.remove(mine)
                        self.invuln = 60
                        break

            for treasure in self.treasures[:]:
                if self.sub_rect.colliderect(treasure['rect']):
                    self.score += TREASURE_SCORE  # adiciona pontos
                    self.treasures.remove(treasure)

            if self.invuln > 0:
                self.invuln -= 1

            self.sharks = [s for s in self.sharks if s['rect'].top < WIN_HEIGHT + 60]
            self.mines = [m for m in self.mines if m['rect'].top < WIN_HEIGHT + 60]
            self.treasures = [t for t in self.treasures if t['rect'].top < WIN_HEIGHT + 60]

            if self.sub_life <= 0:
                self.show_result(won=False)
                return 'menu'
            if self.depth >= MAX_DEPTH:
                self.show_result(won=True)
                return 'menu'

            self.draw_background()

            for shark in self.sharks:
                self.window.blit(shark['surf'], shark['rect'])
            for mine in self.mines:
                self.window.blit(mine['surf'], mine['rect'])
            for treasure in self.treasures:
                self.window.blit(treasure['surf'], treasure['rect'])

            self.window.blit(self.sub_surf, self.sub_rect)

            self.draw_hud()

            pygame.display.flip()
