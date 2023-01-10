import pygame
from src.player import Player
from src.common import WIDTH, HEIGHT, EventInfo
from src.tilemap import TileLayerMap


class WorldInitStage:
	def __init__(self):
		self.world_scroll = pygame.Vector2()
		self.tilemap = TileLayerMap("assets/maps/test2.tmx")


class BackgroundStage(WorldInitStage):
	def __init__(self):
		super().__init__()

		self.bg = pygame.Surface((320, 192))
		self.bg.fill((20, 20, 20))
		
	def draw(self, screen: pygame.Surface):
		screen.blit(self.bg, (0, 0))


class PlayerStage(BackgroundStage):
	def __init__(self):
		super().__init__()

		self.player = Player()
		self.world_scroll = self.player.pos.copy()

	def update(self, event_info: EventInfo):
		self.player.update(event_info, self.tilemap)

	def draw(self, screen: pygame.Surface):
		super().draw(screen)

		self.player.draw(screen, self.world_scroll)

	def save(self):
		self.player.save()


class TileStage(PlayerStage):
	def __init__(self):
		super().__init__()
		
		self.map_surf = self.tilemap.make_map()

	def draw(self, screen: pygame.Surface):
		super().draw(screen)

		screen.blit(self.map_surf, -self.world_scroll)


class CameraStage(TileStage):
	def update(self, event_info: EventInfo):
		super().update(event_info)

		dt = event_info["dt"]
		self.world_scroll.x += dt * (self.player.pos.x - self.world_scroll.x - WIDTH / 2) / 5
		self.world_scroll.y += dt * (self.player.pos.y - self.world_scroll.y - HEIGHT / 1.5) / 5


class World(CameraStage):
	pass
