import numpy as np
import pygame

from config import GRID_SIZE, TILE_SIZE
from data.directions import Direction

class GameStateInformation:
    def __init__(self, trigger_next_frame, destroyables_group, players_group, walls_group, bombs_groups, explosion_group) -> None:
        self.trigger_next_frame = trigger_next_frame
        self.destroyable_matrix = np.zeros((GRID_SIZE, GRID_SIZE))
        self.players_matrix = np.zeros((GRID_SIZE, GRID_SIZE))
        self.walls_matrix = np.zeros((GRID_SIZE, GRID_SIZE))
        self.bombs_matrix = np.zeros((GRID_SIZE, GRID_SIZE))
        self.danger_zone_matrix = np.zeros((GRID_SIZE, GRID_SIZE))

        self.__generate_matrix_of_destroyable__(destroyables_group)
        self.__generate_matrix_of_players__(players_group)
        self.__generate_matrix_of_group__(self.walls_matrix, walls_group)
        self.__generate_matrix_of_group__(self.bombs_matrix, bombs_groups)
        self.__generate_matrix_of_danger_zone__(bombs_groups, explosion_group)


    def __generate_matrix_of_group__(self, matrix, group):
        for sprite in group.sprites():
            position = sprite.rect.topleft
            x = position[0] // TILE_SIZE
            y = position[1] // TILE_SIZE
            if (0 <= x < GRID_SIZE) and (0 <= y < GRID_SIZE):
                matrix[x][y] = 1

    def __generate_matrix_of_players__(self, group):
        for sprite in group.sprites():
            x, y = sprite.get_position_in_grid()
            if (0 <= x < GRID_SIZE) and (0 <= y < GRID_SIZE):
                self.players_matrix[x][y] = 1
        

    def __generate_matrix_of_destroyable__(self, group):
        for sprite in group.sprites():
            if sprite.is_destroying:
                continue
            position = sprite.rect.topleft
            x = position[0] // TILE_SIZE
            y = position[1] // TILE_SIZE
            if (0 <= x < GRID_SIZE) and (0 <= y < GRID_SIZE):
                self.destroyable_matrix[x][y] = 1


    def __create_danger_in_direction__(self, x, y, direction, bomb_range, block_matrix):
        for eid in range(1, bomb_range+1):
            xx = x
            yy = y
            if direction == Direction.DOWN:
                yy += eid
            elif direction == Direction.UP:
                yy -= eid
            elif direction == Direction.LEFT:
                xx -= eid
            elif direction == Direction.RIGHT:
                xx += eid
            if block_matrix[xx][yy] == 1.0:
                break
            self.danger_zone_matrix[xx][yy] = 1

    def __create_block_matrix__(self):
        return np.logical_or(self.destroyable_matrix, self.walls_matrix).astype(int)

    def __generate_matrix_of_danger_zone__(self, bombs_groups, explosion_group):
        block_matrix = self.__create_block_matrix__()
        for bomb_sprite in bombs_groups.sprites():
            bomb_range = bomb_sprite.player.power_ups.bomb_range
            x, y = bomb_sprite.rect.topleft
            dx, dy = x // TILE_SIZE, y // TILE_SIZE
            self.danger_zone_matrix[dx][dy] = 1
            self.__create_danger_in_direction__(dx, dy, Direction.DOWN, bomb_range, block_matrix)

        for explosion in explosion_group.sprites():
            x, y = explosion.rect.topleft
            dx, dy = x // TILE_SIZE, y // TILE_SIZE
            self.danger_zone_matrix[dx][dy] = 1
        

        
