import sys

import pygame
import math
import random
from pygame.locals import *
from settings import *
import globals

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.width = 96
        self.rect_width = 20 * scale_multiplier
        self.height = 37

        self.pos = pygame.math.Vector2(player_start_x, player_start_y)
        self.speed = player_speed
        self.facing = "right"
        self.action = "idle"

        self.max_health = 100
        self.max_armour = 75
        self.max_stamina = 60

        self.health = self.max_health
        self.armour = self.max_armour
        self.stamina = self.max_stamina

        self.keys = ["tut_main"]

        self.recharging = False

        self.can_move = True

        self.can_attack = True
        self.attack_started = False
        self.attack_cooldown = 0

        self.roll_started = False

        self.hit = False
        self.defend_cooldown = 0

        self.hurt_started = False
        self.hurt_finished = False

        self.hurt_counter = 0
        self.heal_rate = 15
        self.heal_timeout = 1

        self.end_of_death = False

        self.camera_offset = (0, 0)

        # Frame & Animation variables
        self.frame_counter = 0
        self.current_frame = 0
        self.animation_incrementer = 36

        self.idle_sprite_sheet = pygame.image.load(
            "assets/player/knight/Sprites/with_outline_adjusted/idle.png"
        ).convert_alpha()
        self.walking_sprite_sheet = pygame.image.load(
            "assets/player/knight/Sprites/with_outline_adjusted/walk.png"
        ).convert_alpha()
        self.running_sprite_sheet = pygame.image.load(
            "assets/player/knight/Sprites/with_outline_adjusted/run.png"
        ).convert_alpha()
        self.rolling_sprite_sheet = pygame.image.load(
            "assets/player/knight/Sprites/with_outline_adjusted/roll.png"
        ).convert_alpha()
        self.attack1_sprite_sheet = pygame.image.load(
            "assets/player/knight/sprites/with_outline_adjusted/attack1.png"
        ).convert_alpha()
        self.defend_sprite_sheet = pygame.image.load(
            "assets/player/knight/sprites/with_outline_adjusted/defend.png"
        ).convert_alpha()
        self.hurt_sprite_sheet = pygame.image.load(
            "assets/player/knight/sprites/with_outline_adjusted/hurt.png"
        ).convert_alpha()
        self.death_sprite_sheet = pygame.image.load(
            "assets/player/knight/sprites/with_outline_adjusted/death.png"
        ).convert_alpha()

        self.idle_frames = []
        self.walking_frames = []
        self.running_frames = []
        self.attack1_frames = []
        self.roll_frames = []
        self.defend_frames = []
        self.hurt_frames = []
        self.death_frames = []

        self.extract_frames(96, 37, self.idle_sprite_sheet, self.idle_frames)
        self.extract_frames(96, 37, self.walking_sprite_sheet, self.walking_frames)
        self.extract_frames(96, 38, self.running_sprite_sheet, self.running_frames)
        self.extract_frames(96, 36, self.attack1_sprite_sheet, self.attack1_frames)
        self.extract_frames(96, 32, self.rolling_sprite_sheet, self.roll_frames)
        self.extract_frames(96, 36, self.defend_sprite_sheet, self.defend_frames)
        self.extract_frames(96, 36, self.hurt_sprite_sheet, self.hurt_frames)
        self.extract_frames(96, 34, self.death_sprite_sheet, self.death_frames)

        self.image = self.idle_frames[self.current_frame]
        self.image = pygame.transform.scale(
            self.image, (self.width * scale_multiplier, self.height * scale_multiplier)
        )

        # self.collision_rect = self.image.get_rect(topleft = self.pos)
        # self.collision_rect = pygame.Rect(self.pos[0] + (((self.width // 2) - 16) * scale_multiplier) , self.pos[1] + (((self.height // 2) - 16)  * scale_multiplier), 32 * scale_multiplier, 32 * scale_multiplier)

        self.rect = pygame.Rect(
            self.pos[0], self.pos[1], self.rect_width, self.height * scale_multiplier
        )
        self.image_rect = self.image.get_rect(center=self.rect.center)

        self.movement_sfx_timeout = 0.2
        self.attacking_sfx_playing = False
        self.defending_sfx_playing = False
        
        self.shadow_width = 25
        self.shadow_height = 24
        self.shadow_image = pygame.image.load('assets/player/playershadow.png').convert_alpha()
        self.shadow_image = pygame.transform.scale(self.shadow_image, (self.shadow_width * scale_multiplier, self.shadow_height * scale_multiplier))
        self.shadow_image.set_alpha(64)
        self.shadow_rect = self.shadow_image.get_rect(bottomleft = self.rect.bottomleft)

    def add_to_camera_group(self, group):
        super().__init__(group)

    def extract_frames(
        self, frame_width, frame_height, current_sprite_sheet, frames_array
    ):
        frame_width = frame_width
        frame_height = frame_height

        for y in range(0, current_sprite_sheet.get_height(), frame_height):
            for x in range(0, current_sprite_sheet.get_width(), frame_width):
                frame = current_sprite_sheet.subsurface(
                    pygame.Rect(x, y, frame_width, frame_height)
                )

                frame = pygame.transform.scale(frame, (self.width, self.height))
                frames_array.append(frame)

    def update_offset(self, offset):
        self.camera_offset = offset

    def draw(self, screen, offset):
        # Adjust rect position by camera offset
        adjusted_rect = self.rect.move(-offset.x, -offset.y)
        adj_col_rect = self.image_rect.move(-offset.x, -offset.y)
        # Fill the rect with a blue color for debugging
        # pygame.draw.rect(screen, blue, adj_col_rect)

        pygame.draw.rect(screen, green, adjusted_rect, 2, 1)

    def user_input(self, dt):
        # Reset velocity every frame
        self.velocity_x = 0
        self.velocity_y = 0

        # Get keys & mouse buttons pressed
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        # Movement
        if self.can_move:
            if keys[pygame.K_d]:
                self.velocity_x = self.speed * dt
                self.action = "walking"
                self.facing = "right"
            if keys[pygame.K_a]:
                self.velocity_x = -self.speed * dt
                self.action = "walking"
                self.facing = "left"
            if keys[pygame.K_s]:
                self.velocity_y = self.speed * dt
                self.action = "walking"
            if keys[pygame.K_w]:
                self.velocity_y = -self.speed * dt
                self.action = "walking"

            # Diagonal movement speed resolution
            if self.velocity_x != 0 and self.velocity_y != 0:
                self.velocity_x /= math.sqrt(2)
                self.velocity_y /= math.sqrt(2)

            # Recharge stamina if not sprinting or rolling or attacking
            if self.stamina < 60 and not (
                self.action == "sprinting"
                or self.action == "rolling"
                or self.action == "attacking"
            ):
                self.stamina += 15 * dt

            # Prevent the player from springing for a period of time if their stamina reaches 0
            if self.stamina <= 0:
                self.recharging = True

            if self.recharging == True and self.stamina > 20:
                self.recharging = False

            # Only do sprinting or rolling if the player is moving

            # Sprinting
            if (
                (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
                and self.stamina > 0
                and self.recharging == False
                and (self.velocity_x != 0 or self.velocity_y != 0)
            ):
                self.speed = player_speed * 1.5
                self.action = "sprinting"
                self.stamina -= 60 * dt
            else:
                self.speed = player_speed

            # Only handle roll logic if the player is moving
            if self.velocity_x != 0 or self.velocity_y != 0:
                # Roll logic
                if not self.roll_started:
                    if keys[pygame.K_SPACE]:
                        if self.stamina > 10:
                            if not self.roll_started:
                                self.stamina -= 10

                            self.roll_started = True

                            self.frame_counter = 0

                elif self.roll_started:
                    self.roll(dt)

            # Attack logic
            if not self.attack_started:
                if mouse_buttons[0]:  # Left click
                    if self.stamina > 10 and self.attack_cooldown <= 0:
                        if not self.attack_started:
                            self.stamina -= 10

                        self.attack_started = True
                        self.frame_counter = 0

                elif mouse_buttons[2]:  # Right click
                    self.handle_defending(dt)

            elif self.attack_started == True:
                self.attack(dt)

    # Player Actions
    def attack(self, dt):
        self.action = "attacking"

    def roll(self, dt):
        self.action = "rolling"

    def handle_defending(self, dt):
        if self.defend_cooldown == 0:
            self.defend_cooldown = 0
            self.action = "defending"

            if not self.hit:
                self.current_frame = 1
                self.frame_counter = len(self.defend_frames) + 1

    def take_damage(self, damage):
        if not self.action == "defending":
            self.health -= damage
            self.current_frame = 0
            self.frame_counter = 0
            self.hurt_started = True
            self.can_move = False
            self.action = "hurt"
        else:
            self.hit = True
            self.stamina -= 20

    def move(self):
        if self.velocity_x > 0 or self.velocity_y > 0:
            self.hurt_started = False
            self.hurt_finished = False

        if self.action == "attacking":
            self.velocity_x *= 0.4
            self.velocity_y *= 0.4
        elif self.action == "defending":
            self.velocity_x *= 0.3
            self.velocity_y *= 0.3
        elif self.action == "rolling":
            self.velocity_x *= 2
            self.velocity_y *= 2

        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.rect.topleft = self.pos
        self.image_rect.center = self.rect.center

        # self.shadow_rect.bottomleft = self.collision_rect.bottomleft

    def update_frame(self, dt):
        self.frame_counter += self.animation_incrementer * dt

        if self.action == "idle":
            self.current_frame = (int(self.frame_counter)) % len(self.idle_frames)
            self.image = self.idle_frames[self.current_frame]

        elif self.action == "walking":
            self.current_frame = (int(self.frame_counter)) % len(self.walking_frames)
            self.image = self.walking_frames[self.current_frame]

        elif self.action == "sprinting":
            self.current_frame = (int(self.frame_counter)) % len(self.running_frames)
            self.image = self.running_frames[self.current_frame]

        elif self.action == "attacking":
            self.hurt_started = False
            self.hurt_finished = True

            self.current_frame = int(self.frame_counter) % (
                len(self.attack1_frames) + 1
            )

            if self.current_frame == len(self.attack1_frames):
                self.attack_started = False
                self.attack_cooldown = 0.2
            else:
                self.image = self.attack1_frames[self.current_frame]

        elif self.action == "rolling":
            self.current_frame = (int(self.frame_counter)) % len(self.roll_frames)
            self.image = self.roll_frames[self.current_frame]

            if self.current_frame == len(self.roll_frames) - 1:
                self.action = "idle"
                self.roll_started = False

        elif self.action == "defending":
            self.current_frame = (int(self.frame_counter)) % len(self.defend_frames)
            self.image = self.defend_frames[self.current_frame]

            if self.current_frame == len(self.defend_frames) - 1:
                self.action = "idle"
                self.hit = False
                self.defend_cooldown = 0.4

        elif self.action == "hurt":
            self.current_frame = int(self.frame_counter) % (len(self.hurt_frames))
            self.image = self.hurt_frames[self.current_frame]

            if self.current_frame == len(self.hurt_frames) - 1:
                self.hurt_finished = True

                self.action = "idle"

        elif self.action == "dead":
            self.current_frame = int(self.frame_counter) % (len(self.death_frames) + 1)

            if self.end_of_death == True:
                self.image = self.death_frames[len(self.death_frames) - 1]
            else:
                if self.current_frame == len(self.death_frames):
                    self.end_of_death = True
                else:
                    self.image = self.death_frames[self.current_frame]

        if self.stamina > 60:
            self.stamina = 60

        self.image = pygame.transform.scale(
            self.image, (self.width * scale_multiplier, self.height * scale_multiplier)
        )

        # Update the rect size and position based on the new image size
        self.rect.size = (self.rect_width, self.height * scale_multiplier)
        self.image_rect = self.image.get_rect(center=self.rect.center)

        if self.facing == "right":
            self.image = pygame.transform.flip(self.image, False, False)
        if self.facing == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    # Handle audio updates for sound effects related to the player
    def update_audio(self, dt):
        # Redefine the audio handler for simpler calling
        audio_handler = globals.game_context.audio_handler

        # Reduce sound effect timeouts by delta time
        self.movement_sfx_timeout -= dt

        # Checking if a sound effect for movement is currently playing
        if self.movement_sfx_timeout < 0:
            # If no movement sfx is currently playing, check if the aciton is walking
            if self.action == "walking":
                randomiser = str(random.randint(1,5))
                # Play the walking sound effect
                audio_handler.playSoundEffect(
                ["player", "footsteps", "walk", "grass", randomiser]
                )
                self.movement_sfx_timeout = 0.12
            elif self.action == "sprinting":
                randomiser = str(random.randint(1,3))
                audio_handler.playSoundEffect(
                    ["player", "footsteps", "sprint", "grass", randomiser]
                )
                self.movement_sfx_timeout = 0.10

        if not self.attacking_sfx_playing:
            if self.action == "attacking":
                randomiser = str(random.randint(1,8))
                audio_handler.playSoundEffect(
                    ["player", "attack", randomiser]
                )
                self.attacking_sfx_playing = True

    def update(self, dt):
        # Reduce cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        elif self.attack_cooldown < 0:
            self.attacking_sfx_playing = False
            self.attack_cooldown = 0

        if self.defend_cooldown > 0:
            self.defend_cooldown -= dt
        elif self.defend_cooldown < 0:
            self.defend_cooldown = 0

        # Allow player to move once hurt animation is finished
        if self.hurt_finished:
            self.hurt_started = False
            self.hurt_finished = False
            self.can_move = True
            self.hurt_counter = 0

        if not self.hurt_started:
            self.action = "idle"

        if self.health <= 0:
            self.action = "dead"
            self.can_move = False

        if self.health < self.max_health and self.action != "dead":
            self.heal_timeout -= dt
            if self.heal_timeout <= 0:
                self.health += self.heal_rate * dt

        if self.health > self.max_health:
            self.health = self.max_health

        self.user_input(dt)

        if self.can_move:
            if self.action == "attacking":
                self.pos[0] -= ((36 * scale_multiplier) - self.rect_width) * 0.5

                self.rect_width = 36 * scale_multiplier
            else:
                # if self.facing == "left":
                self.pos[0] -= ((20 * scale_multiplier) - self.rect_width) * 0.5

                self.rect_width = 20 * scale_multiplier

        self.update_frame(dt)
        self.update_audio(dt)
        self.move()
