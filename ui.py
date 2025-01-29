import pygame
from settings import *

pygame.font.init()

alagard = pygame.font.Font("./assets/fonts/alagard.ttf", 32)

speaker_color = (242, 219, 181)
text_color = (218, 167, 119)

dark = (32, 32, 32)


class HUD(pygame.sprite.Sprite):
    def __init__(self, target):
        self.pos = (64, 32)

        self.max_health = target.max_health
        self.max_armour = target.max_armour
        self.max_stamina = target.max_stamina

        self.health = target.health
        self.armour = target.armour
        self.stamina = target.stamina

        self.image = pygame.image.load("assets/ui/hud/info_filled.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (172 * scale_multiplier, 38 * scale_multiplier)
        )

        self.red_bar_width = 109
        self.red_bar = pygame.image.load("assets/ui/hud/red_bar.png").convert_alpha()
        self.red_bar = pygame.transform.scale(
            self.red_bar, (self.red_bar_width * scale_multiplier, 3 * scale_multiplier)
        )
        self.red_bar_pos = (
            self.pos[0] + (32 * scale_multiplier),
            self.pos[1] + (20 * scale_multiplier),
        )

        self.blue_bar_width = 82
        self.blue_bar = pygame.image.load("assets/ui/hud/blue_bar.png").convert_alpha()
        self.blue_bar = pygame.transform.scale(
            self.blue_bar,
            (self.blue_bar_width * scale_multiplier, 2 * scale_multiplier),
        )
        self.blue_bar_pos = (
            self.pos[0] + (32 * scale_multiplier),
            self.pos[1] + (26 * scale_multiplier),
        )

        self.green_bar_width = 139
        self.green_bar = pygame.image.load(
            "assets/ui/hud/green_bar.png"
        ).convert_alpha()
        self.green_bar = pygame.transform.scale(
            self.green_bar,
            (self.green_bar_width * scale_multiplier, 2 * scale_multiplier),
        )
        self.green_bar_pos = (
            self.pos[0] + (32 * scale_multiplier),
            self.pos[1] + (31 * scale_multiplier),
        )

        self.font = pygame.font.Font("./assets/fonts/alagard.ttf", 64)
        self.shards_info = self.font.render("0 0 0", True, speaker_color)
        self.shards_info_pos = (
            (screen_width - self.shards_info.get_width()) - 64,
            (screen_height - self.shards_info.get_height()) - 64,
        )
        # add to draw func and update pos

    def update_values(self, target):
        self.health = target.health
        self.armour = target.armour
        self.stamina = target.stamina

        self.health_percent = self.health / self.max_health
        self.armour_percent = self.armour / self.max_armour
        self.stamina_percent = self.stamina / self.max_stamina

        if self.stamina_percent < 0:
            self.stamina_percent = 0
        if self.health_percent < 0:
            self.health_percent = 0
        if self.armour_percent < 0:
            self.armour_percent = 0

        self.red_bar = pygame.image.load("assets/ui/hud/red_bar.png").convert_alpha()
        self.red_bar = pygame.transform.scale(
            self.red_bar,
            (
                (self.red_bar_width * self.health_percent) * scale_multiplier,
                3 * scale_multiplier,
            ),
        )

        self.blue_bar = pygame.image.load("assets/ui/hud/blue_bar.png").convert_alpha()
        self.blue_bar = pygame.transform.scale(
            self.blue_bar,
            (
                (self.blue_bar_width * self.armour_percent) * scale_multiplier,
                2 * scale_multiplier,
            ),
        )

        self.green_bar = pygame.image.load(
            "assets/ui/hud/green_bar.png"
        ).convert_alpha()
        self.green_bar = pygame.transform.scale(
            self.green_bar,
            (
                (self.green_bar_width * self.stamina_percent) * scale_multiplier,
                2 * scale_multiplier,
            ),
        )

    def draw(self, screen, target):
        self.update_values(target)

        screen.blit(self.image, self.pos)

        screen.blit(self.red_bar, self.red_bar_pos)
        screen.blit(self.blue_bar, self.blue_bar_pos)
        screen.blit(self.green_bar, self.green_bar_pos)

        # self.shards_info = self.font.render("0 0 0", True, speaker_color)
        screen.blit(self.shards_info, self.shards_info_pos)


