import pygame
from settings import *

from enemy.base import Enemy
from boss.base import Boss

class MaskedOrc(Boss):
    def __init__(self, group, start_pos=(650, 1000)):
        rect_width = 36
        height = 50

        super().__init__(
            width=150,
            height=height,
            health=10,
            rect_width=rect_width,
            group=group,
            start_pos=start_pos,
            animation_incrementer=16,
            attack_range=56,
            attack_damage=55,
        )

        self.pos = pygame.math.Vector2(
            (start_pos[0] - (rect_width / 2)) * scale_multiplier,
            (start_pos[1] - (height / 2)) * scale_multiplier,
        )

        self.idle_sprite_sheet = pygame.image.load(
            "assets/enemy/masked_orc/idle.png"
        ).convert_alpha()
        self.running_sprite_sheet = pygame.image.load(
            "assets/enemy/masked_orc/walk.png"
        ).convert_alpha()
        self.attack1_sprite_sheet = pygame.image.load(
            "assets/enemy/masked_orc/attack.png"
        ).convert_alpha()
        self.hurt_sprite_sheet = pygame.image.load(
            "assets/enemy/masked_orc/hurt.png"
        ).convert_alpha()
        self.death_sprite_sheet = pygame.image.load(
            "assets/enemy/masked_orc/death.png"
        ).convert_alpha()

        self.idle_frames = []
        self.running_frames = []
        self.attack1_frames = []
        self.hurt_frames = []
        self.death_frames = []

        self.extract_frames(150, 50, self.idle_sprite_sheet, self.idle_frames)
        self.extract_frames(150, 55, self.running_sprite_sheet, self.running_frames)
        self.extract_frames(150, 53, self.attack1_sprite_sheet, self.attack1_frames)
        self.extract_frames(150, 50, self.hurt_sprite_sheet, self.hurt_frames)
        self.extract_frames(150, 50, self.death_sprite_sheet, self.death_frames)

        self.image = self.idle_frames[self.current_frame]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = pygame.Rect(
            self.pos[0], self.pos[1], 36 * scale_multiplier, 50 * scale_multiplier
        )
        self.image_rect = self.image.get_rect(center=self.rect.center)

    def update_incrementer(self):
        if self.action == "idle":
            self.pos[1] -= (50 * scale_multiplier) - self.height
            self.height = 50 * scale_multiplier

            self.pos[0] -= ((36 * scale_multiplier) - self.rect_width) * 0.5
            self.rect_width = 36 * scale_multiplier

        elif self.action == "running":
            self.pos[1] -= (55 * scale_multiplier) - self.height
            self.height = 55 * scale_multiplier

            self.pos[0] -= ((36 * scale_multiplier) - self.rect_width) * 0.5
            self.rect_width = 36 * scale_multiplier

        elif self.action == "attacking":
            self.pos[1] -= (53 * scale_multiplier) - self.height
            self.height = 53 * scale_multiplier

            self.pos[0] -= ((110 * scale_multiplier) - self.rect_width) * 0.5
            self.rect_width = 110 * scale_multiplier

        elif self.action == "hurt":
            self.pos[1] -= (50 * scale_multiplier) - self.height
            self.height = 50 * scale_multiplier

            self.pos[0] -= ((36 * scale_multiplier) - self.rect_width) * 0.5
            self.rect_width = 36 * scale_multiplier

        elif self.action == "dead":
            self.pos[1] -= (50 * scale_multiplier) - self.height
            self.height = 50 * scale_multiplier
