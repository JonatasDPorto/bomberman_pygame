
from enum import Enum
import pygame
from data.directions import Direction
from data.game_state_information import GameStateInformation
from data.player.agents.player_agent import PlayerAgent
from data.player.player import Player
from data.player.player_action import MoveAction, PlaceBombAction, PlayerAction, PunchAction, StopAction

class DefaultPlayerAgentKeyboardType(Enum):
    WASD = 0
    ARROWS = 1


class DefaultPlayerAgent(PlayerAgent):
    def __init__(self, keyboard_type: DefaultPlayerAgentKeyboardType) -> None:
        super().__init__()
        self.keyboard_type = keyboard_type

    def act(self, player: Player, gameStateInformation: GameStateInformation) -> PlayerAction:

        keyType = None
        if self.keyboard_type == DefaultPlayerAgentKeyboardType.ARROWS:
            keyType = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_z, pygame.K_x]
        elif self.keyboard_type == DefaultPlayerAgentKeyboardType.WASD:
            keyType = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_j, pygame.K_k]

        keys = pygame.key.get_pressed()

        if keys[keyType[4]]:
            return PlaceBombAction(*player.get_postion())
        if keys[keyType[5]]:
            return PunchAction(player.direction)
        if keys[keyType[0]]:
            return MoveAction(Direction.LEFT)
        if keys[keyType[1]]:
            return MoveAction(Direction.RIGHT)
        if keys[keyType[2]]:
            return MoveAction(Direction.UP)
        if keys[keyType[3]]:
            return MoveAction(Direction.DOWN)    
        return StopAction()
        
    