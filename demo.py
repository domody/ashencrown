# Import libraries and globals
import sys
import pygame
from pygame.locals import *

from settings import *
import globals

# Initialize pygame, create a fps_clock and a screen
pygame.init()
fps_clock = pygame.time.Clock()
screen = globals.screen
pygame.display.set_caption("Ashen Crown")

# Variables
game_state = globals.game_context.game_state

# Main game program
while True:
    # Regulates fps and calculates delta time
    dt = fps_clock.tick(fps) / 1000
    screen.fill("#060606")

    # Get all events from the event queue
    event_list = pygame.event.get()

    for event in event_list:
        # Quit game safely if the close button is pressed
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Basic game state setup
    if game_state == "menu":
        pass
    elif game_state == "cutscene":
        pass
    elif game_state == "game":
        pass
    elif game_state == "paused":
        pass

    # Update the display
    pygame.display.flip()
