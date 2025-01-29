import sys
import os

import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from random import randint

from settings import *
from globals import game_context
import globals

# Camera & Misc
from camera import CameraGroup
from entityGroup import EntityGroup
from trigger import Trigger
from audio import AudioHandler
from save import generate_game_data, save_game, load_game

# Player & Map
from player import Player
from maps import load_map, teleport_player, Transitioner, Entrance

# UI
from menus import MainMenu, PauseMenu, OptionsMenu, e_prompt, statue_prompt
from ui import HUD, DialogueBox, LocationDisplayer, BossHealthBar

# Env
from tile import Tile, Hitbox, Rune, Chest, Statue
from env.collisionGroup import CollisionGroup
from tree import Tree
from env.wall import Wall

# Enemies
from enemy.enemyGroup import EnemyGroup
from enemy.goblin import Goblin

# os.environ['SDL_VIDEO_WINDOW_POS'] = "-2560,-1440"

# Initialize pygame, create window and set video mode, set caption
pygame.init()
fps_clock = pygame.time.Clock()
screen = globals.screen
pygame.display.set_caption("Ashen Crown")

# Menus
main_menu = MainMenu()
pause_menu = PauseMenu()
options_menu = OptionsMenu()

# Groups
audio_handler = game_context.audio_handler
camera_group = game_context.camera_group
enemy_group = game_context.enemy_group
entity_group = game_context.entity_group
ground_tile_group = game_context.ground_tile_group
transitioner = game_context.transitioner
statue = ""

dialogue_box = DialogueBox("???")
location_display = game_context.location_display

load_map(
    context=game_context,
    file="enchanted_shrine/main.tmx",
)

player = Player(camera_group)
entity_group.add(player)

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

hud = HUD(player)

# Cutscene Vars
cutscene_rect_height = 24 * scale_multiplier
cutscene_top_rect = pygame.Rect(0, 0, screen_width, cutscene_rect_height)
cutscene_bottom_rect = pygame.Rect(
    0, screen_height - cutscene_rect_height, screen_width, cutscene_rect_height
)

cutscene_counter = 2
load_cutscene_actions = True
cutscene_actions_finished = False
cutscene_postition_set = False
bossbar = BossHealthBar("Malrath, Sovereign of the Ruined Throne")

paused = False

font = pygame.font.Font("./assets/fonts/alagard.ttf", 32)
debug_pos = (64, 1000)

