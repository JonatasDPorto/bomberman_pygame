
from enum import Enum
import random
import pygame
from data.directions import Direction
from data.game_state_information import GameStateInformation
from data.neural_net_one_bit.one_bit_net import OneBitNet
from data.player.agents.player_agent import PlayerAgent
from data.player.player import Player
from data.player.player_action import MoveAction, PlaceBombAction, PlayerAction, PunchAction, StopAction
from data.player_state_information import PlayerStateInformation


class OneBitAgent(PlayerAgent):
    def __init__(self) -> None:
        super().__init__()
        self.network = OneBitNet()


    def act(self, playerStateInformation: PlayerStateInformation, gameStateInformation: GameStateInformation) -> PlayerAction:

        actions = [
            PlaceBombAction(playerStateInformation.x, playerStateInformation.y),
            MoveAction(Direction.LEFT),
            MoveAction(Direction.RIGHT),
            MoveAction(Direction.UP),
            MoveAction(Direction.DOWN),
            StopAction()
        ]

        index = self.network.forward(gameStateInformation.destroyable_matrix, gameStateInformation.players_matrix, gameStateInformation.walls_matrix, gameStateInformation.danger_zone_matrix)
        return actions[index]

    