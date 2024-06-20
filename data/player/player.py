
import time
from typing import Any
import pygame
from config import TILE_SIZE
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
        self.image = Chars.get_tile(player_id, 0, 1)
        self.position = position
        self.rect = self.image.get_rect(topleft = self.position)
        self.rect.y -= 9
        self.next_action = StopAction()
        self.number_of_frames = 4
        self.current_frame = 0
        self.frames_ids = [0, 1, 2, 1]
        self.animation_id = 0
        self.player_id = player_id
        self.direction = Direction.DOWN
        self.current_bombs_in_ground = 0
        self.is_moving = False
        self.next_position = None
    
    def get_postion(self):
        return self.rect.topleft

    def get_player_collider_rect(self):
        return pygame.Rect(self.rect.x, self.rect.y + 9, 16, 16)
    
    def __get_down_collider_rect__(self):
        return pygame.Rect(self.rect.x + 4, self.rect.y + 9 + 16 + 4, 8, 8)
    
    def __get_up_collider_rect__(self):
        return pygame.Rect(self.rect.x + 4, self.rect.y + 9 - 4 - 8, 8, 8)
    
    def __get_left_collider_rect__(self):
        return pygame.Rect(self.rect.x - 4 - 8, self.rect.y + 9 + 4, 8, 8)
    
    def __get_right_collider_rect__(self):
        return pygame.Rect(self.rect.x + 16 + 4, self.rect.y + 9 + 4, 8, 8)
    
    def bomb_was_killed(self):
        self.current_bombs_in_ground -= 1

    def was_hit_by_explosion(self):
        pass

    def __is_colliding_with_object__(self, rect, collision_groups):
        for group in collision_groups:
            for sprite in group.sprites():
                if rect.colliderect(sprite.rect):
                    return True
        return False
               

    def __can_move_in_direction__(self, collision_groups):
        if self.direction == Direction.DOWN:
            return not self.__is_colliding_with_object__(self.__get_down_collider_rect__(), collision_groups)
        if self.direction == Direction.UP:
            return not self.__is_colliding_with_object__(self.__get_up_collider_rect__(), collision_groups)
        if self.direction == Direction.LEFT:
            return not self.__is_colliding_with_object__(self.__get_left_collider_rect__(), collision_groups)
        if self.direction == Direction.RIGHT:
            return not self.__is_colliding_with_object__(self.__get_right_collider_rect__(), collision_groups)
        
    
    def __try_to_start_movement__(self, collision_groups):
        if self.is_moving:
            return
        self.direction = self.next_action.direction
        self.is_moving = self.__can_move_in_direction__(collision_groups)
        if self.is_moving:
            x = self.direction.value[0]
            y = self.direction.value[1]
            rect = self.get_player_collider_rect()
            self.next_position = (rect.x + (x * TILE_SIZE), rect.y + (y * TILE_SIZE))

    def __movement__(self):
        if not self.is_moving:
            return
        
        dx = self.direction.value[0]
        dy = self.direction.value[1]
        
        rect = self.get_player_collider_rect()

        x = rect.x
        y = rect.y

        nx = self.next_position[0]
        ny = self.next_position[1]

        

        if (abs(nx - x) > self.power_ups.movement_speed) or (abs(ny - y) > self.power_ups.movement_speed):
            self.rect.x += dx * self.power_ups.movement_speed
            self.rect.y += dy * self.power_ups.movement_speed
        else:
            self.rect.x = nx
            self.rect.y = ny - 9
            self.is_moving = False


    def __move_animation__(self):
        if self.is_moving:
            dx = self.direction.value[0]
            dy = self.direction.value[1]
            if dx != 0:
                if dx > 0:
                    self.animation_id = 6
                else:
                    self.animation_id = 7
            else:
                if dy > 0:
                    self.animation_id = 5
                else:
                    self.animation_id = 4


    def __place_bomb__(self):
        if isinstance(self.next_action, PlaceBombAction):
            if self.current_bombs_in_ground < self.power_ups.bomb_count:
                bomb_was_placed = self.game.place_bomb(self)
                if bomb_was_placed:
                    self.current_bombs_in_ground += 1
            

    def __animation__(self, gameStateInformation: GameStateInformation):
        if gameStateInformation.trigger_next_frame:
            self.current_frame = (self.current_frame + 1) % self.number_of_frames
            self.image = Chars.get_tile(self.player_id, self.animation_id, self.frames_ids[self.current_frame])

    def __stop_animation__(self):
        if self.is_moving:
            return
        if self.animation_id == 6:
            self.animation_id = 1
        elif self.animation_id == 7:
            self.animation_id = 0
        elif self.animation_id == 5:
            self.animation_id = 2
        elif self.animation_id == 4:
            self.animation_id = 3

    def update(self, gameStateInformation: GameStateInformation, collision_groups):

        self.next_action = self.agent.act(self, gameStateInformation)

        if isinstance(self.next_action, MoveAction):
            self.__try_to_start_movement__(collision_groups)
        elif isinstance(self.next_action, StopAction):
            self.__stop_animation__()

        elif isinstance(self.next_action, PlaceBombAction):
            self.__place_bomb__()

        self.__movement__()
        self.__move_animation__()
        self.__stop_animation__()
        self.__animation__(gameStateInformation)
       
        
        
