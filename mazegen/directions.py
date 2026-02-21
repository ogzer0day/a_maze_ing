"""Wall direction constants and pixel font data."""

from typing import Callable, Dict, List, Set, Tuple

AnimCb = Callable[
    [Tuple[int, int], Set[Tuple[int, int]], List[Tuple[int, int]]],
    None,
]

N: int = 1
E: int = 2
S: int = 4
W: int = 8

OPPOSITE: Dict[int, int] = {N: S, S: N, E: W, W: E}
DX: Dict[int, int] = {N: 0, E: 1, S: 0, W: -1}
DY: Dict[int, int] = {N: -1, E: 0, S: 1, W: 0}
DIR_CH: Dict[int, str] = {N: "N", E: "E", S: "S", W: "W"}

P4: List[Tuple[int, int]] = [
    (0, 0), (2, 0),
    (0, 1), (2, 1),
    (0, 2), (1, 2), (2, 2),
    (2, 3),
    (2, 4),
]
P2: List[Tuple[int, int]] = [
    (0, 0), (1, 0), (2, 0),
    (2, 1),
    (0, 2), (1, 2), (2, 2),
    (0, 3),
    (0, 4), (1, 4), (2, 4),
]
