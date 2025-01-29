import sys

import pygame
import math
from pygame.locals import *

from settings import *


class CollisionGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update(self, player_rect):
        for sprite in self.sprites():
            sprite.update_player_pos(player_rect)
