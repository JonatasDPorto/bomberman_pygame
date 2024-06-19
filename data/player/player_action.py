
from data.directions import Direction


class PlayerAction:
    pass

class StopAction(PlayerAction):
    def __init__(self) -> None:
        super().__init__()

class MoveAction(PlayerAction):
    def __init__(self, direction: Direction) -> None:
        super().__init__()
        self.direction: Direction = direction

class PunchAction(PlayerAction):
    def __init__(self, direction: Direction) -> None:
        super().__init__()
        self.direction: Direction = direction

class PlaceBombAction(PlayerAction):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.position: tuple = (x, y)

