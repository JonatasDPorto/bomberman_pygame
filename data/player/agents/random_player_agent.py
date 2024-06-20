
from enum import Enum
import random
import pygame
from data.directions import Direction
from data.game_state_information import GameStateInformation
from data.player.agents.player_agent import PlayerAgent
from data.player.player import Player
from data.player.player_action import MoveAction, PlaceBombAction, PlayerAction, PunchAction, StopAction


class RandomPlayerAgent(PlayerAgent):
    def __init__(self) -> None:
        super().__init__()

        self.last_action = StopAction()


    def act(self, player: Player, gameStateInformation: GameStateInformation) -> PlayerAction:

        actions = [
            PlaceBombAction(*player.get_postion()),
            PunchAction(player.direction),
            MoveAction(Direction.LEFT),
            MoveAction(Direction.RIGHT),
            MoveAction(Direction.UP),
            MoveAction(Direction.DOWN),
            StopAction()
        ]
        a, b, c, d = 0, 0, 0, 0
        if isinstance(self.last_action, MoveAction):
            if self.last_action == Direction.LEFT:
                a = 40
            elif self.last_action == Direction.RIGHT:
                b = 40
            elif self.last_action == Direction.UP:
                c = 40
            elif self.last_action == Direction.DOWN:
                d = 40

        self.last_action = random.choices(actions, weights=[1/100, 0/100, (a + 12)/100, (b + 12)/100, (c + 12)/100, (d + 12)/100, 11/100])[0]

        return self.last_action

        
        
    