from typing import Sequence, Tuple

import pygame


class Background:
    """
    Parralax background class
    """

    def __init__(
        self,
        #                         layer           speed
        layers: Sequence[Tuple[pygame.Surface, float]],
    ):

        self.width = layers[0][0].get_width()
        self.layers = layers

    def draw_layer(
        self,
        screen: pygame.Surface,
        layer: pygame.Surface,
        scroll: pygame.Vector2,
        speed: float,
    ):
        """
        Draws a layer of the background on the screen
        Parameters:
                screen: Display surface
                layer: Image of the layer
                scroll: World scroll
                speed: Moving speed of the layer
        """
        x = -scroll.x * speed

        x %= self.width

        if abs(x) <= self.width:
            screen.blit(layer, (x, 0))
        if x != 0:
            screen.blit(layer, (x - self.width, 0))

    def draw(self, screen: pygame.Surface, world_scroll: pygame.Vector2):
        """
        Updates and draws all layers of the background
        Parameters:
                screen: Display surface
                world_scroll: World camera scroll
        """
        for layer, speed in self.layers:
            self.draw_layer(screen, layer, world_scroll, speed)
