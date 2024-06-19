import pygame

from assets.assets import Tile0


class Ground(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.image = Tile0.get_tile(4, 0)
        self.rect = self.image.get_rect(topleft = position)
