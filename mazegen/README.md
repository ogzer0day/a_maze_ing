# mazegen — Reusable Maze Generator

A Python package for generating random perfect mazes, solving them via BFS, and exporting to hex format.

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or from source:

```bash
pip install .
```

## Quick Start

```python
from mazegen import MazeGenerator

maze = MazeGenerator(20, 10, seed=42)
maze.generate()
path = maze.solve()
print(maze.to_hex())
print("Solution:", path)
```

## Custom Parameters

### Constructor

```python
MazeGenerator(width, height, seed=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Maze width in cells (minimum 2) |
| `height` | `int` | Maze height in cells (minimum 2) |
| `seed` | `int \| None` | Random seed for reproducibility |

### Generation

```python
maze.generate(algorithm="backtracker", perfect=True, callback=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `algorithm` | `str` | `"backtracker"` (DFS) or `"prim"` (frontier-based) |
| `perfect` | `bool` | `True` = one path only, `False` = allows loops |
| `callback` | `Callable \| None` | Called at each step with `(cell, visited, stack)` |

### Entry and Exit

```python
maze.entry = (0, 0)         # Default: top-left
maze.exit = (19, 9)         # Default: bottom-right
```

Set these before or after calling `generate()`.

## Accessing the Maze Structure

### The Grid

```python
maze.grid  # 2D list of integers (0-15)
```

Each cell is a 4-bit integer where each bit represents a wall:

| Bit | Value | Direction |
|-----|-------|-----------|
| 0 | 1 | North (top) |
| 1 | 2 | East (right) |
| 2 | 4 | South (bottom) |
| 3 | 8 | West (left) |

Example: `0xF` (15) = all walls, `0x0` = no walls, `0x5` = North + South only.

```python
cell = maze.grid[y][x]
has_north_wall = bool(cell & 1)
has_east_wall = bool(cell & 2)
```

### Blocked Cells (42 Pattern)

```python
maze.blocked  # Set of (x, y) tuples forming the "42" pattern
```

### Direction Constants

```python
from mazegen import N, E, S, W, DX, DY, OPPOSITE, DIR_CH

N  # 1 (North)
E  # 2 (East)
S  # 4 (South)
W  # 8 (West)

DX[E]       # 1  (East moves x+1)
DY[S]       # 1  (South moves y+1)
OPPOSITE[N] # 4  (opposite of North is South)
DIR_CH[E]   # "E" (direction to character)
```

## Solving

```python
path = maze.solve()  # Returns "EESSWN..." (shortest path, BFS)
```

The result is a string of `N`/`E`/`S`/`W` characters, each representing one step.

### Convert Path to Coordinates

```python
coords = maze.path_coords(path)  # Set of (x, y) on the solution path
```

## Export

```python
hex_str = maze.to_hex()  # Hex-encoded grid, one row per line
```

Each cell (0-15) becomes one hex digit (0-F). A 20×10 maze = 20 chars × 10 lines.

## Full Example

```python
from mazegen import MazeGenerator

# Create a 30x15 maze with a fixed seed
maze = MazeGenerator(30, 15, seed=123)

# Set custom entry and exit
maze.entry = (0, 0)
maze.exit = (29, 14)

# Generate using Prim's algorithm
maze.generate(algorithm="prim", perfect=True)

# Solve and get the shortest path
path = maze.solve()
print(f"Path length: {len(path)} steps")
print(f"Solution: {path}")

# Get path as coordinates
coords = maze.path_coords(path)
print(f"Path passes through {len(coords)} cells")

# Access the grid directly
for y in range(maze.height):
    for x in range(maze.width):
        cell = maze.grid[y][x]
        if (x, y) in maze.blocked:
            print("##", end="")
        else:
            print(f"{cell:X} ", end="")
    print()

# Export as hex
print(maze.to_hex())
```
