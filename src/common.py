from typing import Sequence, Tuple, TypeAlias, Union

import pygame

Position: TypeAlias = Union[Sequence, pygame.Vector2]
EventInfo: TypeAlias = dict
Color: TypeAlias = Union[pygame.Color, Tuple[int, int, int], str, int]

WIDTH, HEIGHT = 320, 192
TILE_SIZE = 16

FONT_PATH = "assets/misc/PixeloidSans.ttf"
