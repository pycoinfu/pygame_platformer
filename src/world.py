import pygame

from src.background import Background
from src.common import HEIGHT, WIDTH, EventInfo
from src.player import Player
from src.tilemap import TileLayerMap


class WorldInitStage:
    def __init__(self):
        self.world_scroll = pygame.Vector2()
        self.tilemap = TileLayerMap("assets/maps/map.tmx")


class BackgroundStage(WorldInitStage):
    def __init__(self):
        super().__init__()

        background_layers = (
            [pygame.image.load("assets/gfx/bg/bg_sky.png").convert(), 0.005],
            [pygame.image.load("assets/gfx/bg/bg_clouds.png").convert_alpha(), 0.05],
            [pygame.image.load("assets/gfx/bg/bg_land.png").convert_alpha(), 0.1],
        )
        self.background = Background(background_layers)

    def draw(self, screen: pygame.Surface):
        self.background.draw(screen, self.world_scroll)


class PlayerStage(BackgroundStage):
    def __init__(self):
        super().__init__()

        self.player = Player()
        self.world_scroll = self.player.pos.copy()

    def update(self, event_info: EventInfo):
        self.player.update(event_info, self.tilemap)

    def draw(self, screen: pygame.Surface, event_info: EventInfo):
        super().draw(screen)

        self.player.draw(screen, self.world_scroll, event_info)

    def save(self):
        self.player.save()


class TileStage(PlayerStage):
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
            dt * (self.player.pos.x - self.world_scroll.x - WIDTH / 2) / 5
        )
        self.world_scroll.y += (
            dt * (self.player.pos.y - self.world_scroll.y - HEIGHT / 1.4) / 5
        )


class World(CameraStage):
    pass
