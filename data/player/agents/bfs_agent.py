from collections import deque
import numpy as np
from config import GRID_SIZE
from data.directions import Direction
from data.game_state_information import GameStateInformation
from data.player.agents.player_agent import PlayerAgent
from data.player.player import Player
from data.player.player_action import MoveAction, PlaceBombAction, PlayerAction, PunchAction, StopAction
from data.player_state_information import PlayerStateInformation


class BFSAgent(PlayerAgent):
    def __init__(self) -> None:
        super().__init__()

    def __has_destroyable_around__(self, x, y, matrix):
        if x > 0:
            if matrix[x - 1][y]:
                return True
        if x < GRID_SIZE - 1:
            if matrix[x + 1][y]:
                return True
        if y > 0:
            if matrix[x][y - 1]:
                return True
        if y < GRID_SIZE - 1:
            if matrix[x][y + 1]:
                return True
        return False
    

    def bfs(self, matrix, obstacles, start_row, start_col):
        rows, cols = matrix.shape
        visited = np.zeros_like(matrix, dtype=bool)
        queue = deque([(start_row, start_col, [(start_row, start_col)])])
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            row, col, path = queue.popleft()
            if matrix[row, col] == 1:
                return path

            visited[row, col] = True
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < rows and 0 <= new_col < cols and not visited[new_row, new_col] and obstacles[new_row, new_col] == 0:
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_path))

        return None
    
    def start_bfs(self, matrix, obstacles, x, y):
        result_path = self.bfs(matrix, obstacles, x, y)
        if result_path:
            if len(result_path) > 1:
                dx = result_path[1][0] - result_path[0][0]
                dy = result_path[1][1] - result_path[0][1]
                if dx != 0:
                    if dx > 0:
                        return Direction.RIGHT
                    return Direction.LEFT
                else:
                    if dy > 0:
                        return Direction.DOWN
                    return Direction.UP
    
        return None


    def act(self, playerStateInformation: PlayerStateInformation, gameStateInformation: GameStateInformation) -> PlayerAction:

        x, y = playerStateInformation.x, playerStateInformation.y
        
        actions = [
            PlaceBombAction(x, y),
            MoveAction(Direction.LEFT),
            MoveAction(Direction.RIGHT),
            MoveAction(Direction.UP),
            MoveAction(Direction.DOWN),
            StopAction()
        ]
        if self.__has_destroyable_around__(x, y, gameStateInformation.destroyable_matrix) and playerStateInformation.current_bombs_in_ground < playerStateInformation.power_ups.bomb_count:
            return actions[0]

        next_move = self.start_bfs(gameStateInformation.destroyable_matrix, gameStateInformation.walls_matrix, x, y)

        if next_move:
            return MoveAction(next_move)
        
        return StopAction()
        
        
    