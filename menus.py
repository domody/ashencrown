import sys

import pygame
from pygame.locals import *

from settings import *
import globals

from save import generate_game_data, save_game, load_game

alagard48 = pygame.font.Font(
    "./assets/fonts/alagard.ttf", int(48 * (screen_height / 360))
)
alagard12 = pygame.font.Font(
    "./assets/fonts/alagard.ttf", int(12 * (screen_height / 360))
)

highlight_color = (242, 219, 181)
base_color = (218, 167, 119)
white = (255, 255, 255)


class MainMenu(pygame.sprite.Sprite):
    def __init__(self):
        self.background_image = pygame.image.load(
            "assets/menu/menu_bg1.png"
        ).convert_alpha()
        self.background_image = pygame.transform.scale(
            self.background_image, (screen_width, screen_height)
        )

        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))

        self.title_font = alagard48
        self.game_title = self.title_font.render("Ashen Crown", True, base_color)
        self.game_title_pos = (
            (screen_width - self.game_title.get_width()) / 2,
            65 * scale_multiplier,
        )

        self.game_title_highlight = self.title_font.render(
            "Ashen Crown", True, highlight_color
        )
        self.game_title_highlight_pos = (
            (screen_width - self.game_title.get_width()) / 2,
            68 * scale_multiplier,
        )

        self.options_font = alagard12

        self.start_game_button = self.options_font.render("Start game", True, white)
        self.start_game_button_pos = (
            (screen_width - self.start_game_button.get_width()) / 2,
            174 * scale_multiplier,
        )

        self.options_button = self.options_font.render("Options", True, white)
        self.options_button_pos = (
            (screen_width - self.options_button.get_width()) / 2,
            204 * scale_multiplier,
        )

        self.exit_game_button = self.options_font.render("Exit game", True, white)
        self.exit_game_button_pos = (
            (screen_width - self.exit_game_button.get_width()) / 2,
            234 * scale_multiplier,
        )

        # Define button rectangles for collision detection
        self.start_game_rect = pygame.Rect(
            self.start_game_button_pos[0],
            self.start_game_button_pos[1],
            self.start_game_button.get_width(),
            self.start_game_button.get_height(),
        )
        self.options_rect = pygame.Rect(
            self.options_button_pos[0],
            self.options_button_pos[1],
            self.options_button.get_width(),
            self.options_button.get_height(),
        )
        self.exit_game_rect = pygame.Rect(
            self.exit_game_button_pos[0],
            self.exit_game_button_pos[1],
            self.exit_game_button.get_width(),
            self.exit_game_button.get_height(),
        )

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.overlay, (0, 0))

        screen.blit(self.game_title_highlight, self.game_title_highlight_pos)
        screen.blit(self.game_title, self.game_title_pos)

        screen.blit(self.start_game_button, self.start_game_button_pos)
        screen.blit(self.options_button, self.options_button_pos)
        screen.blit(self.exit_game_button, self.exit_game_button_pos)

    def handle_event(
        self,
        context,
        event,
        options_menu,
        player,
        load_map,
    ):
        camera_group = context.camera_group
        transitioner = context.transitioner
        if (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        ):  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()

            if self.start_game_rect.collidepoint(mouse_pos):

                loaded_data = load_game(1)
                if loaded_data:
                    player_pos = loaded_data["player"]["position"]
                    current_map = loaded_data["world"]["current_map"]

                    player.pos = pygame.math.Vector2(player_pos["x"], player_pos["y"])
                    player.rect.topleft = player.pos
                    player.image_rect.center = player.rect.center
                    load_map(
                        context=context,
                        file=current_map,
                    )
                    player.add_to_camera_group(camera_group)
                    globals.game_context.collision_group
                    camera_group.first_instance = True
                    camera_group.offset.x = player.rect.centerx - camera_group.half_w
                    camera_group.offset.y = player.rect.centery - camera_group.half_h

                    globals.game_context.game_state = "game"

                    transitioner.alpha = 255
                    transitioner.player_can_move = False
                    transitioner.start_fade_out()
            
            elif self.options_rect.collidepoint(mouse_pos):
                options_menu.visible = True

            elif self.exit_game_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()


class OptionsMenu(pygame.sprite.Sprite):
    def __init__(self):
        self.visible = False
        self.background = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.background.fill((48, 37, 33, 255))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))