class DialogueBox(pygame.sprite.Sprite):
    def __init__(self, speaker):
        self.font = alagard
        self.text_lines = []
        self.current_line = 0

        self.width = 1000
        self.height = 250
        self.visible = False

        # self.border_color = white
        self.color = dark

        self.text_lines = []
        self.current_line = 0

        self.speaker = speaker

        # Typing effect variables
        self.typing_speed = 5  # milliseconds per character
        self.last_char_time = pygame.time.get_ticks()
        self.char_index = 0
        self.line_index = 0
        self.line_skipped = False

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

        self.arrow_down = pygame.image.load(
            "assets/ui/hud/arrow_down.png"
        ).convert_alpha()
        self.arrow_down = pygame.transform.scale(
            self.arrow_down, (7 * scale_multiplier, 4 * scale_multiplier)
        )

        self.rename = None
        self.rename_line = None

    def add_line(self, line, rename=None):
        words = line.split(" ")
        wrapped_line = ""
        wrapped_array = []

        for word in words:
            # Create a temporary line to test if adding the next word exceeds the width
            temp_line = wrapped_line + word + " "
            text_screen = self.font.render(temp_line, True, text_color)

            # Check if the width of the rendered text exceeds the allowed width
            if text_screen.get_width() > (self.width - 48):  # 24 from each side
                # If it does, add the current wrapped line to the text_lines with a newline
                wrapped_array.append(wrapped_line.strip())  # Add current line
                wrapped_line = word + " "  # Start a new line with the current word
            else:
                wrapped_line = temp_line  # Add the word to the current line

        # Add any remaining text in wrapped_line to text_lines
        if wrapped_line:
            wrapped_array.append(wrapped_line.strip())

        self.text_lines.append(wrapped_array)

        if rename:
            self.rename = rename
            self.rename_line = len(self.text_lines)

    def next_line(self):

        if self.current_line < len(self.text_lines) - 1:
            self.current_line += 1

            try:
                if self.current_line == self.rename_line - 1:
                    self.speaker = self.rename
            except:
                pass
        else:
            self.visible = False

    def draw(self, screen, event_list):
        if self.visible:
            # Create a transparent screen
            transparent_screen = pygame.Surface(
                (self.width - 8, self.height - 8), pygame.SRCALPHA
            )
            transparent_screen.fill((*self.color, 191))

            # Blit the transparent background rectangle
            screen.blit(
                transparent_screen,
                (
                    (screen_width - self.width) / 2 + 4,
                    screen_height - self.height - 128 + 4,
                ),
            )

            speaker_title = self.font.render(self.speaker + ":", True, speaker_color)
            screen.blit(
                speaker_title,
                (
                    (screen_width - self.width) / 2 + 24,
                    screen_height - self.height - 128 + 24,
                ),
            )

            # Update character index based on typing speed
            current_time = pygame.time.get_ticks()
            if current_time - self.last_char_time > self.typing_speed:
                self.char_index += 1
                self.last_char_time = current_time

            # print(self.char_index)
            # Draw wrapped lines with typewriter effect
            if self.text_lines:
                for i, line in enumerate(self.text_lines[self.current_line]):
                    if not self.line_skipped:
                        if i <= self.line_index:
                            if i < self.line_index:
                                partial_text = line
                            else:
                                partial_text = line[: self.char_index]

                            if self.char_index > len(line) and self.line_index == i:
                                self.line_index = i + 1
                                self.char_index = 0

                            if (
                                self.char_index == len(line)
                                and self.line_index
                                == len(self.text_lines[self.current_line]) - 1
                            ):
                                self.line_skipped = True

                            text_screen = self.font.render(
                                partial_text, True, text_color
                            )
                            screen.blit(
                                text_screen,
                                (
                                    (screen_width - self.width) / 2 + 24,
                                    screen_height
                                    - self.height
                                    - 128
                                    + speaker_title.get_height()
                                    + 28
                                    + (i * self.font.get_height()),
                                ),
                            )
                    else:
                        text_screen = self.font.render(line, True, text_color)
                        screen.blit(
                            text_screen,
                            (
                                (screen_width - self.width) / 2 + 24,
                                screen_height
                                - self.height
                                - 128
                                + speaker_title.get_height()
                                + 28
                                + (i * self.font.get_height()),
                            ),
                        )

            # Blit border images
            screen.blit(
                self.border_tl,
                ((screen_width - self.width) / 2, screen_height - self.height - 128),
            )  # Top-left corner
            screen.blit(
                self.border_tr,
                (
                    (screen_width + self.width) / 2 - self.border_tr.get_width(),
                    screen_height - self.height - 128,
                ),
            )  # Top-right corner
            screen.blit(
                self.border_bl,
                (
                    (screen_width - self.width) / 2,
                    screen_height - 128 - self.border_bl.get_height(),
                ),
            )  # Bottom-left corner
            screen.blit(
                self.border_br,
                (
                    (screen_width + self.width) / 2 - self.border_br.get_width(),
                    screen_height - 128 - self.border_br.get_height(),
                ),
            )  # Bottom-right corner

            screen.blit(
                self.border_top,
                (
                    (screen_width - self.width) / 2 + (13 * scale_multiplier),
                    screen_height - self.height - 128,
                ),
            )
            screen.blit(
                self.border_bottom,
                (
                    (screen_width - self.width) / 2 + (13 * scale_multiplier),
                    screen_height - 128 - 4,
                ),
            )
            screen.blit(
                self.border_side,
                (
                    (screen_width - self.width) / 2,
                    screen_height - self.height - 128 + (13 * scale_multiplier),
                ),
            )
            screen.blit(
                self.border_side,
                (
                    (screen_width + self.width) / 2 - 4,
                    screen_height - self.height - 128 + (13 * scale_multiplier),
                ),
            )

            if self.current_line < len(self.text_lines) - 1:
                screen.blit(
                    self.arrow_down,
                    (
                        (screen_width - self.arrow_down.get_width()) / 2,
                        screen_height - self.arrow_down.get_height() - 128 - 24,
                    ),
                )

            for event in event_list:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.line_skipped:
                        self.next_line()
                        self.char_index = 0
                        self.line_index = 0
                        self.line_skipped = False
                    else:
                        self.line_skipped = True


