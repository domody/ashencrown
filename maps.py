import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from random import randint

from settings import *
import globals

from tile import Tile, Hitbox, Rune, Chest, Door, Statue, GodRay

from ui import BossHealthBar
from enemy.goblin import Goblin
from enemy.masked_orc import MaskedOrc


map_enemies = []
spawn_index = None


def generate_collision(obj):
    pos = obj.x * scale_multiplier, obj.y * scale_multiplier
    collision_group = globals.game_context.collision_group
    camera_group = globals.game_context.camera_group

    match obj.name:
        case "statue":
            hitbox = Hitbox(
                width=35 * scale_multiplier,
                height=20 * scale_multiplier,
                left=pos[0] + (1 * scale_multiplier),
                top=pos[1] + (obj.height * scale_multiplier) - 20 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "pillar_tall" | "pillar_short":
            hitbox = Hitbox(
                width=32 * scale_multiplier,
                height=25 * scale_multiplier,
                left=pos[0],
                top=pos[1] + (obj.height * scale_multiplier) - 25 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "archway":
            hitbox_left = Hitbox(
                width=16 * scale_multiplier,
                height=64 * scale_multiplier,
                left=pos[0],
                top=pos[1],
                groups=camera_group,
            )
            hitbox_right = Hitbox(
                width=16 * scale_multiplier,
                height=64 * scale_multiplier,
                left=pos[0] + (48 * scale_multiplier),
                top=pos[1],
                groups=camera_group,
            )

            collision_group.append(hitbox_left)
            collision_group.append(hitbox_right)
        case "wooden_box_big":
            hitbox = Hitbox(
                width=32 * scale_multiplier,
                height=30 * scale_multiplier,
                left=pos[0],
                top=pos[1] + (obj.height * scale_multiplier) - 30 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "wooden_box_small":
            pass
        case "stone_box":
            hitbox = Hitbox(
                width=32 * scale_multiplier,
                height=25 * scale_multiplier,
                left=pos[0],
                top=pos[1] + (obj.height * scale_multiplier) - 25 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "bench_left":
            hitbox = Hitbox(
                width=24 * scale_multiplier,
                height=46 * scale_multiplier,
                left=pos[0],
                top=pos[1] + (obj.height * scale_multiplier) - 46 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "bench_right":
            hitbox = Hitbox(
                width=24 * scale_multiplier,
                height=46 * scale_multiplier,
                left=pos[0] + (3 * scale_multiplier),
                top=pos[1] + (obj.height * scale_multiplier) - 46 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "pot1":
            hitbox = Hitbox(
                width=17 * scale_multiplier,
                height=8 * scale_multiplier,
                left=pos[0] + (2 * scale_multiplier),
                top=pos[1] + (obj.height * scale_multiplier) - 8 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "pot2":
            hitbox = Hitbox(
                width=20 * scale_multiplier,
                height=8 * scale_multiplier,
                left=pos[0] + (2 * scale_multiplier),
                top=pos[1] + (obj.height * scale_multiplier) - 8 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "pot3":
            hitbox = Hitbox(
                width=19 * scale_multiplier,
                height=5 * scale_multiplier,
                left=pos[0] + (1 * scale_multiplier),
                top=pos[1] + (obj.height * scale_multiplier) - 5 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "tree1":
            hitbox = Hitbox(
                width=11 * scale_multiplier,
                height=10 * scale_multiplier,
                left=pos[0] + (50 * scale_multiplier),
                top=pos[1] + (obj.height * scale_multiplier) - 10 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "tree2":
            hitbox = Hitbox(
                width=10 * scale_multiplier,
                height=10 * scale_multiplier,
                left=pos[0] + (36 * scale_multiplier),
                top=pos[1] + (obj.height * scale_multiplier) - 10 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "tree3":
            hitbox = Hitbox(
                width=11 * scale_multiplier,
                height=10 * scale_multiplier,
                left=pos[0] + (41 * scale_multiplier),
                top=pos[1] + (obj.height * scale_multiplier) - 10 * scale_multiplier,
                groups=camera_group,
            )
            collision_group.append(hitbox)
        case "door":
            hitbox = Hitbox(
                width=37 * scale_multiplier,
                height=8 * scale_multiplier,
                left=pos[0],
                top=pos[1] + (obj.height * scale_multiplier) - (8 * scale_multiplier),
                groups=camera_group,
                hitbox_id="Door",
            )
            collision_group.append(hitbox)


def load_map(
    context,
    file,
):
    global spawn_index
    trigger_group = context.trigger_group
    ground_tile_group = context.ground_tile_group
    light_group = context.light_group
    camera_group = context.camera_group
    collision_group = context.collision_group
    entity_group = context.entity_group
    enemy_group = context.enemy_group
    location_display = context.location_display
    audio_handler = context.audio_handler

    # Clear existing groups
    ground_tile_group.empty()
    camera_group.empty()
    trigger_group.clear()
    collision_group.clear()
    light_group.clear()

    tmx_data = load_pygame("maps/" + file)
    globals.current_map = file
    spawn_pos = None

    camera_group.first_instance = True
    try:
        location_display.set_location(tmx_data.properties["map_name"])
        audio_handler.setLocation(location=tmx_data.properties["map_name"])
    except:
        location_display.direction = None
        location_display.alpha = 0

    try:
        camera_group.set_limit_edges(tmx_data.properties["limit_edges"])
    except:
        camera_group.set_limit_edges(True)

    camera_group.set_map_dimensions(
        map_width=tmx_data.width * tmx_data.tilewidth,
        map_height=tmx_data.height * tmx_data.tilewidth,
    )

    # cycle through all layers
    for layer in tmx_data.visible_layers:
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * 32 * scale_multiplier, y * 32 * scale_multiplier)
                size = 32 * scale_multiplier
                Tile(
                    width=size,
                    height=size,
                    pos=pos,
                    surf=surf,
                    groups=ground_tile_group,
                )

    for obj in tmx_data.objects:
        pos = obj.x * scale_multiplier, obj.y * scale_multiplier
        if obj.type == "DynamicStructure":
            match obj.name:
                case "chest_closed":
                    trigger_group.append(
                        Chest(
                            width=obj.width * scale_multiplier,
                            height=obj.height * scale_multiplier,
                            pos=pos,
                            surf=obj.image,
                            groups=camera_group,
                            items=obj.items,
                            name=obj.name,
                        )
                    )
                case "statue":
                    statue = Statue(
                        width=obj.width * scale_multiplier,
                        height=obj.height * scale_multiplier,
                        pos=pos,
                        surf=obj.image,
                        groups=camera_group,
                        name=obj.name,
                    )
                    trigger_group.append(statue)
                case "door":
                    door = Door(
                        width=obj.width * scale_multiplier,
                        height=obj.height * scale_multiplier,
                        pos=pos,
                        surf=obj.image,
                        closed=obj.door_closed,
                        groups=camera_group,
                        name=obj.name,
                    )
                    trigger_group.append(door)
                case _:
                    Tile(
                        width=obj.width * scale_multiplier,
                        height=obj.height * scale_multiplier,
                        pos=pos,
                        surf=obj.image,
                        groups=camera_group,
                        name=obj.name,
                    )

        elif obj.type == "StaticStructure":
            match obj.name:
                case "platform_runes":
                    trigger_group.append(
                        Rune(
                            width=obj.width * scale_multiplier,
                            height=obj.height * scale_multiplier,
                            pos=pos,
                            surf=obj.image,
                            groups=ground_tile_group,
                            opacity=0,
                            name=obj.name,
                        )
                    )

                case "entrance":
                    visible = getattr(obj, "shadow_visible", False)
                    exit_index = getattr(obj, "exit_index", None)

                    trigger_group.append(
                        Entrance(
                            width=obj.width * scale_multiplier,
                            height=obj.height * scale_multiplier,
                            pos=pos,
                            color=(20, 20, 20),
                            visible=visible,
                            groups=ground_tile_group,
                            exit=obj.exit,
                            exit_index=exit_index,
                        )
                    )

                case _:
                    Tile(
                        width=obj.width * scale_multiplier,
                        height=obj.height * scale_multiplier,
                        pos=pos,
                        surf=obj.image,
                        groups=ground_tile_group,
                        name=obj.name,
                    )

        elif obj.type == "Fauna":
            Tile(
                width=obj.width * scale_multiplier,
                height=obj.height * scale_multiplier,
                pos=pos,
                surf=obj.image,
                groups=camera_group,
                name=obj.name,
            )

        elif obj.type == "Collision":
            objwidth = obj.width * scale_multiplier
            objheight = obj.height * scale_multiplier
            x = obj.x * scale_multiplier
            y = obj.y * scale_multiplier

            hitbox = Hitbox(
                width=objwidth, height=objheight, left=x, top=y, groups=camera_group
            )
            collision_group.append(hitbox)

        elif obj.type == "Enemy":
            match obj.enemy:
                case "goblin":
                    enemy = Goblin(camera_group, start_pos=(obj.x, obj.y))
                    
                case "masked_orc":
                    enemy = MaskedOrc(camera_group, start_pos=(obj.x, obj.y))
                    health_bar = BossHealthBar("Masked Orc", target_health=enemy.health)
                    globals.game_context.boss_health_bars.append([enemy, health_bar])
                    
            entity_group.add(enemy)
            enemy_group.add(enemy)

                

        elif obj.type == "GodRay":
            ray = GodRay(points=obj.points, groups=light_group)
            light_group.append(ray)

        elif obj.type == "Spawn":
            if spawn_index:
                if obj.index == spawn_index:
                    spawn_pos = (obj.x * scale_multiplier, obj.y * scale_multiplier)

            else:
                spawn_pos = (obj.x * scale_multiplier, obj.y * scale_multiplier)

        generate_collision(obj)

    spawn_index = None
    return spawn_pos


def teleport_player(
    file,
    player,
    context,
    pos=(0, 0),
):
    player_pos = pos

    spawn_pos = load_map(
        context=context,
        file=file,
    )

    player.add_to_camera_group(context.camera_group)

    if spawn_pos:
        player.pos = (
            spawn_pos[0] - (player.rect_width / 2),
            spawn_pos[1] - (player.height * scale_multiplier / 2),
        )
    else:
        player.pos = player_pos


class Transitioner(pygame.sprite.Sprite):
    def __init__(self, width, height, fade_color=(0, 0, 0), fade_speed=12):
        self.width = width
        self.height = height
        self.fade_color = (
            fade_color  # Color of the transition (e.g., black for a blackout)
        )
        self.fade_speed = (
            fade_speed  # Speed of the fade (increase or decrease per frame)
        )
        self.alpha = (
            0  # Starting transparency (0 = fully transparent, 255 = fully opaque)
        )
        self.direction = None  # 'in' for fade-in, 'out' for fade-out
        self.image = pygame.Surface((width, height))
        self.image.fill(fade_color)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()

        self.visible = False
        self.can_teleport_player = False
        self.player_can_move = True
        self.transiton_started = False

    def start_fade_in(self):
        self.alpha = 0
        self.direction = "in"
        self.visible = True
        self.transiton_started = True
        self.player_can_move = False

    def start_fade_out(self):
        self.alpha = 255
        self.direction = "out"
        self.visible = True

    def update(self):
        old_alpha = self.alpha
        if self.direction == "in":
            if self.alpha < 255:
                self.alpha += self.fade_speed  # Increase opacity
            else:
                self.alpha = 255
                self.direction = None  # Stop fading in
                self.can_teleport_player = True
                self.start_fade_out()

        elif self.direction == "out":
            if self.alpha > 0:
                self.alpha -= self.fade_speed  # Decrease opacity
            else:
                self.alpha = 0
                self.direction = None  # Stop fading out
                self.visible = False
                self.can_teleport_player = False
                self.transiton_started = False

        if self.alpha != old_alpha:
            self.image.set_alpha(self.alpha)  # Apply updated alpha to the surface

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, (0, 0))


class Entrance(pygame.sprite.Sprite):
    def __init__(
        self,
        width,
        height,
        pos,
        color,
        groups,
        exit,
        exit_index,
        visible=True,
        fade_percent=5,
    ):
        super().__init__(groups)
        self.width = width
        self.height = height
        self.pos = pos
        self.visible = visible
        self.fade_percent = fade_percent

        self.teleport_player = False
        self.exit = exit

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.image = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )  # Allow transparency

        self.exit_index = exit_index

        # Apply fade effect when creating the entrance
        self.create_fade_surface(color)

    def create_fade_surface(self, color):
        """Creates a surface with a fade effect from the given color to transparent."""
        fade_start = int(self.height * (1 - self.fade_percent / 100))

        # Fill the top part with the solid color
        self.image.fill(color, pygame.Rect(0, 0, self.width, fade_start))

        # Create the fade effect at the bottom
        for y in range(int(fade_start), int(self.height)):
            alpha = int(255 * (1 - (y - fade_start) / (self.height - fade_start)))
            # Create the color with decreasing alpha
            fade_color = (*color[:3], alpha)  # Take the RGB from color and add alpha
            self.image.fill(fade_color, pygame.Rect(0, y, self.width, 1))

    def check_trigger(self, player, dt):
        if (
            pygame.Rect.colliderect(player.rect, self.rect)
            and player.rect.bottom < self.rect.bottom
        ):
            self.teleport_player = True

            global spawn_index
            spawn_index = self.exit_index
