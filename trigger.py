import pygame
from settings import *


class Trigger(pygame.sprite.Sprite):
    def __init__(
        self, pos, width, height, trigger_range, action, deactivate_action=None
    ):
        self.pos = pos
        self.width = width
        self.height = height

        self.trigger_range = trigger_range
        self.action = action
        self.deactivate_action = deactivate_action
        self.triggered = False

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def check_trigger(self, player_pos):
        if self.rect.collidepoint(player_pos) or self.is_within_range(player_pos):
            # if not self.triggered:
            self.action()
            # self.triggered = True
        else:
            # if self.triggered and self.deactivate_action:
            self.deactivate_action()
            # self.triggered = False

    def is_within_range(self, player_pos):
        dx = player_pos[0] - (self.rect.x + self.rect.width // 2)
        dy = player_pos[1] - (self.rect.y + self.rect.height // 2)
        distance = (dx**2 + dy**2) ** 0.5
        return distance <= self.trigger_range
