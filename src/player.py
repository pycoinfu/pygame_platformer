from typing import Sequence
import pygame
from src.common import EventInfo, TILE_SIZE
from src.enums import PlayerStates
from src.tile import Tile
from src.entity import Entity
import json

from src.tilemap import TileLayerMap


class Player(Entity):
	SAVE_FILE = "assets/settings/player_save.json"
	def __init__(self):
		super().__init__()

		img = pygame.image.load("assets/gfx/kitty.png").convert_alpha()
		self.assets = {
			"walk_right": pygame.transform.flip(img, True, False),
			"walk_left": img,
			"idle_right": ...,
			"idle_left": ...,
		}

		self.load_save()

		self.speed = 1.5
		self.gravity = 0.5
		self.jump_height = 2.5
		self.vel = pygame.Vector2()
		self.rect = pygame.Rect(self.pos, self.assets["walk_right"].get_size())

		self.facing = "right"
		self.state = PlayerStates.WALK

	def move(self, event_info: EventInfo):
		keys = event_info["keys"]
		dt = event_info["dt"]

		self.vel.x = 0
		if keys[pygame.K_d]:
			self.vel.x = self.speed
			self.facing = "right"
		elif keys[pygame.K_a]:
			self.vel.x = -self.speed
			self.facing = "left"
		
		if not self.jumping and keys[pygame.K_SPACE]:
			self.jumping = True
			self.vel.y = -self.jump_height
		
		self.vel.y += self.gravity * dt

	def update(self, event_info: EventInfo, tilemap: TileLayerMap):
		self.move(event_info)

		collidable_tiles = tilemap.get_neighboring_tiles(
			2,
			pygame.Vector2(
				round(self.pos.x / TILE_SIZE),
				round(self.pos.y / TILE_SIZE),
			)
		)
		self.handle_tile_collisions(collidable_tiles)


	def draw(self, screen: pygame.Surface, scroll: pygame.Vector2):
		screen.blit(self.assets[f"walk_{self.facing}"], (self.pos.x - scroll.x, self.rect.y - scroll.y))


	def save(self):
		"""
		Save the player's position into the json save file
		"""
		save_data = {
			"pos": tuple(self.pos)
		}
		with open(self.SAVE_FILE, "w") as f:
			f.write(json.dumps(save_data))

	def load_save(self):
		"""
		Load the player's position from the json save file
		"""
		with open(self.SAVE_FILE, "r") as f:
			save_data = json.loads(f.read())

		self.pos = pygame.Vector2(save_data["pos"])