class PauseMenu(pygame.sprite.Sprite):
    def __init__(self):
        self.width = 120 * scale_multiplier
        self.height = 150 * scale_multiplier

        # Load and scale the border images
        self.border_tl = pygame.image.load(
            "assets/ui/hud/dialogue_outline_top_left.png"
        ).convert_alpha()
        self.border_tl = pygame.transform.scale(
            self.border_tl, (13 * scale_multiplier, 13 * scale_multiplier)
        )

        self.border_tr = pygame.image.load(
            "assets/ui/hud/dialogue_outline_top_right.png"
        ).convert_alpha()
        self.border_tr = pygame.transform.scale(
            self.border_tr, (13 * scale_multiplier, 13 * scale_multiplier)
        )

        self.border_bl = pygame.image.load(
            "assets/ui/hud/dialogue_outline_bottom_left.png"
        ).convert_alpha()
        self.border_bl = pygame.transform.scale(
            self.border_bl, (13 * scale_multiplier, 13 * scale_multiplier)
        )

        self.border_br = pygame.image.load(
            "assets/ui/hud/dialogue_outline_bottom_right.png"
        ).convert_alpha()
        self.border_br = pygame.transform.scale(
            self.border_br, (13 * scale_multiplier, 13 * scale_multiplier)
        )

        self.border_top = pygame.image.load(
            "assets/ui/hud/dialogue_outline_top.png"
        ).convert_alpha()
        self.border_top = pygame.transform.scale(
            self.border_top,
            (self.width - (26 * screen_width / 640), 1 * scale_multiplier),
        )

        self.border_side = pygame.image.load(
            "assets/ui/hud/dialogue_outline_side.png"
        ).convert_alpha()
        self.border_side = pygame.transform.scale(
            self.border_side,
            (1 * scale_multiplier, self.height - (26 * screen_width / 640)),
        )

        self.border_bottom = pygame.image.load(
            "assets/ui/hud/dialogue_outline_bottom.png"
        ).convert_alpha()
        self.border_bottom = pygame.transform.scale(
            self.border_bottom,
            (self.width - (26 * screen_width / 640), 1 * scale_multiplier),
        )

        self.transparent_screen = pygame.Surface(
            (screen_width, screen_height), pygame.SRCALPHA
        )
        self.transparent_screen.fill((0, 0, 0, 200))

    def draw(self, screen):  # Pass event list aswell
        # Blit the transparent background rectangle
        screen.blit(self.transparent_screen, (0, 0))

        # Blit border images
        screen.blit(
            self.border_tl,
            ((screen_width - self.width) / 2, (screen_height - self.height) / 2),
        )  # Top-left corner
        screen.blit(
            self.border_tr,
            (
                (screen_width + self.width) / 2 - self.border_tr.get_width(),
                (screen_height - self.height) / 2,
            ),
        )  # Top-right corner
        screen.blit(
            self.border_bl,
            (
                (screen_width - self.width) / 2,
                (screen_height + self.height) / 2 - self.border_bl.get_height(),
            ),
        )  # Bottom-left corner
        screen.blit(
            self.border_br,
            (
                (screen_width + self.width) / 2 - self.border_br.get_width(),
                (screen_height + self.height) / 2 - self.border_br.get_height(),
            ),
        )  # Bottom-right corner

        screen.blit(
            self.border_top,
            (
                (screen_width - self.width) / 2 + (13 * scale_multiplier),
                (screen_height - self.height) / 2,
            ),
        )
        screen.blit(
            self.border_bottom,
            (
                (screen_width - self.width) / 2 + (13 * scale_multiplier),
                (screen_height + self.height) / 2 - self.border_bottom.get_height(),
            ),
        )
        screen.blit(
            self.border_side,
            (
                (screen_width - self.width) / 2,
                (screen_height - self.border_side.get_height()) / 2,
            ),
        )
        screen.blit(
            self.border_side,
            (
                (screen_width + self.width) / 2 - 4,
                (screen_height - self.border_side.get_height()) / 2,
            ),
        )


class PromptKey(pygame.sprite.Sprite):
    def __init__(self, prompt_key, visible=True):
        self.prompt_key = prompt_key

        self.visible = visible

        self.width = 16 * scale_multiplier

        self.unpressed_image = pygame.image.load(
            "assets/keys/unpressed/" + prompt_key + "_key.png"
        )
        self.pressed_image = pygame.image.load(
            "assets/keys/pressed/" + prompt_key + "_key.png"
        )

        self.counter = 0
        self.unpressed = True

        # Get the original dimensions
        unpressed_width, unpressed_height = self.unpressed_image.get_size()
        pressed_width, pressed_height = self.pressed_image.get_size()

        # Calculate the scaling factor for width and scale the screen_height proportionally
        unpressed_scale_factor = self.width / unpressed_width
        pressed_scale_factor = self.width / pressed_width

        # Scale the images, maintaining aspect ratio
        self.unpressed_image = pygame.transform.scale(
            self.unpressed_image,
            (int(self.width), int(unpressed_height * unpressed_scale_factor)),
        )
        self.pressed_image = pygame.transform.scale(
            self.pressed_image,
            (int(self.width), int(pressed_height * pressed_scale_factor)),
        )

        self.diff = int(unpressed_height * unpressed_scale_factor) - int(
            pressed_height * pressed_scale_factor
        )

    def draw(self, screen):

        if self.visible:
            if self.unpressed:
                screen.blit(self.unpressed_image, (screen_width - self.width - 64, 64))
            elif self.unpressed == False:
                screen.blit(
                    self.pressed_image, (screen_width - self.width - 64, 64 + self.diff)
                )

            self.counter += 1

        if self.counter >= 33:
            self.counter = 0
            self.unpressed = not self.unpressed


e_prompt = PromptKey("e", visible=False)
statue_prompt = PromptKey("e", visible=False)


# def draw(self, screen):
#     monogram = pygame.font.Font('./assets/fonts/monogram-extended.ttf', 96)

#     prompt_text = monogram.render('Open', True, (255, 255, 255))

#     if self.visible:
#         if self.unpressed:
#             screen.blit(self.unpressed_image, (width - self.width - 64, 64))
#         elif self.unpressed == False:
#             screen.blit(self.pressed_image, (width - self.width - 64, 64 + self.diff))

#         screen.blit(prompt_text, (width - prompt_text.get_width() - self.width - 96, 56))

#         self.counter += 1

#     if self.counter >= 33:
#         self.counter = 0
#         self.unpressed = not self.unpressed
