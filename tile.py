import pygame
import os
from settings import *
import globals

from menus import e_prompt, statue_prompt
from ui import DialogueBox


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, width, height, pos, surf, groups, visible=True, opacity=255, name="Tile"
    ):
        super().__init__(groups)
        self.width = width
        self.height = height

        if surf:
            self.image = surf
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect(topleft=pos)

        if name:
            self.name = name
        else:
            self.name = "Tile"

        # Define the shadow image path
        shadow_image_path = f"assets/env/shadows/{self.name}.png"
        self.shadow_image = None

        # Check if the shadow image exists
        if os.path.exists(shadow_image_path):
            self.shadow_image = pygame.image.load(shadow_image_path).convert_alpha()
            self.shadow_image = pygame.transform.scale(
                self.shadow_image,
                (
                    self.shadow_image.get_width() * scale_multiplier,
                    self.shadow_image.get_height() * scale_multiplier,
                ),
            )
            self.shadow_image.set_alpha(64)
            # Assign shadow_rect for positioning
            self.shadow_rect = self.shadow_image.get_rect(
                bottomleft=self.rect.bottomleft
            )

        else:
            self.shadow_rect = None

        self.opacity = opacity
        self.visible = visible


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, width, height, left, top, groups, hitbox_id="Hitbox"):
        super().__init__(groups)
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.hitbox_id = hitbox_id

        # Corrected Rect initialization
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

        # Create a surface for the image and fill it with red
        if debugging:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 0))  # RGB color for red


class Rune(Tile):
    def __init__(
        self, width, height, pos, surf, groups, visible=True, opacity=155, name="Rune"
    ):
        super().__init__(width, height, pos, surf, groups, visible, opacity, name)

        self.teleport_player = False
        self.teleport_delay = 0.25
        self.teleport_counter = self.teleport_delay

        self.trigger_range = 32 * scale_multiplier
        self.teleport_range = 12 * scale_multiplier

    def check_trigger(self, player, dt):

        px = player.rect.centerx
        py = player.rect.centery + 32

        center_x = self.rect.centerx
        center_y = self.rect.centery

        dx = px - center_x
        dy = py - center_y

        dist = ((dx**2) + (dy**2)) ** 0.5

        if dist <= self.trigger_range:
            if self.opacity < 255:
                self.opacity += 5
        else:
            if self.opacity > 0:
                self.opacity -= 5

        if dist <= self.teleport_range:
            if self.teleport_counter > 0:
                self.teleport_counter -= self.teleport_delay * dt
            elif self.teleport_counter <= 0:
                self.teleport_player = True
        else:
            self.teleport_counter = self.teleport_delay

        # print(self.teleport_counter)
        self.image.set_alpha(self.opacity)


class Chest(Tile):
    def __init__(
        self,
        width,
        height,
        pos,
        surf,
        groups,
        items,
        visible=True,
        opacity=255,
        name="Tile",
    ):
        super().__init__(width, height, pos, surf, groups, visible, opacity, name)

        self.pos = pos
        self.state = "closed"
        self.items = items.split(",")
        self.trigger_range = 48 * scale_multiplier

    def check_trigger(self, player, dt):

        px = player.rect.centerx
        py = player.rect.centery + 32

        center_x = self.rect.centerx
        center_y = self.rect.centery

        dx = px - center_x
        dy = py - center_y

        dist = ((dx**2) + (dy**2)) ** 0.5

        if dist <= self.trigger_range:
            if self.state == "closed":
                e_prompt.visible = True
                keys = pygame.key.get_pressed()

                if keys[pygame.K_e] and self.state == "closed":
                    self.state = "opened"
                    e_prompt.visible = False

                    self.image = pygame.image.load(
                        "assets/env/structures/chest_opened.png"
                    ).convert_alpha()
                    self.image = pygame.transform.scale(
                        self.image, (32 * (screen_width / 640), 49 * scale_multiplier)
                    )
                    pos = (self.pos[0], self.pos[1] - (18 * scale_multiplier))
                    self.rect = self.image.get_rect(topleft=pos)

        else:
            e_prompt.visible = False


