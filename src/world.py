import json

import pygame

from src.assets import load_assets
from src.background import Background
from src.common import HEIGHT, SETTINGS_PATH, WIDTH, EventInfo
from src.interactables import Note
from src.npc import NPC
from src.player import Player
from src.tilemap import TileLayerMap


class WorldInitStage:
    def __init__(self):
        self.world_scroll = pygame.Vector2()
        self.assets = load_assets("level")
        self.tilemap = TileLayerMap("assets/maps/map.tmx", self.assets)


class BackgroundStage(WorldInitStage):
    def __init__(self):
        super().__init__()

        background_layers = (
            [self.assets["bg_sky"], 0.005],
            [self.assets["bg_clouds"], 0.05],
            [self.assets["bg_land"], 0.1],
        )
        self.background = Background(background_layers)

    def draw(self, screen: pygame.Surface):
        self.background.draw(screen, self.world_scroll)


class PlayerStage(BackgroundStage):
    def __init__(self):
        super().__init__()

        self.player = Player(self.assets)
        self.world_scroll = self.player.pos.copy()

    def update(self, event_info: EventInfo):
        self.player.update(event_info, self.tilemap)

    def draw(self, screen: pygame.Surface, event_info: EventInfo):
        super().draw(screen)

        self.player.draw(screen, self.world_scroll, event_info)

    def save(self):
        self.player.save()


class NPCStage(PlayerStage):
    def __init__(self):
        super().__init__()

        self.npcs = {NPC("bunny", self.assets)}

    def update(self, event_info: EventInfo):
        super().update(event_info)

        for npc in self.npcs:
            npc.update(event_info, self.tilemap, self.player)

    def draw(self, screen: pygame.Surface, event_info: EventInfo):
        super().draw(screen, event_info)

        for npc in self.npcs:
            npc.draw(screen, self.world_scroll, event_info)

    def save(self):
        super().save()

        for npc in self.npcs:
            npc.save()


class InteractableStage(NPCStage):
    def __init__(self):
        super().__init__()

        self.notes = {
            Note(obj, self.assets["note"])
            for obj in self.tilemap.tilemap.get_layer_by_name("notes")
        }

    def update(self, event_info: EventInfo):
        super().update(event_info)

        for note in self.notes:
            note.update(event_info["dt"], self.player.rect)

    def draw(self, screen: pygame.Surface, event_info: EventInfo):
        super().draw(screen, event_info)

        for note in self.notes:
            note.draw(screen, self.world_scroll)


class TileStage(InteractableStage):
    def __init__(self):
        super().__init__()

        self.map_surf = self.tilemap.make_map()

    def draw(self, screen: pygame.Surface, event_info: EventInfo):
        super().draw(screen, event_info)

        screen.blit(self.map_surf, -self.world_scroll)


class CameraStage(TileStage):
    def update(self, event_info: EventInfo):
        super().update(event_info)

        dt = event_info["dt"]
        self.world_scroll.x += (
            dt * (self.player.rect.x - round(self.world_scroll.x) - WIDTH / 2) / 5
        )
        self.world_scroll.y += (
            dt * (self.player.rect.y - round(self.world_scroll.y) - HEIGHT / 1.4) / 5
        )


class World(CameraStage):
    pass
