#!/usr/bin/env python3

import os
import random
import sys
from typing import Dict, Optional, Set, Tuple

from mazegen import MazeGenerator

from constants import COLOR_LIST
from config import parse_config, validate
from renderer import render
from file_io import save_output
from animation import animate


def main() -> None:
    """Main entry point: parse, generate, display."""
    if len(sys.argv) != 2:
        print(
            "Usage: python3 a_maze_ing.py config.txt"
        )
        sys.exit(1)

    cfg: Dict[str, str] = parse_config(sys.argv[1])
    validate(cfg)

    try:
        w: int = int(cfg["WIDTH"])
        h: int = int(cfg["HEIGHT"])
        ex, ey = map(int, cfg["ENTRY"].split(","))
        xx, xy = map(int, cfg["EXIT"].split(","))
        out: str = cfg["OUTPUT_FILE"]
        perf_str: str = cfg["PERFECT"].lower()
        if perf_str not in ("true", "false"):
            print(
                "Error: PERFECT must be"
                " 'true' or 'false'"
            )
            sys.exit(1)
        perfect: bool = perf_str == "true"
        seed: int = int(cfg.get("SEED", "42"))
        algo: str = cfg.get(
            "ALGORITHM", "backtracker"
        )
    except ValueError as e:
        print(f"Error: Invalid config - {e}")
        sys.exit(1)

    try:
        m: MazeGenerator = MazeGenerator(w, h, seed)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    m.entry = (ex, ey)
    m.exit = (xx, xy)

    if not (0 <= ex < w and 0 <= ey < h):
        print("Error: ENTRY out of bounds")
        sys.exit(1)
    if not (0 <= xx < w and 0 <= xy < h):
        print("Error: EXIT out of bounds")
        sys.exit(1)
    if m.entry == m.exit:
        print("Error: ENTRY and EXIT must differ")
        sys.exit(1)

    m.generate(algorithm=algo, perfect=perfect)

    if m.entry in m.blocked:
        print("Error: ENTRY overlaps 42 pattern")
        sys.exit(1)
    if m.exit in m.blocked:
        print("Error: EXIT overlaps 42 pattern")
        sys.exit(1)

    save_output(m, out)
    print(f"Maze saved to {out}")

    show: bool = False
    wi: int = 0
    pi: int = 5

    while True:
        os.system("clear")
        ps: str = m.solve()
        pc: Optional[
            Set[Tuple[int, int]]
        ] = m.path_coords(ps) if show else None
        print(render(m, pc, COLOR_LIST[wi], COLOR_LIST[pi]))
        st: str = "ON" if show else "OFF"
        print(
            f"\n{w}x{h} | {algo} | "
            f"path:{st} | "
            f"wall:{COLOR_LIST[wi]} | 42:{COLOR_LIST[pi]}"
        )
        print(
            "[r]egenerate [p]ath [c]olor "
            "[t]42-color [a]nimate "
            "[s]witch-algo [q]uit"
        )
        try:
            ch: str = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if ch == "q":
            break
        elif ch == "r":
            m.seed = random.randint(0, 99999)
            m.generate(algo, perfect)
            save_output(m, out)
        elif ch == "p":
            show = not show
        elif ch == "c":
            wi = (wi + 1) % len(COLOR_LIST)
        elif ch == "t":
            pi = (pi + 1) % len(COLOR_LIST)
        elif ch == "a":
            m.seed = random.randint(0, 99999)
            animate(
                m, algo, perfect,
                COLOR_LIST[wi], COLOR_LIST[pi],
            )
            save_output(m, out)
        elif ch == "s":
            algo = (
                "prim"
                if algo == "backtracker"
                else "backtracker"
            )
            m.seed = random.randint(0, 99999)
            m.generate(algo, perfect)
            save_output(m, out)


if __name__ == "__main__":
    main()
