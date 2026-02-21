from mazegen import MazeGenerator


def save_output(
    m: MazeGenerator, out: str
) -> None:
    path_str: str = m.solve()
    with open(out, "w") as f:
        f.write(m.to_hex() + "\n")
        f.write("\n")
        ex, ey = m.entry
        f.write(f"{ex},{ey}\n")
        xx, xy = m.exit
        f.write(f"{xx},{xy}\n")
        f.write(path_str + "\n")
