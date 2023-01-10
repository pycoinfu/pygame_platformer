import pygame

from src.common import Position


class Tile:
    def __init__(self, image: pygame.Surface, pos: Position):
        self.image = image
        self.rect = pygame.Rect(pos, self.image.get_size())

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def __repr__(self):
        return f"Tile<{self.rect.topleft}>"
