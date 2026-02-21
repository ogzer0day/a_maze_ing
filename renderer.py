from typing import Optional, Set, Tuple

from mazegen import MazeGenerator

from constants import (
    COLORS, RST, BLD, DIM,
)


def render(
    m: MazeGenerator,
    path: Optional[Set[Tuple[int, int]]] = None,
    wc: str = "white",
    pc: str = "cyan",
    head: Optional[Tuple[int, int]] = None,
    visited: Optional[Set[Tuple[int, int]]] = None,
    stack: Optional[Set[Tuple[int, int]]] = None,
) -> str:
    """Render maze as colored ASCII art.

    Args:
        m: MazeGenerator instance.
        path: Optional set of path coordinates.
        wc: Wall color name.
        pc: Color for the 42 pattern cells.
        head: Current active cell for animation.
        visited: Visited cells for animation.
        stack: Stack/frontier cells for animation.

    Returns:
        Multi-line colored ASCII string.
    """
    cw: str = COLORS.get(wc, COLORS["white"])
    cp: str = COLORS.get(pc, COLORS["cyan"])
    lines: list[str] = []
    for y in range(m.height):
        top: str = ""
        mid: str = ""
        for x in range(m.width):
            c: int = m.grid[y][x]
            top += cw + "█" + RST
            if c & 1:
                top += cw + "███" + RST
            else:
                top += "   "
            if c & 8:
                mid += cw + "█" + RST
            else:
                mid += " "
            if (x, y) in m.blocked:
                mid += cp + "███" + RST
            elif head and (x, y) == head:
                mid += BLD + "\033[91m █ " + RST
            elif (x, y) == m.entry:
                mid += BLD + "\033[92m E " + RST
            elif (x, y) == m.exit:
                mid += BLD + "\033[91m X " + RST
            elif path and (x, y) in path:
                mid += "\033[93m \u2022 " + RST
            elif (
                stack is not None
                and (x, y) in stack
            ):
                mid += "\033[93m \u00b7 " + RST
            elif (
                visited is not None
                and (x, y) in visited
            ):
                mid += DIM + "\033[90m . " + RST
            else:
                mid += "   "
        last: int = m.grid[y][m.width - 1]
        top += cw + "█" + RST
        if last & 2:
            mid += cw + "█" + RST
        else:
            mid += " "
        lines.append(top)
        lines.append(mid)
    bot: str = ""
    for x in range(m.width):
        c = m.grid[m.height - 1][x]
        bot += cw + "█" + RST
        if c & 4:
            bot += cw + "███" + RST
        else:
            bot += "   "
    bot += cw + "█" + RST
    lines.append(bot)
    return "\n".join(lines)
