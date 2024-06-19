
import pygame

from assets.assets import Tile0
from data.game_state_information import GameStateInformation

class Bomb(pygame.sprite.Sprite):
    def __init__(self, game, player, position, group):
        super().__init__(group)
        self.game = game
        self.player = player
        self.image = Tile0.get_tile(6, 10)
        self.rect = self.image.get_rect(topleft = position)
        self.current_frame = 0
        self.frames_ids = [0, 1, 2, 1]
        self.number_of_frames = len(self.frames_ids)
        self.timer = 0
        

    def explode(self):
        self.game.bomb_was_killed(*self.rect.topleft, self.player)
        self.kill()

    def was_hit_by_explosion(self):
        self.explode()

    

    def update(self, gameStateInformation: GameStateInformation):
        if gameStateInformation.trigger_next_frame:
            self.current_frame = (self.current_frame + 1) % self.number_of_frames
            self.timer += 1
            if self.timer == 16:
                self.explode()
            self.image = Tile0.get_tile(6 + self.frames_ids[self.current_frame], 10)
