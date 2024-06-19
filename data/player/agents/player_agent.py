from abc import abstractmethod
from data.game_state_information import GameStateInformation
from data.player.player_action import PlayerAction


class PlayerAgent:
    @abstractmethod
    def act(self, player, gameStateInformation: GameStateInformation) -> PlayerAction:
        pass