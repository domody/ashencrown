import pygame
from pygame.locals import *
from settings import *
import json
import globals


def generate_game_data(player, current_map):
    return {
        "player": {
            "position": {"x": player.pos[0], "y": player.pos[1]},
            "health": player.health,
        },
        "world": {
            "current_map": current_map,
        },
    }


def save_game(data, filename="savefile.json"):
    with open(filename, "w") as save_file:
        json.dump(data, save_file, indent=4)


def load_game(save: int, filename="savefile.json"):
    try:
        with open(filename, "r") as save_file:
            data = json.load(save_file)

        if data[str(save)]:
            return data[str(save)]
        else:
            return data["DEFAULT"]
    except:
        return data["DEFAULT"]
