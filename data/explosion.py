
import pygame

from assets.assets import Tile0
from data.bomb import Bomb
from data.destroyable import Destroyable
from data.game_state_information import GameStateInformation
from data.player.player import Player

class Explosion(pygame.sprite.Sprite):
    def __init__(self, player, position, animation_id, group, collision_groups, is_core_explosion=False):
        super().__init__(group)
        self.player = player
        self.animation_id = animation_id
        self.collision_groups = collision_groups
        self.image = Tile0.get_tile(0, 5 + animation_id)
        self.rect = self.image.get_rect(topleft = position)
        self.current_frame = 0
        self.frames_ids = [1, 2, 3, 4]
        self.number_of_frames = len(self.frames_ids)
        self.delete_on_next_frame = False
        self.is_core_explosion = is_core_explosion
        

    def update(self, gameStateInformation: GameStateInformation):
        if gameStateInformation.trigger_next_frame:
            if self.delete_on_next_frame:
                self.kill()
                if self.is_core_explosion:
                    self.player.bomb_was_killed()
                return
            self.current_frame = (self.current_frame + 1) % self.number_of_frames

            if self.current_frame == self.number_of_frames - 1:
                self.delete_on_next_frame = True

            col_sprites = []
            for group in self.collision_groups:
                col_sprites += group.sprites() 
            col_rects = [obj.rect for obj in col_sprites]

            ids = self.rect.collidelistall(col_rects)
            for rect_id in ids:
                sprite = col_sprites[rect_id]
                if isinstance(sprite, Player):
                    if self.delete_on_next_frame:
                        sprite.was_hit_by_explosion()

                elif isinstance(sprite, Destroyable) or isinstance(sprite, Bomb):
                    sprite.was_hit_by_explosion()


            self.image = Tile0.get_tile(self.frames_ids[self.current_frame], 5 + self.animation_id)
