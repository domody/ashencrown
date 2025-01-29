import pygame
from settings import *
import random

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
transparent = (0, 0, 0, 0)


class Enemy(pygame.sprite.Sprite):
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
        super().__init__(group)

        self.velocity_x = 0
        self.velocity_y = 0

        self.player_in_alert_range = False
        self.trigger_range = 160 * scale_multiplier
        self.attack_range = attack_range * scale_multiplier

        self.state = "idle"
        self.timeout = 0.3
        self.attack_cooldown = 0.2
        self.speed = base_speed

        self.los_blocked = False
        self.target_seen = False
        self.target_last_location = None

        self.color = green

        self.action = "idle"
        self.facing = "right"

        self.width = width * scale_multiplier
        self.height = height * scale_multiplier
        self.rect_width = rect_width * scale_multiplier

        self.max_health = health
        self.health = self.max_health

        self.can_move = True
        self.can_attack = True
        self.attack_started = False
        self.attack_finished = False
        self.attack_damage = attack_damage
        self.dealt_damage = False
        self.target_dead = False

        self.hurt = False
        self.hurt_started = False
        self.hurt_finished = False
        self.damaged = False

        self.dead = False
        self.end_of_death = False

        # Knockback variables
        self.knockback_active = False
        self.knockback_direction = pygame.math.Vector2(0, 0)
        self.knockback_speed = 1000  # Adjust for desired knockback speed
        self.knockback_duration = 0.1  # Knockback effect duration in seconds
        self.knockback_timer = 0  # Tracks the time remaining for knockback

        # Frame & Animation variables
        self.frame_counter = 0
        self.current_frame = 0
        self.animation_incrementer = animation_incrementer

        self.home_pos = (
            start_pos[0] * scale_multiplier,
            start_pos[1] * scale_multiplier,
        )
        self.wander_pos = None
        self.wander_range = 128
        self.pos = pygame.math.Vector2(
            start_pos[0] * scale_multiplier, start_pos[1] * scale_multiplier
        )

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

    def draw(self, screen, offset, target):
        adjusted_rect = self.rect.move(-offset.x, -offset.y)
        adjusted_img_rect = self.image_rect.move(-offset.x, -offset.y)
        adjusted_circ = [
            int(self.pos[0] - offset.x) + (self.rect_width / 2),
            int(self.pos[1] - offset.y) + (self.height / 2),
        ]

        # Calculate the center of the circle
        centercirc = (adjusted_circ[0], adjusted_circ[1])

        # Create a new Surface with per-pixel alpha
        circle_surface = pygame.Surface(
            (self.trigger_range * 2, self.trigger_range * 2), pygame.SRCALPHA
        )
        circle_surface = circle_surface.convert_alpha()

        adjusted_player_rect = target.move(-offset.x, -offset.y)

        # Draw the semi-transparent circle on the new Surface
        # pygame.draw.circle(circle_surface, (0, 0, 255, 100), (self.trigger_range, self.trigger_range), self.trigger_range)

        # Blit the new Surface with the semi-transparent circle onto the screen
        # screen.blit(circle_surface, (adjusted_circ[0] - self.trigger_range, adjusted_circ[1] - self.trigger_range))

        self.line_to_player = (adjusted_rect.center, adjusted_player_rect.center)

        # pygame.draw.line(screen, self.color, *self.line_to_player, width=4)
        pygame.draw.rect(screen, blue, adjusted_img_rect, 2, 1)
        pygame.draw.rect(screen, green, adjusted_rect, 2, 1)

        if self.player_in_alert_range:
            self.color = red
        elif self.state == "searching":
            self.color = blue
        else:
            self.color = green

    def check_collision_with_player(self, target):
        distance = pygame.math.Vector2(target.center).distance_to(self.rect.center)

        if self.health > 0:
            if distance <= self.trigger_range:
                self.player_in_alert_range = True
                self.target_seen = True
            else:
                self.player_in_alert_range = False

            if self.target_seen:
                if distance <= self.attack_range:
                    self.state = "attacking"
                    self.action = "idle"
                    self.can_move = False
                else:
                    self.state = "aggressive"
                    self.can_move = True

                if self.los_blocked:
                    self.state = "searching"
            else:
                self.state = "idle"

            if self.hurt:
                self.state = "hurt"
                self.hurt_started = True

                if not self.damaged:
                    self.take_damage(target)

            if target.center[0] < self.rect.center[0]:
                self.facing = "left"
            else:
                self.facing = "right"

    def update_self(self, target, offset, dt):
        self.velocity_x = 0
        self.velocity_y = 0

        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # If knockback is active, handle knockback movement
        if self.knockback_active:
            self.velocity_x = self.knockback_direction.x * self.knockback_speed * dt
            self.velocity_y = self.knockback_direction.y * self.knockback_speed * dt

            # Update the knockback timer
            self.knockback_timer -= dt
            if self.knockback_timer <= 0:
                self.knockback_active = False  # End knockback after duration

            self.action = "hurt"
        else:
            target_pos = pygame.math.Vector2(target.center) - offset
            goblin_pos = pygame.math.Vector2(self.rect.center) - offset

            if self.state == "hurt":
                self.action = "hurt"

            elif self.state == "aggressive":
                self.chase_target(dt, target, offset)

            elif self.state == "searching" and self.target_last_location:
                target_pos = pygame.math.Vector2(self.target_last_location) - offset

                direction = target_pos - goblin_pos

                distance = direction.length()

                if distance != 0:  # Avoid division by zero
                    direction = direction.normalize()

                    # Update the goblin's velocity
                    self.velocity_x = direction.x * self.speed * dt
                    self.velocity_y = direction.y * self.speed * dt

            elif self.state == "attacking":
                self.handle_attacking(dt)

            elif self.state == "idle":
                # self.handle_wandering(dt, offset)
                self.action = "idle"

            if self.hurt_started and not self.hurt:
                self.handle_hurt()

            if self.health <= 0:
                self.handle_death()

            if self.attack_finished:
                self.attack_finished = False
                self.attack_started = False
                self.action = "idle"
                self.dealt_damage = False

    def chase_target(self, dt, target, offset):
        target_pos = pygame.math.Vector2(target.center) - offset
        goblin_pos = pygame.math.Vector2(self.rect.center) - offset

        if self.timeout > 0:
            self.timeout -= dt

        if self.timeout <= 0 and self.can_move:
            self.action = "running"
            direction = target_pos - goblin_pos

            distance = direction.length()

            if distance != 0:  # Avoid division by zero
                direction = direction.normalize()

                # Update the goblin's velocity
                self.velocity_x = direction.x * self.speed * dt
                self.velocity_y = direction.y * self.speed * dt

        if self.target_last_location:
            self.target_last_location = None

    def handle_attacking(self, dt):
        if self.attack_cooldown <= 0:
            self.action = "attacking"

            if self.attack_started == False:
                self.frame_counter = 0
                self.current_frame = 0
                self.attack_started = True

    def handle_hurt(self):
        if self.hurt_finished:
            self.hurt_finished = False
            self.hurt_started = False

            self.frame_counter = 0
            self.current_frame = 0

        else:
            self.hurt_finished = True

        self.damaged = False

    def take_damage(self, target):
        self.health -= 10
        self.damaged = True

        self.frame_counter = 0
        self.current_frame = 0
        # Activate knockback
        self.knockback_active = True
        self.knockback_timer = self.knockback_duration

        # Calculate knockback direction (away from the player)
        direction_to_player = pygame.math.Vector2(
            self.rect.center
        ) - pygame.math.Vector2(target.center)
        if direction_to_player.length() != 0:
            self.knockback_direction = direction_to_player.normalize()

    def handle_death(self):
        if self.hurt_finished:
            self.state = "dead"
            self.action = "dead"
            if not self.dead:
                self.frame_counter = 0
                self.current_frame = 0
                self.dead = True

        self.can_move = False
        self.can_attack = False

    def handle_wandering(self, dt, offset):
        if not self.wander_pos:
            rand_x = (
                random.randint(-self.wander_range, self.wander_range) * scale_multiplier
            )
            rand_y = (
                random.randint(-self.wander_range, self.wander_range) * scale_multiplier
            )
            self.wander_pos = (self.home_pos[0] + rand_x, self.home_pos[1] + rand_y)

        elif self.wander_pos and self.pos != self.wander_pos:
            target_pos = pygame.math.Vector2(self.wander_pos)
            goblin_pos = pygame.math.Vector2(self.rect.center)

            self.action = "running"
            direction = target_pos - goblin_pos

            distance = direction.length()

            if distance != 0:  # Avoid division by zero
                direction = direction.normalize()

                # Update the goblin's velocity
                self.velocity_x = direction.x * self.speed * dt
                self.velocity_y = direction.y * self.speed * dt

        if tuple(map(int, self.wander_pos)) == self.rect.center:
            self.wander_pos = None

    def update_target_pos(self, dt, target, offset):
        self.check_collision_with_player(target)
        self.update_self(target, offset, dt)

    def update_frame(self, dt):
        self.frame_counter += self.animation_incrementer * dt

        if self.action == "idle":
            self.current_frame = (int(self.frame_counter)) % len(self.idle_frames)
            self.image = self.idle_frames[self.current_frame]

        elif self.action == "running":
            if self.attack_started:
                self.attack_started = False
                self.attack_finished = False

            self.current_frame = (int(self.frame_counter)) % len(self.running_frames)
            self.image = self.running_frames[self.current_frame]

        elif self.action == "attacking":
            self.hurt_started = False
            self.hurt_finished = True

            self.current_frame = int(self.frame_counter) % (len(self.attack1_frames))
            self.image = self.attack1_frames[self.current_frame]

            if self.current_frame == len(self.attack1_frames) - 1:
                self.attack_finished = True
                self.attack_cooldown = 0.2

        elif self.action == "hurt":
            self.current_frame = int(self.frame_counter) % (len(self.hurt_frames))
            self.image = self.hurt_frames[self.current_frame]

            if self.current_frame == len(self.hurt_frames) - 1 and self.hurt == False:
                self.hurt_finished = True

        elif self.action == "dead":
            self.current_frame = int(self.frame_counter) % (len(self.death_frames) + 1)

            if self.end_of_death == True:

                self.image = self.death_frames[len(self.death_frames) - 1]
            else:
                if self.current_frame == len(self.death_frames):
                    self.end_of_death = True
                else:
                    self.image = self.death_frames[self.current_frame]

        # Scale the image according to the current width and height
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Update the rect size and position based on the new image size
        self.rect.size = (self.rect_width, self.height)
        self.image_rect = self.image.get_rect(center=self.rect.center)

        if self.facing == "right":
            self.image = pygame.transform.flip(self.image, True, False)
        if self.facing == "left":
            self.image = pygame.transform.flip(self.image, False, False)

    def move(self, dt):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

        self.rect.topleft = self.pos
        self.image_rect.center = self.rect.center

    def update_incrementer(self):
        pass

    def update(self, dt):
        if self.target_dead:
            self.state = "idle"
            self.action = "idle"

        self.update_incrementer()
        self.update_frame(dt)
        self.move(dt)
