from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, _event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        if key == tcod.event.KeySym.UP or key ==tcod.event.KeySym.w:
            action = MovementAction(dx=0, dy=-1)
            print(action)
        elif key == tcod.event.KeySym.DOWN  or key == tcod.event.KeySym.s:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.a:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.KeySym.RIGHT  or key == tcod.event.KeySym.d:
            action = MovementAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action