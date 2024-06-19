from data.power_up import PowerType


class PlayerPowerUps:
    def __init__(self) -> None:
        self.movement_speed = 2
        self.bomb_range = 1
        self.punch = False
        self.bomb_count = 2
        self.walk_through_bombs = False
    
    def power_up(self, power: PowerType):
        if power.value == PowerType.MOVEMENT_SPEED:
            self.movement_speed += 0.2
        elif power.value == PowerType.BOMB_RANGE:
            self.bomb_range += 1
        elif power.value == PowerType.PUNCH:
            self.punch = True
        elif power.value == PowerType.BOMB_COUNT:
            self.bomb_count += 1
        elif power.value == PowerType.WALK_THROUGH_BOMBS:
            self.walk_through_bombs = True
        