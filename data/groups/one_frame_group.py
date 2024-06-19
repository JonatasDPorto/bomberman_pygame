import pygame
from config import GAME_WINDOW_SIZE


class OneFrameGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(GAME_WINDOW_SIZE, pygame.SRCALPHA)

    def build(self):
        for sprite in self.sprites():
            self.surface.blit(sprite.image, sprite.rect)

    def draw(self, surface):
        surface.blit(self.surface, (0, 0))