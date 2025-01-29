import pygame
from pygame.locals import *
from random import randint

from settings import *

pygame.mixer.init()
pygame.mixer.music.set_volume(music_vol)


class AudioHandler(pygame.sprite.Sprite):
    def __init__(self):
        self.location = None

        self.background_music_started = False

    def setLocation(self, location):
        if not self.location == location:
            self.location = location
            self.background_music_started = False

    def startBackgroundMusic(self):
        match self.location:
            case "Enchanted Shrine":
                pygame.mixer.music.load("audio/background_music/enchanted_shrine.mp3")
                pygame.mixer.music.play(-1)
            case "Ashwood Flats":
                pygame.mixer.music.load("audio/background_music/bg_1.mp3")
                pygame.mixer.music.play(-1)

    def update(self):
        try:
            if not self.background_music_started:
                self.startBackgroundMusic()
                self.background_music_started = True

        except:
            # No audio device connected
            pass
