import sys

import pygame
import math
from pygame.locals import *

from settings import *

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
transparent = (0, 0, 0, 0)


class Wall(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.width = 1024
        self.height = 1024
        self.pos = pygame.math.Vector2(0, 0)

        self.image = pygame.Surface((self.width, self.height))
        self.color = red
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=self.pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update_player_pos(self, player_rect):
        player_rect_center = player_rect.center
        # print(pygame.Rect.colliderect(player_rect, self.rect))

        if self.rect.colliderect(player_rect):
            # self.resolve_collision(player_rect)
            self.color = green
        else:
            self.color = red

    def update_frame(self):
        self.image.fill(self.color)

    def update(self, dt):
        self.update_frame()