class BossHealthBar(pygame.sprite.Sprite):
    def __init__(self, target_name, target_health=100):
        self.health = target_health
        self.name = target_name

        self.font = alagard
        self.boss_title = self.font.render(target_name, True, speaker_color)
        self.text_pos = ((screen_width - self.boss_title.get_width()) / 2, 32)

        self.image = pygame.image.load("assets/ui/hud/boss_bar.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (233 * scale_multiplier, 14 * scale_multiplier)
        )

        self.purple_bar_width = 231
        self.purple_bar = pygame.image.load(
            "assets/ui/hud/purple_bar.png"
        ).convert_alpha()
        self.purple_bar = pygame.transform.scale(
            self.purple_bar,
            (self.purple_bar_width * scale_multiplier, 4 * scale_multiplier),
        )

        self.pos = ((screen_width - self.image.get_width()) / 2, 64)

        self.background_pos = (
            self.pos[0] + scale_multiplier,
            (self.pos[1] + (6 * scale_multiplier)),
        )
        self.purple_bar_pos = (
            self.pos[0] + scale_multiplier,
            (self.pos[1] + (6 * scale_multiplier)),
        )

    def draw(self, screen):
        # Create a background screen behind the health bar
        background = pygame.Surface(
            (self.image.get_width() - (2 * scale_multiplier), 4 * scale_multiplier),
            pygame.SRCALPHA,
        )

        # Fill the background with a dark color (slightly transparent)
        background.fill((20, 20, 20, 200))

        screen.blit(background, self.background_pos)
        screen.blit(self.purple_bar, self.purple_bar_pos)
        # Blit Title & Bar Border
        screen.blit(self.boss_title, self.text_pos)
        screen.blit(self.image, self.pos)


class LocationDisplayer(pygame.sprite.Sprite):
    def __init__(self, location="???"):
        self.location = location
        self.displayed = False

        self.alpha = 0
        self.direction = "in"
        self.fade_speed = 2
        self.fade_timeout = 1

        self.font = pygame.font.Font("./assets/fonts/alagard.ttf", 96)
        self.text_color = (255, 255, 255)

    def set_location(self, new_location):
        self.location = new_location
        self.displayed = False
        self.alpha = 0
        self.direction = None
        # self.fade_timeout = 1
        self.start_fade_in()

    def start_fade_in(self):
        self.alpha = 0
        self.direction = "in"

    def start_fade_out(self):
        self.alpha = 255
        self.direction = "out"

    def update(self, dt):
        if self.direction == "in":
            if self.alpha < 255:
                self.alpha += self.fade_speed  # Increase opacity
            else:
                self.alpha = 255

                if self.fade_timeout > 0:

                    self.fade_timeout -= dt
                else:
                    self.direction = None  # Stop fading in
                    self.start_fade_out()

        elif self.direction == "out":
            if self.alpha > 0:
                self.alpha -= self.fade_speed  # Decrease opacity
            else:
                self.alpha = 0
                self.direction = None  # Stop fading out
                self.displayed = True

    def draw(self, screen, dt):
        if self.displayed == False:
            self.update(dt)

        if self.alpha > 0:
            location_text = self.font.render(self.location, True, self.text_color)
            location_text.set_alpha(self.alpha)
            pos = ((screen_width - location_text.get_width()) / 2, 320)

            mask = pygame.mask.from_surface(location_text)
            mask.invert()
            mask_surf = mask.to_surface(
                setcolor=(255, 255, 255, 0), unsetcolor=(27, 27, 27)
            )
            mask_surf.set_alpha(self.alpha)

            screen.blit(mask_surf, (pos[0] - 6, pos[1]))
            screen.blit(mask_surf, (pos[0] + 6, pos[1]))
            screen.blit(mask_surf, (pos[0], pos[1] - 6))
            screen.blit(mask_surf, (pos[0], pos[1] + 6))

            screen.blit(location_text, (pos))
