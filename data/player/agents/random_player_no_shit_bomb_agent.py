
from enum import Enum
import random
import pygame
from config import GRID_SIZE
from data.directions import Direction
from data.game_state_information import GameStateInformation
from data.player.agents.player_agent import PlayerAgent
from data.player.player import Player
from data.player.player_action import MoveAction, PlaceBombAction, PlayerAction, PunchAction, StopAction
from data.player_state_information import PlayerStateInformation


class RandomPlayerNoShitBombAgent(PlayerAgent):
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

    def act(self, playerStateInformation: PlayerStateInformation, gameStateInformation: GameStateInformation) -> PlayerAction:

        actions = [
            PlaceBombAction(playerStateInformation.x, playerStateInformation.y),
            MoveAction(Direction.LEFT),
            MoveAction(Direction.RIGHT),
            MoveAction(Direction.UP),
            MoveAction(Direction.DOWN),
            StopAction()
        ]
        if self.__has_destroyable_around__(playerStateInformation.x, playerStateInformation.y, gameStateInformation.destroyable_matrix) and playerStateInformation.current_bombs_in_ground < playerStateInformation.power_ups.bomb_count:
            return actions[0]

            
        weights = [0, 0, 22, 22, 22, 22, 11]
        

        return random.choices(actions, weights=weights)[0]

        
        
    