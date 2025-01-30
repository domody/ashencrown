import pygame
from pygame.locals import *
from random import randint
from settings import *
import globals

pygame.mixer.init()
pygame.mixer.music.set_volume(music_vol)


class AudioHandler(pygame.sprite.Sprite):
    def __init__(self):
        self.location = None

        self.background_music_started = False
        self.player_walk_channel = pygame.mixer.Channel(2)

    def setLocation(self, location):
        if not self.location == location:
            self.location = location
            self.background_music_started = False

    def startBackgroundMusic(self):

        if globals.game_context.game_state == "game" or globals.game_context.game_state == "cutscene":
            match self.location:
                case "Enchanted Shrine":
                    pygame.mixer.music.load("audio/background_music/enchanted_shrine.mp3")
                    pygame.mixer.music.play(-1)
                case "Ashwood Flats":
                    pygame.mixer.music.load("audio/background_music/bg_1.mp3")
                    pygame.mixer.music.play(-1)
        else: 
            self.background_music_started = False

    def stopBackgroundMusic(self):
        pygame.mixer.music.stop()

    # Get the sound path from the sound library
    def getNestedValue(self, keys, default=None):
        #
        sound_library = globals.sound_library
        for key in keys:
            sound_library = sound_library.get(key, {})
            if sound_library == {}:  # If key is missing, return default
                return default
        return sound_library

    def playSoundEffect(self, path: list, channel=None):
        sound_file = self.getNestedValue(path)
        sound_effect = pygame.mixer.Sound(sound_file)
        sound_effect.set_volume(sound_vol)
        if "player" in path:
            self.player_walk_channel.play(sound_effect)
        else:
            sound_effect.play()

    def update(self):
        try:
            if not self.background_music_started:
                self.background_music_started = True
                self.startBackgroundMusic()


        except:
            # No audio device connected
            pass
