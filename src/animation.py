from typing import Sequence

import pygame

from src.common import Position


class Animation:
    def __init__(
        self,
        frames: Sequence[pygame.Surface],
        speed: float,
    ):
        self.frames = frames
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


class FadingImage:
    def __init__(self, surface: pygame.Surface, speed: float, starting_alpha: int):
        self.surface = surface
        self.speed = speed
        self.alpha = starting_alpha
        self.surface.set_alpha(starting_alpha)
        
    def fade_in(self, dt: float):
        self.alpha += self.speed * dt
        # this caps the alpha to 255
        self.alpha = min(255, self.alpha)
        self.surface.set_alpha(self.alpha)
    
    def fade_out(self, dt: float):
        self.alpha -= self.speed * dt
        # this sets the minimum alpha at 0
        self.alpha = max(0, self.alpha)
        self.surface.set_alpha(self.alpha)
    
    def update(self, dt: float, fade_in=False, fade_out=False):
        if fade_in:
            self.fade_in(dt)
        elif fade_out:
            self.fade_out(dt)
    
    def draw(self, screen: pygame.Surface, pos: Position):
        screen.blit(self.surface, pos)
