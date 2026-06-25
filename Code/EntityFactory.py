import pygame
from pygame.surface import Surface


def _make_submarine() -> Surface:
    img = pygame.image.load('./asset/Submarine.png').convert_alpha()
    return pygame.transform.scale(img, (80, 40))


def _make_shark() -> Surface:
    img = pygame.image.load('./asset/Shark.png').convert_alpha()
    return pygame.transform.scale(img, (70, 30))


def _make_mine() -> Surface:
    img = pygame.image.load('./asset/Dynamite.png').convert_alpha()
    return pygame.transform.scale(img, (30, 30))


def _make_treasure() -> Surface:
    img = pygame.image.load('./asset/Treasure.png').convert_alpha()
    return pygame.transform.scale(img, (36, 28))


BUILDERS = {
    'submarine': _make_submarine,
    'shark': _make_shark,
    'mine': _make_mine,
    'treasure': _make_treasure,
}


def make(name: str) -> Surface:
    builder = BUILDERS.get(name)
    if builder is None:
        raise ValueError(f"Unknown entity: {name}")
    return builder()
