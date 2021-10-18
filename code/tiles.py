import pygame
from helpers import import_sprite_sheet


class StaticTile(pygame.sprite.Sprite):
    def __init__(self, x, y, surface, collideable=True):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collideable = collideable
