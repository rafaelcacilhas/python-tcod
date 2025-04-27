#!/usr/bin/env python3
from __future__ import annotations

import tcod.console
import tcod.context
import tcod.tileset

import globalState
from actions import EscapeAction, MovementAction
from input_handlers import EventHandler
from entity import Entity
from engine import Engine
from procgen import generate_dungeon

def main() -> None:

    screen_width = 80
    screen_height = 50
    
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 5   

    event_handler = EventHandler()
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0   ))
    entities = {npc, player}
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player
    )               

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    tcod.tileset.procedural_block_elements(tileset=tileset)

    globalState.console = tcod.console.Console(screen_width, screen_height)

    with tcod.context.new(console=globalState.console, tileset=tileset) as globalState.context:
        while True:
            engine.render(console=globalState.console, context=globalState.context)
            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == "__main__":
    main()
