import json

import pygame

from src.animation import Animation
from src.common import TILE_SIZE, EventInfo
from src.entity import Entity
from src.enums import PlayerStates
from src.tilemap import TileLayerMap


class Player(Entity):
    WALK_SIZE = (20, 19)
    WALK_SPEED = 1
    IDLE_SPEED = 0.05
    SAVE_FILE = "assets/settings/player_save.json"

    def __init__(self):
        super().__init__()

        walk = pygame.image.load("assets/gfx/player/player_walk.png").convert_alpha()
        idle = pygame.image.load("assets/gfx/player/player_idle.png").convert_alpha()
        jump = pygame.image.load("assets/gfx/player/player_jump.png").convert_alpha()
        self.animations = {
            "walk_right": Animation(
                pygame.transform.flip(walk, True, False),
                self.WALK_SIZE,
                self.WALK_SPEED,
            ),
            "walk_left": Animation(walk, self.WALK_SIZE, self.WALK_SPEED),
            "idle_right": Animation(
                pygame.transform.flip(idle, True, False),
                self.WALK_SIZE,
                self.IDLE_SPEED,
            ),
            "idle_left": Animation(idle, self.WALK_SIZE, self.IDLE_SPEED),
            "jump_right": Animation(
                pygame.transform.flip(jump, True, False), self.WALK_SIZE, 1
            ),
            "jump_left": Animation(jump, self.WALK_SIZE, 1),
        }

        self.load_save()

        self.speed = 1.5
        self.gravity = 0.5
        self.jump_height = 2.5
        self.vel = pygame.Vector2()
        self.rect = pygame.Rect(
            self.pos, self.animations["walk_right"].frames[0].get_size()
        )

        self.facing = "right"
        self.state = PlayerStates.IDLE

    def move(self, event_info: EventInfo):
        keys = event_info["keys"]
        dt = event_info["dt"]

        self.vel.x = 0
        self.state = PlayerStates.IDLE
        if keys[pygame.K_d]:
            self.vel.x = self.speed
            self.facing = "right"
            if not self.jumping:
                self.state = PlayerStates.WALK
        elif keys[pygame.K_a] and self.pos.x > 0:
            self.vel.x = -self.speed
            self.facing = "left"
            if not self.jumping:
                self.state = PlayerStates.WALK

        if not self.jumping and keys[pygame.K_SPACE]:
            self.jumping = True
            self.vel.y = -self.jump_height
            self.state = PlayerStates.JUMP

        self.vel.y += self.gravity * dt

    def update(self, event_info: EventInfo, tilemap: TileLayerMap):
        self.move(event_info)

        collidable_tiles = tilemap.get_neighboring_tiles(
            2,
            pygame.Vector2(
                round(self.pos.x / TILE_SIZE),
                round(self.pos.y / TILE_SIZE),
            ),
        )
        self.handle_tile_collisions(collidable_tiles)

    def draw(
        self, screen: pygame.Surface, scroll: pygame.Vector2, event_info: EventInfo
    ):
        pos = (self.pos.x - scroll.x, self.rect.y - scroll.y)
        self.animations[f"{self.state.value}_{self.facing}"].play(
            screen, pos, event_info["dt"]
        )

    def save(self):
        """
        Save the player's position into the json save file
        """
        save_data = {"pos": tuple(self.pos)}
        with open(self.SAVE_FILE, "w") as f:
            f.write(json.dumps(save_data, indent=4))

    def load_save(self):
        """
        Load the player's position from the json save file
        """
        with open(self.SAVE_FILE, "r") as f:
            save_data = json.loads(f.read())

        self.pos = pygame.Vector2(save_data["pos"])
