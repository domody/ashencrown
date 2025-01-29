import pygame
from settings import *

from enemy.base import Enemy


class Goblin(Enemy):
    def __init__(self, group, start_pos=(650, 1000)):
        rect_width = 30
        height = 45

        super().__init__(
            width=116,
            height=height,
            health=20,
            rect_width=rect_width,
            group=group,
            start_pos=start_pos,
            animation_incrementer=24,
            attack_range=44,
            attack_damage=15,
        )

        self.pos = pygame.math.Vector2(
            (start_pos[0] - (rect_width / 2)) * scale_multiplier,
            (start_pos[1] - (height / 2)) * scale_multiplier,
        )

        self.idle_sprite_sheet = pygame.image.load(
            "assets/enemy/goblin/idle.png"
        ).convert_alpha()
        self.running_sprite_sheet = pygame.image.load(
            "assets/enemy/goblin/run.png"
        ).convert_alpha()
        self.attack1_sprite_sheet = pygame.image.load(
            "assets/enemy/goblin/attack1.png"
        ).convert_alpha()
        self.hurt_sprite_sheet = pygame.image.load(
            "assets/enemy/goblin/hurt.png"
        ).convert_alpha()
        self.death_sprite_sheet = pygame.image.load(
            "assets/enemy/goblin/death.png"
        ).convert_alpha()

        self.idle_frames = []
        self.running_frames = []
        self.attack1_frames = []
        self.hurt_frames = []
        self.death_frames = []

        self.extract_frames(116, 45, self.idle_sprite_sheet, self.idle_frames)
        self.extract_frames(116, 44, self.running_sprite_sheet, self.running_frames)
        self.extract_frames(116, 53, self.attack1_sprite_sheet, self.attack1_frames)
        self.extract_frames(116, 63, self.hurt_sprite_sheet, self.hurt_frames)
        self.extract_frames(116, 41, self.death_sprite_sheet, self.death_frames)

        self.image = self.idle_frames[self.current_frame]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = pygame.Rect(
            self.pos[0], self.pos[1], 30 * scale_multiplier, 45 * scale_multiplier
        )
        self.image_rect = self.image.get_rect(center=self.rect.center)

    def update_incrementer(self):
        if self.action == "idle":
            self.pos[1] -= (45 * scale_multiplier) - self.height
            self.height = 45 * scale_multiplier

            self.animation_incrementer = 24

            # if self.facing == "left":
            self.pos[0] -= ((30 * scale_multiplier) - self.rect_width) * 0.5

            self.rect_width = 30 * scale_multiplier

        elif self.action == "running":
            self.pos[1] -= (44 * scale_multiplier) - self.height
            self.height = 44 * scale_multiplier

            # if self.facing == "left":
            self.pos[0] -= ((30 * scale_multiplier) - self.rect_width) * 0.5

            self.rect_width = 30 * scale_multiplier

            self.animation_incrementer = 24

        elif self.action == "attacking":
            self.pos[1] -= (53 * scale_multiplier) - self.height
            self.height = 53 * scale_multiplier

            # if self.facing == "left":
            self.pos[0] -= ((59 * scale_multiplier) - self.rect_width) * 0.5

            self.rect_width = 59 * scale_multiplier

        elif self.action == "hurt":
            self.pos[1] -= (63 * scale_multiplier) - self.height
            self.height = 63 * scale_multiplier

            # if self.facing == "left":
            self.pos[0] -= ((30 * scale_multiplier) - self.rect_width) * 0.5

            self.rect_width = 30 * scale_multiplier

        elif self.action == "dead":
            self.pos[1] -= (41 * scale_multiplier) - self.height
            self.height = 41 * scale_multiplier
