from src.tile import Tile

import pygame
import pytmx 


class TileLayerMap:
    """
    Adds some functions like render_map and make_map to enhance pytmx's tilemap
    """

    def __init__(self, map_path: str):
        def overwritten_get_layer_by_name(name: str):
            try:
                return self.tilemap.layernames[name]
            except KeyError:
                return ()

        self.tilemap = pytmx.load_pygame(str(map_path))

        self.tilemap.get_layer_by_name = overwritten_get_layer_by_name

        self.width = self.tilemap.width * self.tilemap.tilewidth
        self.height = self.tilemap.height * self.tilemap.tileheight

        # Tiles will be filled in on render_map
        self.tiles = {}

    def render_map(
        self, surface: pygame.Surface
    ) -> None:
        """
        Renders the map to a given surface
        Parameters:
            surface: pygame.Surface to blit on
        """

        for layer_id, layer in enumerate(self.tilemap.visible_layers):
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    # Gets tile properties
                    tile_props = self.tilemap.get_tile_properties_by_gid(gid)
                    if tile_props is None:
                        continue

                    tile_img = self.tilemap.get_tile_image_by_gid(gid)

                    # Blit the tile image to surface
                    surface.blit(
                        tile_img,
                        (x * self.tilemap.tilewidth, y * self.tilemap.tileheight),
                    )

                    if tile_props["class"] == "collidable":
                        tile_instance = Tile(
                            tile_img,
                            (x * self.tilemap.tilewidth, y * self.tilemap.tileheight),
                        )
                        # Add tile instance to self.tiles
                        self.tiles[(x, y)] = tile_instance

    def make_map(self) -> pygame.Surface:
        """
        Makes a pygame.Surface, then render the map and return the rendered map
        Returns:
            A pygame.Surface to blit to the main screen
        """

        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render_map(temp_surface)
        return temp_surface

    def get_neighboring_tiles(self, radius: int, tile_pos: pygame.Vector2):
        """
        Gets the nearest `radius` tiles from `tile_pos`
        Parameters:
        radius: The desired radius of tiles to include
        tile_pos: The tile position
        """
        neighboring_tile_entities = []

        for x in range(int(tile_pos.x) - radius, int(tile_pos.x) + radius + 1):
            for y in range(int(tile_pos.y) - radius, int(tile_pos.y) + radius + 1):
                try:
                    tile = self.tiles[(x, y)]
                except KeyError:
                    # Outside map boundaries (for some reason)
                    continue

                neighboring_tile_entities.append(tile)

        return neighboring_tile_entities