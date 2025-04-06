"""This module stores globally mutable variables used by this program."""
# TODO - Change this file name since globals is used

from __future__ import annotations

import tcod.context
import tcod.ecs
import game

context: tcod.context.Context
"""The window managed by tcod."""

world: tcod.ecs.Registry
"""The active ECS registry and current session."""

states: list[game.state.State] = []

console = tcod.console.Console(80, 50, order="F")
