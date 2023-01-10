from typing import Sequence, TypeAlias, Union

import pygame

Position: TypeAlias = Union[Sequence, pygame.Vector2]
EventInfo: TypeAlias = dict

WIDTH, HEIGHT = 320, 192
TILE_SIZE = 16
