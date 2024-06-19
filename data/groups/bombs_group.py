import pygame
from data.game_state_information import GameStateInformation



class BombsGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def update(self, gameStateInformation: GameStateInformation):
        for sprite in self.sprites():
            sprite.update(gameStateInformation)