class Door(Tile):
    def __init__(
        self,
        width,
        height,
        pos,
        surf,
        groups,
        closed,
        visible=True,
        opacity=255,
        name="Tile",
    ):
        self.state = "closed" if closed else "open"
        self.trigger_range = 48 * scale_multiplier

        if closed:
            surf = pygame.image.load(
                "assets/env/structures/door_closed.png"
            ).convert_alpha()
        else:
            surf = pygame.image.load(
                "assets/env/structures/door_open.png"
            ).convert_alpha()

        super().__init__(width, height, pos, surf, groups, visible, opacity, name)

    def open_door(self):
        self.image = pygame.image.load(
            "assets/env/structures/door_open.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        for collision in globals.game_context.collision_group:
            if collision.hitbox_id == "Door":
                globals.game_context.collision_group.remove(collision)
                collision.kill()

    def check_trigger(self, player, dt):
        px = player.rect.centerx
        py = player.rect.centery + 32

        center_x = self.rect.centerx
        center_y = self.rect.centery

        dx = px - center_x
        dy = py - center_y

        dist = ((dx**2) + (dy**2)) ** 0.5

        keys = pygame.key.get_pressed()

        if dist <= self.trigger_range:
            if self.state == "closed":
                if keys[pygame.K_e]:
                    self.open_door()


class Statue(Tile):
    def __init__(
        self,
        width,
        height,
        pos,
        surf,
        groups,
        visible=True,
        opacity=255,
        dialogue_box=None,
        name="Tile",
    ):
        super().__init__(width, height, pos, surf, groups, visible, opacity, name)

        self.pos = pos
        self.state = "inactive"
        self.dialogue_box = dialogue_box
        self.trigger_range = 48 * scale_multiplier

    def check_trigger(self, player, dt):
        px = player.rect.centerx
        py = player.rect.centery + 32

        center_x = self.rect.centerx
        center_y = self.rect.centery

        dx = px - center_x
        dy = py - center_y

        dist = ((dx**2) + (dy**2)) ** 0.5

        keys = pygame.key.get_pressed()

        # if self.dialogue_box.visible == False:
        # self.state = 'inactive'

        # if dist <= self.trigger_range:
        #     if self.state == 'inactive':
        #         player.can_move = True
        #         statue_prompt.visible = True

        #         if keys[pygame.K_e]:
        #             self.state = 'active'
        #             statue_prompt.visible = False
        #             # self.dialogue_box.visible = True

        #     if self.state == 'active':
        #         player.can_move = False

        # else:
        #     statue_prompt.visible = False


class GodRay(pygame.sprite.Sprite):
    def __init__(self, points, groups):
        super().__init__(groups)

        # Calculate the bounding box of the polygon points
        scaled_points = [
            (p.x * scale_multiplier, p.y * scale_multiplier) for p in points
        ]
        min_x = min(point[0] for point in scaled_points)
        min_y = min(point[1] for point in scaled_points)
        max_x = max(point[0] for point in scaled_points)
        max_y = max(point[1] for point in scaled_points)

        # Create the surface size based on the bounding box
        width = max_x - min_x
        height = max_y - min_y
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Offset the points to fit within the surface
        offset_points = [(x - min_x, y - min_y) for x, y in scaled_points]

        # Define color (light, warm tone) and full opacity
        color = (255, 223, 186, 100)

        # Draw the polygon on the surface
        pygame.draw.polygon(self.surface, color, offset_points)

        # Store the actual position for blitting
        self.blit_pos = (min_x, min_y)

    def draw(self, display_surface, camera_offset):
        # Calculate the final position by accounting for the camera offset
        final_pos = (
            self.blit_pos[0] - camera_offset[0],
            self.blit_pos[1] - camera_offset[1],
        )
        display_surface.blit(self.surface, final_pos)
