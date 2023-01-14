import pygame
import json
from typing import Dict
from src.animation import Animation
from src.enums import EntityStates
from src.entity import Entity
from src.tilemap import TileLayerMap
from src.player import Player
from src.common import ENEMY_SETTINGS_PATH, Position, EventInfo, TILE_SIZE


class Enemy(Entity):
    def __init__(self, pos: Position, type_: str, assets: Dict[str, pygame.Surface]):
        super().__init__()

        self.type = type_
        self.load_save()

        walk_right = [
            pygame.transform.flip(surf, True, False)
            for surf in assets[f"{self.type}_walk"]
        ]
        idle_right = [
            pygame.transform.flip(surf, True, False)
            for surf in assets[f"{self.type}_idle"]
        ]
        jump_right = [
            pygame.transform.flip(surf, True, False)
            for surf in assets[f"{self.type}_jump"]
        ]
        self.animations = {
            "walk_right": Animation(walk_right, self.settings["walk_speed"]),
            "walk_left": Animation(
                assets[f"{self.type}_walk"], self.settings["walk_speed"]
            ),
            "idle_right": Animation(idle_right, self.settings["idle_speed"]),
            "idle_left": Animation(
                assets[f"{self.type}_idle"], self.settings["idle_speed"]
            ),
            "jump_right": Animation(jump_right, 1),
            "jump_left": Animation(assets[f"{self.type}_jump"], 1),
        }

        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2()
        self.rect = pygame.Rect(self.pos, assets[f"{self.type}_walk"][0].get_size())

        self.facing = "right"
        self.state = EntityStates.IDLE

    def move(self, event_info: EventInfo, player: Player):
        dt = event_info["dt"]
        diff = abs(player.rect.x - self.rect.x)

        self.vel.x = 0
        self.state = EntityStates.IDLE
        if diff <= self.settings["radius"] and not self.rect.colliderect(player.rect):
            self.state = EntityStates.WALK
            if player.rect.x > self.rect.x:
                self.vel.x = self.settings["speed"] * dt
                self.facing = "right"
            elif player.rect.x < self.rect.x:
                self.vel.x = -self.settings["speed"] * dt
                self.facing = "left"
        
        if self.colliding_with_tiles and not self.jumping:
            self.vel.y = -self.settings["jump_height"]
            self.jumping = True
            self.state = EntityStates.JUMP

        self.vel.y += self.GRAVITY * dt

    def update(self, event_info: EventInfo, tilemap: TileLayerMap, player: Player):
        self.move(event_info, player)
        
        collidable_tiles = tilemap.get_neighboring_tiles(
            2,
            pygame.Vector2(
                round(self.pos.x / TILE_SIZE),
                round(self.pos.y / TILE_SIZE),
            ),
        )
        self.handle_tile_collisions(collidable_tiles, event_info["dt"])
    
    def draw(
        self, screen: pygame.Surface, scroll: pygame.Vector2, event_info: EventInfo
    ):
        pos = ((self.pos.x - scroll.x), (self.rect.y - scroll.y))
        self.animations[f"{self.state.value}_{self.facing}"].play(
            screen, pos, event_info["dt"]
        )

    def load_save(self):
        with open(ENEMY_SETTINGS_PATH, "r") as f:
            settings = json.loads(f.read())
        self.settings = settings[self.type]
