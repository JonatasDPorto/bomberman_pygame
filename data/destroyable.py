import pygame

from assets.assets import Tile0
from data.game_state_information import GameStateInformation
from .power_up import PowerUp


class Destroyable(pygame.sprite.Sprite):
    
    def __init__(self, position, group, powerUp: PowerUp|None = None):
        super().__init__(group)
        self.powerUp = powerUp
        self.image = Tile0.get_tile(3, 1)
        self.rect = self.image.get_rect(topleft = position)
        self.is_destroying = False
        self.current_frame = 0
        self.frames_ids = [1, 2, 3, 4]
        self.number_of_frames = len(self.frames_ids)
        self.delete_on_next_frame = False



    def was_hit_by_explosion(self):
        self.is_destroying = True


    def update(self, gameStateInformation: GameStateInformation):
        if gameStateInformation.trigger_next_frame and self.is_destroying:
            if self.delete_on_next_frame:
                self.kill()
                return
            
            self.current_frame = (self.current_frame + 1) % self.number_of_frames
            if self.current_frame == self.number_of_frames - 1:
                self.delete_on_next_frame = True

            self.image = Tile0.get_tile(self.frames_ids[self.current_frame], 12)

            