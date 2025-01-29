import sys

import pygame
import math
from pygame.locals import *

from settings import *


class EnemyGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update(self, dt, target, offset):
        for sprite in self.sprites():
            sprite.update_target_pos(dt, target.rect, offset)

            if (
                sprite.target_seen
                and sprite.los_blocked
                and sprite.target_last_location == None
            ):
                sprite.target_last_location = target.rect.center

            if (
                pygame.Rect.colliderect(sprite.rect, target.rect)
                and target.action == "attacking"
                and target.current_frame == 3
            ):
                sprite.hurt = True
                break
            else:
                sprite.hurt = False

            if (
                pygame.Rect.colliderect(sprite.rect, target.rect)
                and sprite.action == "attacking"
            ):
                if not sprite.dealt_damage and sprite.current_frame == 2:
                    target.take_damage(sprite.attack_damage)
                    sprite.dealt_damage = True

            if target.action == "dead":
                sprite.target_dead = True

            if sprite.dead and sprite.end_of_death:
                sprite.kill()

        super().update(dt)


#             if self.hurt:
#                 self.state = "hurt"
#                 self.hurt_started = True

#                 if not self.damaged:
#                     self.health -= 10
#                     self.damaged = True


# def update_self(self, target, offset, dt):
#         self.velocity_x = 0
#         self.velocity_y = 0

#         target_pos = pygame.math.Vector2(target.center) - offset
#         goblin_pos = pygame.math.Vector2(self.rect.center) - offset

#         if self.state == "aggressive":
#             self.action = "running"
#             self.timeout -= dt

#             if self.timeout <= 0 and self.can_move:
#                 direction = target_pos - goblin_pos

#                 distance = direction.length()

#                 if distance != 0:  # Avoid division by zero
#                     direction = direction.normalize()

#                     # Update the goblin's velocity
#                     self.velocity_x = direction.x * self.speed * dt
#                     self.velocity_y = direction.y * self.speed * dt

#             if self.target_last_location:
#                 self.target_last_location = None

#         elif self.state == "searching" and self.target_last_location:
#                 target_pos = pygame.math.Vector2(self.target_last_location) - offset

#                 direction = target_pos - goblin_pos

#                 distance = direction.length()

#                 if distance != 0:  # Avoid division by zero
#                     direction = direction.normalize()

#                     # Update the goblin's velocity
#                     self.velocity_x = direction.x * self.speed * dt
#                     self.velocity_y = direction.y * self.speed * dt

#         elif self.state == "attacking":
#             self.attack_timeout -= dt

#             if self.attack_timeout <= 0:
#                 self.action = "attacking"

#                 if self.attack_started == False:
#                     self.frame_counter = 0
#                     self.attack_started = True


#             if self.attack_finished:
#                 self.attack_timeout = 0.2
#                 self.attack_finished = False
#                 self.attack_started = False
#                 self.action = "idle"

#         elif self.state == "hurt":
#             self.action = "hurt"

#         if self.hurt_started and not self.hurt:
#             if self.hurt_finished:
#                 self.hurt_finished = False
#                 self.hurt_started = False
#             else:
#                 self.hurt_finished = True

#             self.damaged = False


#         if self.health <= 0:
#             if self.hurt_finished:
#                 self.state = "dead"
#                 self.action = "dead"
#                 if not self.dead:
#                     self.frame_counter = 0
#                     self.current_frame = 0
#                     self.dead = True

#             self.can_move = False
#             self.can_attack = False
