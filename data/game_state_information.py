import numpy as np
import pygame

from config import GRID_SIZE, TILE_SIZE

class GameStateInformation:
    def __init__(self, trigger_next_frame, destroyables_group, players_group, walls_group, bombs_groups) -> None:
        self.trigger_next_frame = trigger_next_frame
        self.destroyable_matrix = np.zeros((GRID_SIZE, GRID_SIZE))
        self.players_matrix = np.zeros((GRID_SIZE, GRID_SIZE))
        self.walls_matrix = np.zeros((GRID_SIZE, GRID_SIZE))
        self.bombs_matrix = np.zeros((GRID_SIZE, GRID_SIZE))

        self.__generate_matrix_of_group__(self.destroyable_matrix, destroyables_group)
        self.__generate_matrix_of_group__(self.players_matrix, players_group)
        self.__generate_matrix_of_group__(self.walls_matrix, walls_group)
        self.__generate_matrix_of_group__(self.bombs_matrix, bombs_groups)


    def __generate_matrix_of_group__(self, matrix, group):
        for sprite in group.sprites():
            position = sprite.rect.topleft
            x = position[0] // TILE_SIZE
            y = position[1] // TILE_SIZE
            if (0 >= x < GRID_SIZE) and (0 >= x < GRID_SIZE):
                matrix[x][y] = 1
        
