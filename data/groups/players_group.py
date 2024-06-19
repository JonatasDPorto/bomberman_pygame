import pygame
from data.game_state_information import GameStateInformation



class PlayersGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def update(self, gameStateInformation: GameStateInformation, collision_groups):
        for sprite in self.sprites():
            sprite.update(gameStateInformation, collision_groups)
