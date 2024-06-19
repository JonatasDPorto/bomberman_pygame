
import time
from typing import Any
import pygame
from data.bomb import Bomb
from data.directions import Direction
from assets.assets import Chars
from data.game_state_information import GameStateInformation
from data.player.agents.player_agent import PlayerAgent
from data.player.player_action import MoveAction, PlaceBombAction, StopAction
from data.player.player_power_ups import PlayerPowerUps

class Player(pygame.sprite.Sprite):

    def __init__(self, game, position, agent, player_id, group):
        super().__init__(group)
        self.agent: PlayerAgent = agent
        self.power_ups = PlayerPowerUps()
        self.game = game
        self.image = Chars.get_tile(0, 0, 1)
        self.position = position
        self.rect = self.image.get_rect(topleft = self.position)
        self.next_action = StopAction()
        self.number_of_frames = 4
        self.current_frame = 0
        self.frames_ids = [0, 1, 2, 1]
        self.animation_id = 0
        self.player_id = player_id
        self.direction = Direction.DOWN
        self.current_bombs_in_ground = 0
        self.place_bomb_recent = False
        self.is_colliding_with_recent_bomb = False
    
    def get_postion(self):
        return self.rect.topleft

    def get_collide_rect(self):
        return pygame.Rect(self.rect.x + 3, self.rect.y + 17, 11, 8)
    
    def get_collide_rect_by_direction(self):
        if self.direction == Direction.DOWN or self.direction == Direction.UP:
            return pygame.Rect(self.rect.x + 5, self.rect.y + 17, 7, 8)
        return self.get_collide_rect()
    
    def bomb_was_killed(self):
        self.current_bombs_in_ground -= 1

    def was_hit_by_explosion(self):
        pass

    def __is_colliding_with_object__(self, collision_groups):
        new_rect = self.get_collide_rect_by_direction()
        for group in collision_groups:
            for sprite in group.sprites():
                if new_rect.colliderect(sprite.rect):
                    self.is_colliding_with_recent_bomb = isinstance(sprite, Bomb) and self.place_bomb_recent
                    return sprite.rect
        return None
               

    def __movement__(self, collision_groups):
        if isinstance(self.next_action, MoveAction):
            self.direction = self.next_action.direction
            x = self.direction.value[0]
            y = self.direction.value[1]
            self.rect.x += x * self.power_ups.movement_speed
            self.rect.y += y * self.power_ups.movement_speed
            obj_rect = self.__is_colliding_with_object__(collision_groups)
            can_walk = obj_rect is None
            if self.is_colliding_with_recent_bomb:
                can_walk = not can_walk
            if can_walk: # if is not colliding with something -> make animations
                if x != 0:
                    if x > 0:
                        self.animation_id = 6
                    else:
                        self.animation_id = 7
                else:
                    if y > 0:
                        self.animation_id = 5
                    else:
                        self.animation_id = 4
            else: # if is colliding with something -> ajust the x and y position to not transpass
                if obj_rect is None:
                    self.is_colliding_with_recent_bomb = False
                    self.place_bomb_recent = False
                    return 
                if x != 0:
                    if x > 0:
                        self.rect.right = obj_rect.left + 2
                    else:
                        self.rect.left = obj_rect.right - 2
                else:
                    if y > 0:
                        self.rect.bottom = obj_rect.top
                    else:
                        self.rect.top = obj_rect.bottom - 17

        elif isinstance(self.next_action, StopAction):
            if self.animation_id == 6:
                self.animation_id = 1
            elif self.animation_id == 7:
                self.animation_id = 0
            elif self.animation_id == 5:
                self.animation_id = 2
            elif self.animation_id == 4:
                self.animation_id = 3
            pass

    def __place_bomb__(self):
        if isinstance(self.next_action, PlaceBombAction):
            if self.current_bombs_in_ground < self.power_ups.bomb_count:
                bomb_was_placed = self.game.place_bomb(self)
                if bomb_was_placed:
                    self.current_bombs_in_ground += 1
                    self.place_bomb_recent = True
            

    def __animation__(self, gameStateInformation: GameStateInformation):
        if gameStateInformation.trigger_next_frame:
            self.current_frame = (self.current_frame + 1) % self.number_of_frames
            self.image = Chars.get_tile(self.player_id, self.animation_id, self.frames_ids[self.current_frame])

    def update(self, gameStateInformation: GameStateInformation, collision_groups):
        self.next_action = self.agent.act(self, gameStateInformation)
        self.__movement__(collision_groups)
        self.__animation__(gameStateInformation)
        self.__place_bomb__()
       
        
        
