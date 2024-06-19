import pygame


class Tile0:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Tile0, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.grid = []
        self.flipped_grid = []
  
    def load_surfaces(self):
        asset = pygame.image.load('assets/tile_0.png')
        for y in range(13):
            row = []
            flipped_row = []
            for x in range(9):
                dx = 1 + x + (16*x)
                dy = 1 + y + (16*y)
                surface = pygame.Surface((16, 16), pygame.SRCALPHA)
                surface.blit(asset, (0, 0), (dx, dy, 16, 16))
                flipped_surface = pygame.transform.flip(surface, True, False)
                row.append(surface)
                flipped_row.append(flipped_surface)
            self.grid.append(row)
            self.flipped_grid.append(flipped_row)

    def get_tile(x, y, flipped=False):
        if flipped:
            return Tile0._instance.flipped_grid[y][x]
        return Tile0._instance.grid[y][x]



class Chars:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Chars, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.grid = []
        self.flipped_grid = []
  
    def load_surfaces(self):
        asset = pygame.image.load('assets/chars.png').convert_alpha()
        for y in range(4):
            row = []
            flipped_row = []
            for x in range(27):
                dx = 1 + x + (17*x)
                dy = 1 + y + (25*y)
                surface = pygame.Surface((17, 25), pygame.SRCALPHA)
                surface.blit(asset, (0, 0), (dx, dy, 17, 25))
                flipped_surface = pygame.transform.flip(surface, True, False)
                row.append(surface)
                flipped_row.append(flipped_surface)
            self.grid.append(row)
            self.flipped_grid.append(flipped_row)

    def get_tile(player_id, animation_id, animation_frame_id, flipped=False):
        x = (animation_id * 3) + animation_frame_id
        y = player_id
        if flipped:
            return Chars._instance.flipped_grid[y][x]
        return Chars._instance.grid[y][x]



def init_assets():
    Tile0().load_surfaces()
    Chars().load_surfaces()