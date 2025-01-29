import pygame
from camera import CameraGroup
from entityGroup import EntityGroup
from enemy.enemyGroup import EnemyGroup
from audio import AudioHandler
from ui import LocationDisplayer
from maps import Transitioner
from settings import *

pygame.init()

# Global variables


screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)


# Game Context
class GameContext:
    def __init__(self):
        # Groups
        self.trigger_group = []
        self.ground_tile_group = pygame.sprite.Group()
        self.light_group = []
        self.camera_group = CameraGroup()
        self.collision_group = []
        self.entity_group = EntityGroup()
        self.enemy_group = EnemyGroup()
        self.location_display = LocationDisplayer("???")
        self.audio_handler = AudioHandler()
        self.transitioner = Transitioner(screen_width, screen_height)
        # Ref vars
        self.game_state = "menu"
        self.cutscene = "game_state"


collision_group = []
trigger_group = []
light_group = []

game_context = GameContext()