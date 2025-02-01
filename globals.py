import pygame
from camera import CameraGroup
from entityGroup import EntityGroup
from enemy.enemyGroup import EnemyGroup
from audio import AudioHandler
from ui import LocationDisplayer, DialogueBox
from maps import Transitioner
from settings import *

pygame.init()

# Global variables
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Sound Library

sound_library = {
    "player": {
        "footsteps": {
            "crouch": {"dirt": {"1": None, "2": None}, "grass": {"1": None, "2": None}},
            "hard_walk": {
                "dirt": {"1": None, "2": None},
                "grass": {"1": None, "2": None},
            },
            "jump": {"dirt": {"1": None, "2": None}, "grass": {"1": None, "2": None}},
            "sprint": {
                "dirt": {"1": None, "2": None},
                "grass": {
                    "1": "audio/sfx/footsteps/grass/walk/1.ogg",
                    "2": "audio/sfx/footsteps/grass/walk/2.ogg",
                    "3": "audio/sfx/footsteps/grass/walk/3.ogg",
                    "4": "audio/sfx/footsteps/grass/walk/4.ogg",
                    "5": "audio/sfx/footsteps/grass/walk/5.ogg",
                },
            },
            "walk": {
                "dirt": {"1": None, "2": None},
                "grass": {
                    "1": "audio/sfx/footsteps/grass/walk/1.ogg",
                    "2": "audio/sfx/footsteps/grass/walk/2.ogg",
                    "3": "audio/sfx/footsteps/grass/walk/3.ogg",
                    "4": "audio/sfx/footsteps/grass/walk/4.ogg",
                    "5": "audio/sfx/footsteps/grass/walk/5.ogg",
                },
            },
        },
        "attack": {
            "1": "audio/sfx/attack/1.ogg",
            "2": "audio/sfx/attack/2.ogg",
            "3": "audio/sfx/attack/3.ogg",
            "4": "audio/sfx/attack/4.ogg",
            "5": "audio/sfx/attack/5.ogg",
            "6": "audio/sfx/attack/6.ogg",
            "7": "audio/sfx/attack/7.ogg",
            "8": "audio/sfx/attack/8.ogg",
        },
        "defend": {},
        "hurt": {},
        "death": {},
    },
    "goblin": {"footsteps": {}, "attack": {}, "defend": {}, "hurt": {}, "death": {}},
    "skeleton": {"footsteps": {}, "attack": {}, "defend": {}, "hurt": {}, "death": {}},
}


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
        self.dialogue_box = DialogueBox("???")
        self.sound_library = sound_library
        self.boss_health_bars = []
        # Ref vars
        self.game_state = "menu"
        self.cutscene = None
        self.save_file = "1"


game_context = GameContext()
