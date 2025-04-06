"""State handling functions."""

from __future__ import annotations
from typing import Protocol, TypeAlias

import tcod.console

import attrs
import tcod.console
import tcod.constants
import tcod.event
from tcod.event import KeySym

import globalState
# from game.state import Pop, Push, Reset, StateResult, State
# import game.menus
# import game.world_tools
# from game.components import Gold, Graphic, Position
# from game.constants import DIRECTION_KEYS
# from game.state import Push, Reset, State, StateResult
# from game.tags import IsItem, IsPlayer

"""Base classes for states."""
class State(Protocol):
    """An abstract game state."""

    __slots__ = ()

    def on_event(self, event: tcod.event.Event) -> StateResult:
        """Called on events."""

    def on_draw(self, console: tcod.console.Console) -> None:
        """Called when the state is being drawn."""


@attrs.define()
class Push:
    """Push a new state on top of the stack."""

    state: State


@attrs.define()
class Pop:
    """Remove the current state from the stack."""


@attrs.define()
class Reset:
    """Replace the entire stack with a new state."""

    state: State


StateResult: TypeAlias = "Push | Pop | Reset | None"
"""Union of state results."""

def main_draw() -> None:
    """Render and present the active state."""
    if not globalState.states:
        return
    globalState.console.clear()
    globalState.states[-1].on_draw(globalState.console)
    globalState.context.present(globalState.console)


def apply_state_result(result: StateResult) -> None:
    """Apply a StateResult to `globalState.states`."""
    match result:
        case Push(state=state):
            globalState.states.append(state)
        case Pop():
            globalState.states.pop()
        case Reset(state=state):
            while globalState.states:
                apply_state_result(Pop())
            apply_state_result(Push(state))
        case None:
            pass
        case _:
            raise TypeError(result)


def main_loop() -> None:
    """Run the active state forever."""
    while True:
        main_draw()
        for event in tcod.event.wait():
            tile_event = globalState.context.convert_event(event)
            if globalState.states:
                apply_state_result(globalState.states[-1].on_event(tile_event))


def get_previous_state(state: State) -> State | None:
    """Return the state before `state` in the stack if it exists."""
    current_index = next(index for index, value in enumerate(globalState.states) if value is state)
    return globalState.states[current_index - 1] if current_index > 0 else None


def draw_previous_state(state: State, console: tcod.console.Console, dim: bool = True) -> None:
    """Draw previous states, optionally dimming all but the active state."""
    prev_state = get_previous_state(state)
    if prev_state is None:
        return
    prev_state.on_draw(console)
    if dim and state is globalState.states[-1]:
        console.rgb["fg"] //= 4
        console.rgb["bg"] //= 4

    """A collection of game states."""


# @attrs.define()
# class InGame(State):
#     """Primary in-game state."""

#     def on_event(self, event: tcod.event.Event) -> StateResult:
#         """Handle events for the in-game state."""
#         (player,) = globalState.world.Q.all_of(tags=[IsPlayer])
#         match event:
#             case tcod.event.Quit():
#                 raise SystemExit()
#             case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
#                 player.components[Position] += DIRECTION_KEYS[sym]
#                 # Auto pickup gold
#                 for gold in globalState.world.Q.all_of(components=[Gold], tags=[player.components[Position], IsItem]):
#                     player.components[Gold] += gold.components[Gold]
#                     text = f"Picked up {gold.components[Gold]}g, total: {player.components[Gold]}g"
#                     globalState.world[None].components[("Text", str)] = text
#                     gold.clear()
#                 return None
#             case tcod.event.KeyDown(sym=KeySym.ESCAPE):
#                 return Push(MainMenu())
#             case _:
#                 return None

#     def on_draw(self, console: tcod.console.Console) -> None:
#         """Draw the standard screen."""
#         for entity in globalState.world.Q.all_of(components=[Position, Graphic]):
#             pos = entity.components[Position]
#             if not (0 <= pos.x < console.width and 0 <= pos.y < console.height):
#                 continue
#             graphic = entity.components[Graphic]
#             console.rgb[["ch", "fg"]][pos.y, pos.x] = graphic.char, graphic.color

#         if text := globalState.world[None].components.get(("Text", str)):
#             console.print(x=0, y=console.height - 1, string=text, fg=(255, 255, 255), bg=(0, 0, 0))

# class MainMenu(game.menus.ListMenu):
#     """Main/escape menu."""

#     # __slots__ = ()

#     # def __init__(self) -> None:
#     #     """Initialize the main menu."""
#     #     items = [
#     #         game.menus.SelectItem("New game", self.new_game),
#     #         game.menus.SelectItem("Quit", self.quit),
#     #     ]
#     #     if hasattr(globals, "world"):
#     #         items.insert(0, game.menus.SelectItem("Continue", self.continue_))

#     #     super().__init__(
#     #         items=tuple(items),
#     #         selected=0,
#     #         x=5,
#     #         y=5,
#     #     )

#     # @staticmethod
#     # def continue_() -> StateResult:
#     #     """Return to the game."""
#     #     return Reset(InGame())

#     # @staticmethod
#     # def new_game() -> StateResult:
#     #     """Begin a new game."""
#     #     globalState.world = game.world_tools.new_world()
#     #     return Reset(InGame())

#     # @staticmethod
#     # def quit() -> StateResult:
#     #     """Close the program."""
#     #     raise SystemExit()