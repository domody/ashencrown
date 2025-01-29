import pygame
from pygame.locals import *
import globals
from settings import *


class EntityGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_collisions(self, rect, entities):
        hit_list = []
        for entity in entities:
            if rect.colliderect(entity.rect):
                hit_list.append(entity.rect)
        return hit_list

    def update(self, dt, offset, player_rect):
        collision_group = globals.game_context.collision_group
        for sprite in self.sprites():
            movement = [sprite.velocity_x, sprite.velocity_y]

            collision_types = {
                "top": False,
                "bottom": False,
                "left": False,
                "right": False,
            }

            # sprite.rect.x += movement[0]
            # sprite.rect.y += movement[1]
            bottom_offset = 3 * scale_multiplier

            hit_list = self.get_collisions(sprite.rect, collision_group)
            for entity in hit_list:
                if (
                    movement[0] != 0
                    and movement[1] < -1
                    and sprite.rect.bottom - bottom_offset <= entity.bottom
                    and not entity.bottom - 20 > sprite.rect.bottom - bottom_offset
                ):
                    sprite.rect.bottom = entity.bottom + bottom_offset
                elif (
                    movement[0] != 0
                    and movement[1] > 1
                    and sprite.rect.bottom < entity.top + ((sprite.speed * dt) + 20)
                ):
                    sprite.rect.bottom = entity.top

            hit_list = self.get_collisions(sprite.rect, collision_group)
            for entity in hit_list:
                # if the sprites bottom - val is not lower than the entity bottom, then do left right collisions
                if not sprite.rect.bottom - bottom_offset + 15 > entity.bottom:
                    if movement[0] > 0:
                        sprite.rect.right = entity.left
                        collision_types["right"] = True

                    elif movement[0] < 0:
                        sprite.rect.left = entity.right
                        collision_types["right"] = False

            hit_list = self.get_collisions(sprite.rect, collision_group)
            for entity in hit_list:
                if movement[1] > 0 and not sprite.rect.bottom > entity.top + 20:
                    sprite.rect.bottom = entity.top
                    collision_types["bottom"] = True
                elif movement[1] < 0 and sprite.rect.bottom < (
                    entity.bottom + bottom_offset
                ):
                    sprite.rect.bottom = entity.bottom + bottom_offset
                    collision_types["top"] = False

            sprite.pos = [sprite.rect.x, sprite.rect.y]

            if hasattr(sprite, "line_to_player"):
                line_start, line_end = sprite.line_to_player
                sprite.los_blocked = False
                for entity in collision_group:
                    entity_rect = entity.rect
                    if entity_rect.clipline(line_start + offset, line_end + offset):
                        sprite.los_blocked = True
                        break
