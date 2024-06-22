import numpy as np
import pygame

from config import GRID_SIZE, TILE_SIZE
from data.directions import Direction
from data.player.player_power_ups import PlayerPowerUps

class PlayerStateInformation:
    def __init__(self, x: int, y: int, direction: Direction, power_ups: PlayerPowerUps, current_bombs_in_ground: int) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.power_ups = power_ups
        self.current_bombs_in_ground = current_bombs_in_ground

