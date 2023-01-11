import json

import pygame

from src.animation import Animation
from src.common import TILE_SIZE, EventInfo
from src.entity import Entity
from src.enums import PlayerStates
from src.tilemap import TileLayerMap
from typing import Dict


class Player(Entity):
    WALK_SPEED = 1
    IDLE_SPEED = 0.05
    SAVE_FILE = "assets/settings/player_save.json"

    def __init__(self, assets: Dict[str, pygame.Surface]):
        super().__init__()

        walk_right = [pygame.transform.flip(surf, True, False) for surf in assets["player_walk"]]
        idle_right = [pygame.transform.flip(surf, True, False) for surf in assets["player_idle"]]
        jump_right = [pygame.transform.flip(surf, True, False) for surf in assets["player_jump"]]
        self.animations = {
            "walk_right": Animation(walk_right, self.WALK_SPEED),
            "walk_left": Animation(assets["player_walk"], self.WALK_SPEED),
            "idle_right": Animation(idle_right,  self.IDLE_SPEED),
            "idle_left": Animation(assets["player_idle"], self.IDLE_SPEED),
            "jump_right": Animation(jump_right, 1),
            "jump_left": Animation(assets["player_jump"], 1),
        }

        self.load_save()

        self.speed = 1.5
        self.gravity = 0.5
        self.jump_height = 2.5
        self.vel = pygame.Vector2()
        self.rect = pygame.Rect(
            self.pos, assets["player_walk"][0].get_size()
        )

        self.facing = "right"
        self.state = PlayerStates.IDLE

    def move(self, event_info: EventInfo):
        keys = event_info["keys"]
        dt = event_info["dt"]

        self.vel.x = 0
        self.state = PlayerStates.IDLE

        if not (keys[pygame.K_d] and keys[pygame.K_a]):
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
