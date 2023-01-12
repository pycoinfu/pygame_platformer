import pygame
from pytmx import TiledObject

from src.animation import FadingImage
from src.common import FONT_PATH
from src.utils import render_text

pygame.font.init()


class Note:
    def __init__(self, obj: TiledObject, surface: pygame.Surface):
        self.surf = surface
        self.rect = pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height))
        self.pos = pygame.Vector2(self.rect.topleft)

        font = pygame.font.Font(FONT_PATH, 9)

        text = render_text(font, obj.properties["text"], (48, 44, 46))

        text_rect = text.get_rect(
            center=(self.rect.centerx, self.rect.y - text.get_height())
        )
        self.text_pos = pygame.Vector2(text_rect.topleft)

        self.text_fade = FadingImage(text, 75, 0)

        self.show_text = False

    def update(self, dt: float, player_rect: pygame.Rect):
        self.show_text = False
        if self.rect.colliderect(player_rect):
            self.show_text = True

        if self.show_text:
            self.text_fade.update(dt, fade_in=True)
        elif not self.show_text:
            self.text_fade.update(dt, fade_out=True)

    def draw(self, screen: pygame.Surface, scroll: pygame.Vector2):
        screen.blit(self.surf, self.pos - scroll)
        self.text_fade.draw(screen, self.text_pos - scroll)
