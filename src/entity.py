import pygame
from typing import Sequence
from src.tile import Tile


class Entity:
    def __init__(self):
        self.pos = pygame.Vector2()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.vel = pygame.Vector2()
        self.jumping = False

    def handle_tile_collisions(self, tiles: Sequence[Tile]):
        """
        Handles the tile collision
        Parameters:
            neighboring_tiles: the entity's current closest tiles
        """
        self.pos.x += self.vel.x
        self.rect.x = round(self.pos.x)

        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.vel.x > 0:
                    self.rect.right = tile.rect.left
                    self.pos.x = self.rect.x
                elif self.vel.x < 0:
                    self.rect.left = tile.rect.right
                    self.pos.x = self.rect.x

        self.pos.y += self.vel.y
        self.rect.y = round(self.pos.y)
    
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.vel.y > 0:
                    self.vel.y = 0
                    self.jumping = False
                    self.rect.bottom = tile.rect.top
                    self.pos.y = self.rect.y
                elif self.vel.y < 0:
                    self.vel.y = 0
                    self.rect.top = tile.rect.bottom
                    self.pos.y = self.rect.y