# Game loop.
while True:
    dt = fps_clock.tick(fps) / 1000  # Calculate delta time
    screen.fill("#060606")
    cutscene = game_context.cutscene
    event_list = pygame.event.get()
    for event in event_list:
        if globals.game_context.game_state == "menu":
            main_menu.handle_event(
                event=event,
                options_menu=options_menu,
                player=player,
                context=game_context,
                load_map=load_map,
            )

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
            and globals.game_context.game_state == "game"
        ):
            globals.game_context.game_state = "paused"
        elif (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
            and globals.game_context.game_state == "paused"
            and not options_menu.visible
        ):
            globals.game_context.game_state = "game"
        elif (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
            and options_menu.visible
        ):
            options_menu.visible = False

    if globals.game_context.game_state == "menu":
        main_menu.draw(screen=screen)

    elif globals.game_context.game_state == "cutscene":
        pygame.mouse.set_visible(False)
        player.can_move = False

        for enemy in enemy_group:
            enemy.can_move = False
            enemy.can_attack = False

        if cutscene == "game_start":
            if cutscene_postition_set == False:
                teleport_player(
                    "enchanted_shrine/main.tmx",
                    player=player,
                    context=game_context,
                )

                transitioner.fade_speed = 1
                transitioner.alpha = 255
                transitioner.start_fade_out()
                cutscene_postition_set = True

                dialogue_box.add_line(
                    "Long ago, the Ashen Crown was whole, a relic of power binding Edranor's realm, keeping darkness at bay."
                )
                dialogue_box.add_line("But pride led to ruin,")
                dialogue_box.add_line(
                    "and in their hubris, the lords of this land shattered the Crown into fragments."
                )
                dialogue_box.add_line("Charred Relics.")
                dialogue_box.add_line(
                    "Each binding its own power, each turning to ash and shadow."
                )
                dialogue_box.add_line(
                    "In these lands, now trusted and lost to time, the Charred Relics lie guarded." 
                )
                dialogue_box.add_line(
                    "The lords who hold them, - once human, now consumed - dwell in places forsaken."
                )
                dialogue_box.add_line("Their souls scorched.")
                dialogue_box.add_line("Their minds tainted.")

                dialogue_box.add_line("And you... you are Ashen-touched.")
                dialogue_box.add_line(
                    "A remnant from ages past, awakening here in this Enchanted Shrine - the last haven untouched by shadow."
                )
                dialogue_box.add_line(
                    "You have been chosen, bearer of a distant flame, to seek the Charred Relics,"
                )
                dialogue_box.add_line("And restore what has been broken.")
                dialogue_box.add_line(
                    "Your path will lead you through Edranor's cursed halls, "
                )
                dialogue_box.add_line("Through mountains scarred by ancient battles,")
                dialogue_box.add_line("Through towns now lost to ruin.")
                dialogue_box.add_line(
                    "Seek the Charred Relics, buried deep beneath the guardians who have long since abandoned humanity."
                )
                dialogue_box.add_line(
                    "Only when each Relic is in hand may you stand before Eldran, fallen ruler of this forsaken realm."
                )
                dialogue_box.add_line("Arise, and bear the weight of the Ashen Crown.")
                dialogue_box.add_line("Your burden is both purpose and curse.")
                dialogue_box.add_line("May the flames guide you,")
                dialogue_box.add_line("Ashen One.")

            if cutscene_counter <= 0:
                cutscene_counter = 0
            elif cutscene_counter > 0:
                cutscene_counter -= 2 * dt
                camera_group.first_instance = True

            if load_cutscene_actions:
                if cutscene_counter <= 0:
                    cutscene_counter = 0
                    dialogue_box.visible = True

                    load_cutscene_actions = False

            # Update.
            camera_group.update(dt)
            camera_group.custom_draw(player, dt, game_context)

            player.update_offset(camera_group.offset)
            player.update(dt)

            # Update the transitioner (fading effect)
            transitioner.update()
            transitioner.draw(screen)

            if cutscene_counter <= 0 and cutscene_actions_finished == False:
                if dialogue_box.visible == False and load_cutscene_actions == False:
                    cutscene_actions_finished = True
                    cutscene_counter = 1

            elif cutscene_counter >= 0 and cutscene_actions_finished:
                cutscene_rect_height = 24 * scale_multiplier * cutscene_counter

                cutscene_top_rect = pygame.Rect(
                    0, 0, screen_width, cutscene_rect_height
                )
                cutscene_bottom_rect = pygame.Rect(
                    0,
                    screen_height - cutscene_rect_height,
                    screen_width,
                    cutscene_rect_height,
                )

            elif cutscene_counter <= 0 and cutscene_actions_finished:
                globals.game_context.game_state = "game"
                player.can_move = True
                transitioner.fade_speed = 12

            dialogue_box.draw(screen, event_list)

        # Draw the cutscene border rectangles
        pygame.draw.rect(screen, black, cutscene_top_rect)
        pygame.draw.rect(screen, black, cutscene_bottom_rect)

    elif globals.game_context.game_state == "game":
        pygame.mouse.set_visible(False)
        # Update.
        camera_group.update(dt)
        camera_group.custom_draw(player, dt, game_context)

        # sprite_group.draw(screen)

        player.update_offset(camera_group.offset)

        player.update(dt)
        # wall.update(dt)

        enemy_group.update(dt, player, camera_group.offset)
        entity_group.update(dt, camera_group.offset, player.rect)

        # Debug
        if debugging:
            player.draw(screen, camera_group.offset)

            for enemy in enemy_group:
                enemy.draw(screen, camera_group.offset, player.rect)

        # Teleportation Triggers
        for trigger in game_context.trigger_group:
            trigger.check_trigger(player, dt)

            # Start the fade-in when stepping on a rune or entrance
            if transitioner.transiton_started == False:
                if isinstance(trigger, Rune) and trigger.teleport_player:
                    transitioner.start_fade_in()
                    trigger.teleport_player = False  # Prevent repeated triggers

                elif isinstance(trigger, Entrance) and trigger.teleport_player:
                    transitioner.start_fade_in()
                    trigger.teleport_player = False  # Prevent repeated triggers

            # If the fade-in has completed, handle the teleport logic
            if transitioner.can_teleport_player:
                if isinstance(trigger, Rune) and trigger.teleport_player:
                    teleport_player(
                        "boss_room_1_courtyard.tmx",
                        (790 * scale_multiplier, 763 * scale_multiplier),
                        player=player,
                        context=game_context,
                    )

                elif isinstance(trigger, Entrance) and trigger.teleport_player:
                    teleport_player(
                        trigger.exit + ".tmx", player=player, context=game_context
                    )

                transitioner.can_teleport_player = (
                    False  # Reset teleport flag after teleporting
                )
        6
        if transitioner.direction == "out":
            camera_group.first_instance = True
            player.can_move = False
        elif (
            transitioner.direction != "out"
            and transitioner.player_can_move == False
            and player.can_move == False
        ):
            player.can_move = True
            transitioner.player_can_move = True

        # Draw UI
        hud.draw(screen, player)

        # Show prompts:
        e_prompt.draw(screen)
        statue_prompt.draw(screen)

        dialogue_box.draw(screen, event_list)
        # bossbar.draw(screen=screen)

        location_display.draw(screen, dt)

        # Update the transitioner (fading effect)
        transitioner.update()
        transitioner.draw(screen)

        # print(player.pos, camera_group.limit_edges, camera_group.map_height, camera_group.map_width)

        for event in event_list:
            if event.type == KEYDOWN and event.key == K_i:
                game_data = generate_game_data(
                    player=player, current_map=globals.current_map
                )
                save_game(game_data)

    elif globals.game_context.game_state == "paused":
        camera_group.custom_draw(player, dt, game_context)
        location_display.draw(screen, dt)
        pause_menu.draw(screen)

    if options_menu.visible:
        options_menu.draw(screen=screen)

    debug = font.render(f"{game_context.game_state, game_context.cutscene}", True, (242, 219, 181))
    screen.blit(debug, debug_pos)

    audio_handler.update()
    # Flip display, tick fps
    # print(camera_group.offset)
    pygame.display.flip()
    fps_clock.tick(fps)

# With every tree asset and their respective shadow in ashwood flats, fps dips to 90 fps from 144/150
