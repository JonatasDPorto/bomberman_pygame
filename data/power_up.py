from enum import IntEnum
import pygame


class PowerType(IntEnum):
    MOVEMENT_SPEED = 0
    BOMB_RANGE = 1
    PUNCH = 2
    BOMB_COUNT = 3
    WALK_THROUGH_BOMBS = 4

    def get_values():
        return list(map(int, PowerType))


class PowerUp(pygame.sprite.Sprite):

    def __init__(self, group, powerType: PowerType):
        super().__init__(group)
        self.powerType = powerType