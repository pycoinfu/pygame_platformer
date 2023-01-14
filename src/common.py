from typing import Sequence, Tuple, TypeAlias, Union

import pygame

Position: TypeAlias = Union[Sequence, pygame.Vector2]
EventInfo: TypeAlias = dict
Color: TypeAlias = Union[pygame.Color, Tuple[int, int, int], str, int]

WIDTH, HEIGHT = 320, 192
TILE_SIZE = 16

FONT_PATH = "assets/misc/PixeloidSans.ttf"
SETTINGS_PATH = "assets/settings"
NPC_SETTINGS_PATH = SETTINGS_PATH + "/npc_settings.json"
NPC_GFX_PATH = "assets/gfx/npcs"
ENEMY_SETTINGS_PATH = SETTINGS_PATH + "/enemy_settings.json"
