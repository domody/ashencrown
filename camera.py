import sys

import pygame
import math
from pygame.locals import *
from player import Player
from enemy.goblin import Goblin
from enemy.masked_orc import MaskedOrc

from settings import *

# https://www.youtube.com/watch?v=u7LPRqrzry8


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.first_instance = True

        self.camera_borders = {"left": 0, "right": 0, "top": 0, "bottom": 0}
        l = self.camera_borders["left"]
        t = self.camera_borders["top"]
        w = self.display_surface.get_size()[0] - (
            self.camera_borders["left"] + self.camera_borders["right"]
        )
        h = self.display_surface.get_size()[1] - (
            self.camera_borders["top"] + self.camera_borders["bottom"]
        )
        self.camera_rect = pygame.Rect(l, t, w, h)

        self.map_width = None
        self.map_height = None

        self.camera_speed = 2.5

        self.limit_edges = False

    def set_map_dimensions(self, map_width, map_height):
        self.map_height = map_height
        self.map_width = map_width

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

        # Camera Limits
        if self.limit_edges:
            if self.offset.x < 1:
                self.offset.x = 0
            elif self.offset.x + screen_width > self.map_width * scale_multiplier:
                self.offset.x = self.map_width * scale_multiplier - screen_width

            if self.offset.y < 1:
                self.offset.y = 0
            elif self.offset.y + screen_width > self.map_height * scale_multiplier:
                self.offset.y = self.map_height * scale_multiplier - screen_width

        # self.offset.x = 0
        # self.offset.y = 0

    def delay_target_camera(self, target, dt):
        # Calculate target offset
        target_offset_x = target.rect.centerx - self.half_w
        target_offset_y = target.rect.centery - self.half_h

        # Interpolate between current offset and target offset
        self.offset.x += (target_offset_x - self.offset.x) * self.camera_speed * dt

        self.offset.y += (target_offset_y - self.offset.y) * self.camera_speed * dt

        # Camera Limits
        if self.limit_edges:
            if self.offset.x < 1:
                self.offset.x = 0
            elif self.offset.x + screen_width > self.map_width * scale_multiplier:
                self.offset.x = self.map_width * scale_multiplier - screen_width

            if self.offset.y < 1:
                self.offset.y = 0
            elif self.offset.y + screen_width > self.map_height * scale_multiplier:
                self.offset.y = self.map_height * scale_multiplier - screen_width

    def set_limit_edges(self, limit_edges):
        # print(limit_edges)
        self.limit_edges = limit_edges

    def custom_draw(self, player, dt, context):
        ground_tile_group = context.ground_tile_group
        light_group = context.light_group

        if self.first_instance == True:
            self.center_target_camera(player)
            self.first_instance = False
        else:
            self.delay_target_camera(player, dt)

        # print(self.offset)
        # Draw ground tiles
        for sprite in ground_tile_group:
            offset_pos = sprite.rect.topleft - self.offset
            # print(sprite)
            if (
                hasattr(sprite, "shadow_image") == True
                and sprite.shadow_image is not None
            ):
                if sprite.shadow_rect:  # Ensure the shadow_rect is defined
                    shadow_offset_pos = sprite.shadow_rect.topleft - self.offset
                    self.display_surface.blit(
                        sprite.shadow_image,
                        sprite.rect.bottomleft
                        - pygame.math.Vector2(0, sprite.shadow_rect.height)
                        - self.offset,
                    )

            if sprite.visible == True:
                self.display_surface.blit(sprite.image, offset_pos)

            # # Draw a small circle above each tile to represent its state
            # tile_center = sprite.rect.center - self.offset  # Get tile center position
            # pygame.draw.circle(self.display_surface, (255, 165, 0), tile_center - pygame.math.Vector2(0, 10), 5)  # Small orange circle 10 pixels above the tile

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            if (
                isinstance(sprite, Player)
                or isinstance(sprite, Goblin)
                or isinstance(sprite, MaskedOrc)
            ):
                offset_pos = sprite.image_rect.topleft - self.offset
            else:
                offset_pos = sprite.rect.topleft - self.offset

            if (
                hasattr(sprite, "shadow_image") == True
                and sprite.shadow_image is not None
            ):
                if sprite.shadow_rect:  # Ensure the shadow_rect is defined
                    shadow_offset_pos = sprite.shadow_rect.topleft - self.offset
                    self.display_surface.blit(
                        sprite.shadow_image,
                        sprite.rect.bottomleft
                        - pygame.math.Vector2(0, sprite.shadow_rect.height)
                        - self.offset,
                    )

            if hasattr(sprite, "image") == True:
                self.display_surface.blit(sprite.image, offset_pos)

        for light in light_group:
            # pass
            light.draw(self.display_surface, self.offset)
            # offset_pos = (0, 0) - self.offset
            # print(light.pos, player.pos)
            # self.display_surface.blit(light.surface,  offset_pos)

        # pygame.draw.rect(self.display_surface, 'yellow', self.camera_rect, 5)
        # line_to_player = ((self.half_w - self.offset.x, self.half_h - self.offset.y), (player.rect.centerx - self.offset.x, player.rect.centery - self.offset.y))
        # pygame.draw.line(self.display_surface, 'yellow', *line_to_player,  width=4)

    def update(self, dt, *args):
        # super().update(dt, *args)
        pass
