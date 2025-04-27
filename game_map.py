import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        
        self.visible = np.full((width, height), fill_value=False, order="F")    
        self.explored = np.full((width, height), fill_value=False, order="F")       


    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        for x in range(0,self.width):
            for y in range(0,self.height):
                if self.visible[x,y]:
                    console.rgb[y,x] = self.tiles[x,y]["light"]
                elif self.explored[x,y]:
                    console.rgb[y,x] = self.tiles[x,y]["dark"]
                else:
                    console.rgb[y,x] = tile_types.SHROUD

                

