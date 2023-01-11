from typing import List, Sequence

import pygame

from src.common import Position


def get_images(
    sheet: pygame.Surface,
    size: Sequence[int],
) -> List[pygame.Surface]:
    """
    Converts a sprite sheet to a list of surfaces
    Parameters:
        sheet: A pygame.Surface that contains the sprite sheet
        size: Size of a sprite in the sprite sheet
    """
    images = []

    width, height = size

    # loop through all sprites in the sprite sheet
    rows = int(sheet.get_height() / height)
    columns = int(sheet.get_width() / width)

    for row in range(rows):
        for col in range(columns):
            image = sheet.subsurface(pygame.Rect((col * width), (row * height), *size))

            images.append(image)

    return images


class Animation:
    def __init__(
        self,
        sprite_sheet: pygame.Surface,
        sprite_size: Sequence[int],
        speed: float,
    ):
        self.frames = get_images(sprite_sheet, sprite_size)
        self.speed = speed

        self.f_len = len(self.frames)

        self.index = 0
        self.animated_once = False

    def update(self, dt: float):
        self.index += self.speed * dt

        if self.index >= self.f_len:
            self.index = 0
            self.animated_once = True

    def draw(self, screen: pygame.Surface, pos: Position):
        frame = self.frames[int(self.index)]

        screen.blit(frame, pos)

    def play(self, screen: pygame.Surface, pos: Position, dt: float):
        self.update(dt)
        self.draw(screen, pos)
