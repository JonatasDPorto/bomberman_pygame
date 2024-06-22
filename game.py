import random
from typing import List
import pygame
from config import GRID_SIZE, TILE_SIZE
from data.bomb import Bomb
from data.destroyable import Destroyable
from data.explosion import Explosion
from data.game_state_information import GameStateInformation
from data.groups.bombs_group import BombsGroup
from data.groups.explosion_group import ExplosionGroup
from data.groups.one_frame_group import OneFrameGroup
from data.groups.players_group import PlayersGroup
from data.player.agents.player_agent import PlayerAgent
from data.power_up import PowerType
from data.wall import Wall
from data.ground import Ground
from data.player.player import Player



class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls_group = OneFrameGroup()
        self.ground_group = OneFrameGroup()
        self.destroyable_group = pygame.sprite.Group()
        self.bomb_group = BombsGroup()
        self.explosion_group = ExplosionGroup()
        self.players_group = PlayersGroup()


    def update(self, trigger_next_frame):

        state = GameStateInformation(trigger_next_frame, self.destroyable_group, self.players_group, self.walls_group, self.bomb_group, self.explosion_group)
        
        self.walls_group.update()
        self.ground_group.update()
        self.destroyable_group.update(state)
        self.bomb_group.update(state)
        self.explosion_group.update(state)
        self.players_group.update(state, [self.walls_group, self.destroyable_group, self.bomb_group])

    def draw(self, surface):
        self.walls_group.draw(surface)
        self.ground_group.draw(surface)
        self.destroyable_group.draw(surface)
        self.bomb_group.draw(surface)
        self.explosion_group.draw(surface)
        self.players_group.draw(surface)
                
    def create_players(self, players: List[PlayerAgent]):
        positions = [
            (2, 1),
            (GRID_SIZE - 3, GRID_SIZE - 3),
            (GRID_SIZE - 3,1),
            (2, GRID_SIZE - 3),
        ]
        for pos, agent in enumerate(players):
            Player(self, tuple(i * TILE_SIZE for i in positions[pos]), agent, pos, self.players_group)


    def create_map(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                wall = Wall(x, y, self.walls_group)
                if not wall.position:
                    dx, dy = x * TILE_SIZE, y * TILE_SIZE
                    if random.random() > 0.3 and (3 < x < GRID_SIZE - 4 or 3 < y < GRID_SIZE - 4):
                        powerType = random.sample(population=PowerType.get_values() + [None]*10, k=1)
                        powerUp = None#PowerUp(self.objects_group, powerType=powerType[0])
                        destroyable = Destroyable((dx, dy), self.destroyable_group, powerUp=powerUp)
                    Ground((dx, dy), self.ground_group)
        self.walls_group.build()
        self.ground_group.build()
            
    
    def place_bomb(self, player: Player) -> bool:
        if player.percentage_in_next_grid() > 0.2:
            return False
        x, y = player.get_position_in_grid()

        Bomb(self, player, (x * TILE_SIZE, y * TILE_SIZE), self.bomb_group)
        return True
    
    def __create_explosion_in_direction__(self, player: Player, calc_pos_1, calc_pos_2, anim_1, anim_2):
        top_canceled = False
        for eid in range(1, player.power_ups.bomb_range):
            if top_canceled:
                break
            pos = calc_pos_1(eid)
            rect = pygame.Rect(*pos, TILE_SIZE, TILE_SIZE)
  
            if rect.collidelist([wall.rect for wall in self.walls_group.sprites()]) >= 0:
                top_canceled = True
                break
            if rect.collidelist([destroyable.rect for destroyable in self.destroyable_group.sprites()]) >= 0:
                top_canceled = True

            Explosion(player, pos, anim_1, self.explosion_group, [self.destroyable_group, self.players_group, self.bomb_group])
                
        if not top_canceled:
            pos = calc_pos_2()
            rect = pygame.Rect(*pos, TILE_SIZE, TILE_SIZE)
            if rect.collidelist([wall.rect for wall in self.walls_group.sprites()]) >= 0:
                return
            Explosion(player, pos, anim_2, self.explosion_group, [self.destroyable_group, self.players_group, self.bomb_group])


    def bomb_was_killed(self, x, y, player: Player):
        Explosion(player, (x, y), 6, self.explosion_group, [self.destroyable_group, self.players_group, self.bomb_group], True)
        self.__create_explosion_in_direction__(player, lambda eid: (x, y - (TILE_SIZE * eid)), lambda: (x, y - (TILE_SIZE * player.power_ups.bomb_range)), 5, 2)
        self.__create_explosion_in_direction__(player, lambda eid: (x, y + (TILE_SIZE * eid)), lambda: (x, y + (TILE_SIZE * player.power_ups.bomb_range)), 5, 3)
        self.__create_explosion_in_direction__(player, lambda eid: (x - (TILE_SIZE * eid), y), lambda: (x - (TILE_SIZE * player.power_ups.bomb_range), y), 4, 0)
        self.__create_explosion_in_direction__(player, lambda eid: (x + (TILE_SIZE * eid), y), lambda: (x + (TILE_SIZE * player.power_ups.bomb_range), y), 4, 1)
