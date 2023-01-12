import pygame

from src.common import Color


def render_text(font: pygame.font.Font, text: str, color: Color) -> pygame.Surface:
    text_arr = text.split("\n")
    # getting the sizes of each line, in pixels
    line_sizes = [[size for size in font.size(line)] for line in text_arr]
    # calculating the size of the text surface
    width = sum([size[0] for size in line_sizes])
    height = sum([size[1] for size in line_sizes])
    # creating a surface based on the calculations
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    rect = surf.get_rect()
    for i, line in enumerate(text_arr):
        # rendered line
        line_surf = font.render(line, False, color)
        # rect for the rendered line
        line_rect = line_surf.get_rect()
        # text should be centered
        line_rect.centerx = rect.centerx
        # getting the y coordinate of the line
        y = i * height / len(text_arr)
        line_rect.y = y

        surf.blit(line_surf, line_rect)

    return surf
