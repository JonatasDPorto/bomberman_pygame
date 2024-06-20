import time
import pygame
import sys

from assets.assets import init_assets
from data.player.agents.default_player_agent import DefaultPlayerAgent, DefaultPlayerAgentKeyboardType
from config import *
from data.player.agents.random_player_agent import RandomPlayerAgent
from game import Game

pygame.init()

original_screen = pygame.Surface(GAME_WINDOW_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

init_assets()

game = Game(*WINDOW_SIZE)
game.create_map()


game.create_players([
    # DefaultPlayerAgent(DefaultPlayerAgentKeyboardType.ARROWS),
    # DefaultPlayerAgent(DefaultPlayerAgentKeyboardType.WASD),
    RandomPlayerAgent(),
    RandomPlayerAgent(),
    RandomPlayerAgent(),
    RandomPlayerAgent()
])
running = True

last_frame_time = pygame.time.get_ticks()
animations_time = 100

first_frame = True

while running:
    original_screen.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_frame_time = pygame.time.get_ticks()
    elapsed_time = current_frame_time - last_frame_time

    if elapsed_time >= animations_time:
        last_frame_time = current_frame_time
        game.update(True)
    else:
        game.update(False)
    
    game.draw(original_screen)

    scaled_screen = pygame.transform.scale(original_screen, WINDOW_SIZE)
    screen.blit(scaled_screen, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)
    if first_frame:
        first_frame = False
        time.sleep(5)
        

pygame.quit()
sys.exit()