import numpy as np
from config import GRID_SIZE

class OneBitNet:

    def __init__(self) -> None:
        self.randomize_weights()

    def randomize_weights(self):
        self.destroyable_weights_1 = np.random.randint(0, 2, (GRID_SIZE, 1))
        self.players_weights_1 = np.random.randint(0, 2, (GRID_SIZE, 1))
        self.walls_weights_1 = np.random.randint(0, 2, (GRID_SIZE, 1))
        self.danger_zone_weights_1 = np.random.randint(0, 2, (GRID_SIZE, 1))

        self.destroyable_weights_2 = np.random.randint(0, 2, (6, GRID_SIZE))
        self.players_weights_2 = np.random.randint(0, 2, (6, GRID_SIZE))
        self.walls_weights_2 = np.random.randint(0, 2, (6, GRID_SIZE))
        self.danger_zone_weights_2 = np.random.randint(0, 2, (6, GRID_SIZE))

    def forward(self, destroyable_matrix, players_matrix, walls_matrix, danger_zone_matrix):
        destroyable_first_layer = np.dot(destroyable_matrix, self.destroyable_weights_1)
        players_first_layer = np.dot(players_matrix, self.players_weights_1)
        walls_first_layer = np.dot(walls_matrix, self.walls_weights_1)
        danger_zone_first_layer = np.dot(danger_zone_matrix, self.danger_zone_weights_1)

        destroyable_second_layer = np.dot(self.destroyable_weights_2, destroyable_first_layer).flatten()
        players_second_layer = np.dot(self.players_weights_2, players_first_layer).flatten()
        walls_second_layer = np.dot(self.walls_weights_2, walls_first_layer).flatten()
        danger_zone_second_layer = np.dot(self.danger_zone_weights_2, danger_zone_first_layer).flatten()

        result = (destroyable_second_layer * players_second_layer * walls_second_layer * danger_zone_second_layer)
        return np.argmax(result)
