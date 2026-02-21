import os
import sys
import time

from mazegen import MazeGenerator, N, E, S, W, DX, DY
from constants import HOME, HIDE_CURSOR, SHOW_CURSOR
from renderer import render


def animate(m: MazeGenerator, algo: str, perfect: bool,
            wc: str = "white", pc: str = "cyan") -> None:

    total = m.width * m.height - len(m.blocked)
    steps = 0
    frame_every = max(1, total // 40)

    def cb(cell, visited, stack):
        nonlocal steps
        steps += 1
        if steps % frame_every:
            return

        sys.stdout.write(
            HOME +
            render(m, head=cell, visited=visited,
                   stack=set(stack), wc=wc, pc=pc) +
            "\n"
        )
        sys.stdout.flush()
        time.sleep(0.06)

    sys.stdout.write(HIDE_CURSOR)
    os.system("clear")

    m.generate(algorithm=algo, perfect=perfect, callback=cb)

    sys.stdout.write(HOME + render(m, wc=wc, pc=pc) + "\n")
    sys.stdout.flush()
    time.sleep(0.8)

    directions = [(N, "N"), (E, "E"), (S, "S"), (W, "W")]
    queue = [(m.entry, "")]
    visited = {m.entry}
    order = [m.entry]
    solved = ""

    while queue:
        (x, y), path = queue.pop(0)
        if (x, y) == m.exit:
            solved = path
            break

        for bit, label in directions:
            if m.grid[y][x] & bit:
                continue
            nx, ny = x + DX[bit], y + DY[bit]
            if m._ok(nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                order.append((nx, ny))
                queue.append(((nx, ny), path + label))

    shown = set()
    chunk = max(1, len(order) // 30)

    for i in range(0, len(order), chunk):
        batch = order[i:i + chunk]
        shown.update(batch)
        last = batch[-1]

        sys.stdout.write(
            HOME +
            render(m, head=last, visited=shown,
                   wc=wc, pc=pc) +
            "\n"
        )
        sys.stdout.flush()
        time.sleep(0.03)

    if solved:
        coords = {m.entry}
        x, y = m.entry
        lookup = {"N": N, "E": E, "S": S, "W": W}

        for ch in solved:
            bit = lookup[ch]
            x, y = x + DX[bit], y + DY[bit]
            coords.add((x, y))

            sys.stdout.write(
                HOME +
                render(m, path=coords, head=(x, y),
                       wc=wc, pc=pc) +
                "\n"
            )
            sys.stdout.flush()
            time.sleep(0.03)

    sys.stdout.write(
        HOME +
        render(m, path=m.path_coords(solved),
               wc=wc, pc=pc) +
        "\n\n"
    )
    sys.stdout.flush()
    time.sleep(1.2)

    sys.stdout.write(SHOW_CURSOR)
