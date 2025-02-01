import pygame
from settings import *
import random
import globals
from enemy.base import Enemy

class Boss(Enemy):
    def __init__(  
        self,
        width,
        height,
        health,
        rect_width,
        start_pos,
        group,
        animation_incrementer=36,
        attack_range=54,
        attack_damage=10,
      ):

        super().__init__(
            width=width,
            height=health,
            health=health,
            rect_width=rect_width,
            start_pos=start_pos,
            group=group,
            animation_incrementer=animation_incrementer,
            attack_range=attack_damage,
            attack_damage=attack_damage,
        )
    
    def boss_handler(self, dt):
        if (self.health / self.max_health) < 0.3:
            self.attack_type = 2

    def update(self, dt):
        if self.target_dead:
            self.state = "idle"
            self.action = "idle"

        self.boss_handler(dt)
        self.update_incrementer()
        self.update_frame(dt)
        self.move(dt)
