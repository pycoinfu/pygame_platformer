from typing import TypeAlias, Union, Sequence
import pygame

Position: TypeAlias = Union[Sequence, pygame.Vector2]
EventInfo: TypeAlias = dict

WIDTH, HEIGHT = 320, 192
TILE_SIZE = 16