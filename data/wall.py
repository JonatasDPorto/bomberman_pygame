import pygame

from assets.assets import Tile0
from config import GRID_SIZE, TILE_SIZE

class Wall(pygame.sprite.Sprite):
    
    def __init__(self, x, y, group):
        self.x = x
        self.y = y
        self.position, reverse = self.__get_tile_position__()
      
        if self.position:
            super().__init__(group)
            self.image = Tile0.get_tile(*self.position, flipped=reverse)
            self.rect = self.image.get_rect(topleft = (x*TILE_SIZE, y*TILE_SIZE))
        

    def __get_tile_position__(self):
        if self.y == 0:
            if (self.x == 0) or (self.x == GRID_SIZE - 1):
                return (0, 0), self.x != 0
            if (self.x == 1) or (self.x == GRID_SIZE - 2):
                return (1, 0),self.x != 1
            return (2, 0), False
        if self.y == 1:
            if (self.x == 0) or (self.x == GRID_SIZE - 1):
                return (0, 1), self.x != 0
            if (self.x == 1) or (self.x == GRID_SIZE - 2):
                return (1, 1),self.x != 1
            return None, None
        if self.y == GRID_SIZE - 1:
            if (self.x == 0) or (self.x == GRID_SIZE - 1):
                return (0, 4), self.x != 0
            if (self.x == 1) or (self.x == GRID_SIZE - 2):
                return (1, 4),self.x != 1
            return (2, 4), False
        if self.y == GRID_SIZE - 2:
            if (self.x == 0) or (self.x == GRID_SIZE - 1):
                return (0, 3), self.x != 0
            if (self.x == 1) or (self.x == GRID_SIZE - 2):
                return (1, 3),self.x != 1
            return  None, None
        if (self.x == 0) or (self.x == GRID_SIZE - 1):
                return (0, 1), self.x != 0
        if (self.x == 1) or (self.x == GRID_SIZE - 2):
            return (1, 2),self.x != 1
        if self.x % 2 == 1 and self.y % 2 == 0:
            return (4, 1), False
        return  None, None
