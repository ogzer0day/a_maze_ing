import random
from typing import Dict, List, Optional, Set, Tuple

from mazegen.directions import (
    AnimCb, N, E, S, W,
    OPPOSITE, DX, DY, DIR_CH, P4, P2,
)


class MazeGenerator:
    """Maze generator supporting multiple algorithms.

    Generates random mazes using recursive backtracker or
    Prim's algorithm. Supports perfect mazes, the '42'
    pattern, and BFS shortest-path solving.

    Attributes:
        width: Maze width in cells.
        height: Maze height in cells.
        seed: Random seed for reproducibility.
        grid: 2D list of wall values (0-15).
        entry: Entry cell (x, y).
        exit: Exit cell (x, y).
        blocked: Cells used for the '42' pattern.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
    ) -> None:
        if width < 2 or height < 2:
            raise ValueError(
                "Width and height must be >= 2"
            )
        self.width: int = width
        self.height: int = height
        self.seed: Optional[int] = seed
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (
            width - 1, height - 1
        )
        self.grid: List[List[int]] = []
        self.blocked: Set[Tuple[int, int]] = set()
        self._reset()

    def _reset(self) -> None:
        """Reset grid to all walls closed."""
        random.seed(self.seed)
        self.grid = [
            [0xF] * self.width
            for _ in range(self.height)
        ]
        self.blocked = set()

    def _ok(self, x: int, y: int) -> bool:
        """Check if (x, y) is within maze bounds."""
        return (
            0 <= x < self.width
            and 0 <= y < self.height
        )

    def _carve(self, x: int, y: int, d:  int) -> None:
        """Remove wall between (x,y) and neighbor."""
        nx, ny = x + DX[d], y + DY[d]
        self.grid[y][x] &= ~d
        self.grid[ny][nx] &= ~OPPOSITE[d]

    def _place_42(self) -> None:
        """Place '42' pattern of fully-walled cells."""
        if self.width < 9 or self.height < 7:
            print(
                "Error: Maze too small for '42'"
            )
            return
        ox: int = (self.width - 7) // 2
        oy: int = (self.height - 5) // 2
        for dx, dy in P4:
            self.blocked.add((ox + dx, oy + dy))
        for dx, dy in P2:
            self.blocked.add(
                (ox + 4 + dx, oy + dy)
            )

    def generate(
        self,
        algorithm: str = "backtracker",
        perfect: bool = True,
        callback: Optional[AnimCb] = None,
    ) -> None:
        """Generate the maze."""
        self._reset()
        self._place_42()
        if algorithm == "prim":
            self._prim(callback)
        else:
            self._backtrack(callback)
        if not perfect:
            self._add_loops()

    def _backtrack(
        self, cb: Optional[AnimCb]
    ) -> None:
        """Iterative recursive backtracker (DFS)."""
        vis: Set[Tuple[int, int]] = set(self.blocked)
        stack: List[Tuple[int, int]] = [self.entry]
        vis.add(self.entry)
        dirs: List[int] = [N, E, S, W]
        while stack:
            x, y = stack[-1]
            nbrs: List[Tuple[int, int, int]] = []
            for d in dirs:
                nx, ny = x + DX[d], y + DY[d]
                if (
                    self._ok(nx, ny)
                    and (nx, ny) not in vis
                ):
                    nbrs.append((nx, ny, d))
            if nbrs:
                nx, ny, d = random.choice(nbrs)
                self._carve(x, y, d)
                vis.add((nx, ny))
                stack.append((nx, ny))
                if cb:
                    cb((nx, ny), vis, list(stack))
            else:
                stack.pop()
                if cb and stack:
                    cb(stack[-1], vis, list(stack))

    def _prim(
        self, cb: Optional[AnimCb]
    ) -> None:
        """Prim's algorithm — grow from entry."""
        vis: Set[Tuple[int, int]] = set(self.blocked)
        vis.add(self.entry)
        dirs: List[int] = [N, E, S, W]
        frontier: List[Tuple[int, int, int, int]] = []
        x0, y0 = self.entry
        for d in dirs:
            nx, ny = x0 + DX[d], y0 + DY[d]
            if (
                self._ok(nx, ny)
                and (nx, ny) not in vis
            ):
                frontier.append((x0, y0, nx, ny))
        while frontier:
            idx = random.randint(
                0, len(frontier) - 1
            )
            fx, fy, tx, ty = frontier.pop(idx)
            if (tx, ty) in vis:
                continue
            for d in dirs:
                if (
                    fx + DX[d] == tx
                    and fy + DY[d] == ty
                ):
                    self._carve(fx, fy, d)
                    break
            vis.add((tx, ty))
            for d in dirs:
                nx, ny = tx + DX[d], ty + DY[d]
                if (
                    self._ok(nx, ny)
                    and (nx, ny) not in vis
                ):
                    frontier.append(
                        (tx, ty, nx, ny)
                    )
            if cb:
                cb(
                    (tx, ty), vis,
                    [(tx, ty)],
                )

    def _add_loops(self) -> None:
        """Remove random walls for imperfect maze."""
        n: int = self.width * self.height // 8
        dirs: List[int] = [N, E, S, W]
        for _ in range(n):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) in self.blocked:
                continue
            d = random.choice(dirs)
            nx, ny = x + DX[d], y + DY[d]
            if (
                self._ok(nx, ny)
                and (nx, ny) not in self.blocked
            ):
                self._carve(x, y, d)

    def solve(self) -> str:
        """Find shortest path entry→exit via BFS."""
        q: List[Tuple[Tuple[int, int], str]] = [(self.entry, "")]
        vis: Set[Tuple[int, int]] = {self.entry}
        while q:
            (x, y), path = q.pop(0)
            if (x, y) == self.exit:
                return path
            for d in (N, E, S, W):
                if not (self.grid[y][x] & d):
                    nx = x + DX[d]
                    ny = y + DY[d]
                    if (
                        self._ok(nx, ny)
                        and (nx, ny) not in vis
                    ):
                        vis.add((nx, ny))
                        q.append((
                            (nx, ny),
                            path + DIR_CH[d],
                        ))
        return ""

    def to_hex(self) -> str:
        """Maze as hex string, one row per line."""
        return "\n".join(
            "".join(f"{c:X}" for c in row)
            for row in self.grid
        )

    def path_coords(
        self, path: str
    ) -> Set[Tuple[int, int]]:
        """Convert path string to coordinate set."""
        x, y = self.entry
        coords: Set[Tuple[int, int]] = {(x, y)}
        lookup: Dict[str, int] = {
            "N": N, "E": E, "S": S, "W": W,
        }
        for ch in path:
            d = lookup[ch]
            x, y = x + DX[d], y + DY[d]
            coords.add((x, y))
        return coords
