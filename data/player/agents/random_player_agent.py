
from enum import Enum
import random
import pygame
from data.directions import Direction
from data.game_state_information import GameStateInformation
from data.player.agents.player_agent import PlayerAgent
from data.player.player import Player
from data.player.player_action import MoveAction, PlaceBombAction, PlayerAction, PunchAction, StopAction
from data.player_state_information import PlayerStateInformation


class RandomPlayerAgent(PlayerAgent):
    def __init__(self) -> None:
        super().__init__()


    def act(self, playerStateInformation: PlayerStateInformation, gameStateInformation: GameStateInformation) -> PlayerAction:

        actions = [
            PlaceBombAction(playerStateInformation.x, playerStateInformation.y),
            MoveAction(Direction.LEFT),
            MoveAction(Direction.RIGHT),
            MoveAction(Direction.UP),
            MoveAction(Direction.DOWN),
            StopAction()
        ]

        return random.choices(actions)[0]

    