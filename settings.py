import pygame

# Initialize pygame (required to fetch display information)
pygame.init()

# Get the display resolution
display_info = pygame.display.Info()
screen_width = display_info.current_w  # Get the current display width
screen_height = display_info.current_h  # Get the current display height
scale_multiplier = screen_width / 640  # 640 x
debugging = True

fps = 144

# Player settings
player_start_x = 160 * scale_multiplier
player_start_y = 176 * scale_multiplier
player_speed = 320 * scale_multiplier

# Entity settings
base_speed = player_speed * 0.9