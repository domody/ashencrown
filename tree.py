import sys

import pygame
import math
from pygame.locals import *
from settings import *


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load("assets/tree.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (256, 256))
        self.rect = self.image.get_rect(topleft=pos)
