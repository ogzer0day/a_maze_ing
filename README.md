*This project has been created as part of the 42 curriculum by mdamouh, mzougari.*

# A-Maze-ing 🏰

A Python maze generator with ASCII visualization, interactive controls, and real-time animation.

---

## Description

**Goal**: Build a maze generator that creates random perfect mazes, solves them, and visualizes both the generation process and solution interactively in the terminal.

**Overview**:
A-Maze-ing is a full-featured maze generation system featuring:
- **Two generation algorithms**: Recursive Backtracker (DFS) and Prim's frontier-based algorithm
- **Perfect maze guarantee**: Exactly one path between any two cells
- **Interactive terminal UI**: Real-time ASCII rendering with 7 ANSI colors
- **Animation system**: Watch the maze being generated and solved step-by-step
- **BFS solver**: Finds the shortest path from entry to exit
- **Easter egg**: Embeds the "42" digit pattern in every maze
- **Reusable package**: The `mazegen` module can be imported independently into other projects

The project demonstrates clean Python architecture with type hints, modular design, and a separation between the core algorithm engine and the display/interaction layer.

---

## Instructions

### Requirements
- Python 3.10+
- `flake8` and `mypy` for code validation (optional)

### Installation & Execution

```bash
# Install the mazegen package (one-time setup)
make install

# Run with the default config.txt
make run

# Or run directly with a custom config
python3 a_maze_ing.py config.txt

# Other commands
make clean      # Remove cache files and build artifacts
make lint       # Check code style (flake8 + mypy)
make build      # Build wheel and source distribution
```

### Quick Start

1. Edit `config.txt` to set maze dimensions, entry/exit points, and algorithm choice
2. Run `make run` to generate and display the maze
3. Use interactive commands to regenerate, view solutions, change colors, and animate

---

## Configuration File Format

The `config.txt` file uses a simple `KEY=VALUE` format. Lines starting with `#` are comments.

```ini
# A-Maze-ing Configuration
WIDTH=20              # Maze width in cells (minimum 2)
HEIGHT=10             # Maze height in cells (minimum 2)
ENTRY=0,0             # Entry point coordinates (x,y)
EXIT=19,9             # Exit point coordinates (x,y)
OUTPUT_FILE=maze.txt  # Output file path (hex-encoded maze)
PERFECT=true          # true = perfect maze (one path only), false = allows loops
SEED=42               # Random seed (same seed produces same maze)
ALGORITHM=backtracker # "backtracker" or "prim"
```

**Required keys**: `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`

**Optional keys**: `SEED` (default: 42), `ALGORITHM` (default: backtracker)

---

## Interactive Controls

When the program runs, the maze displays with a command menu:

| Key | Action |
|-----|--------|
| `r` | **Regenerate** — new random seed, create new maze |
| `p` | **Path** — toggle showing/hiding the shortest path |
| `c` | **Color walls** — cycle through 7 ANSI colors for maze walls |
| `t` | **Color 42** — cycle colors for the "42" pattern |
| `a` | **Animate** — watch generation + solving in real-time |
| `s` | **Switch algorithm** — toggle between backtracker ↔ prim |
| `q` | **Quit** — exit the program |

---

## Maze Generation Algorithms

### Algorithm Choice: Recursive Backtracker (Primary) + Prim's (Bonus)

#### Recursive Backtracker (DFS) — Default

**What it does**:
```
1. Start at entry cell. Mark visited. Use a stack.
2. While stack not empty:
   - Look at the top cell (current position)
   - Find all unvisited neighbors
   - If unvisited neighbors exist:
     → Pick one randomly
     → Carve wall between current and neighbor
     → Mark neighbor visited
     → Push neighbor onto stack
   - Else: Backtrack (pop stack)
```

**Why this algorithm**:
- **Simple to understand**: Plain DFS with a stack—easy to explain and debug
- **Efficient**: O(cells) time, visits each cell exactly once
- **Perfect maze guarantee**: Creates exactly one path between any two cells
- **Aesthetic**: Produces characteristic long winding corridors
- **Easy to animate**: The stack naturally shows backtracking progress

**Visual style**: Long, twisting passages with natural-looking dead ends.

#### Prim's Algorithm — Bonus Feature

**What it does**:
```
1. Start at entry cell. Mark visited.
2. Add all unvisited neighbors to a "frontier" list.
3. While frontier not empty:
   - Pick a random cell from frontier
   - If it's unvisited:
     → Carve wall connecting it to a visited neighbor
     → Mark it visited
     → Add all its unvisited neighbors to frontier
```

**Why included as bonus**:
- **Different aesthetic**: Creates more evenly distributed passages
- **Educational value**: Shows an alternative approach (frontier-based vs. stack-based)
- **Switchable at runtime**: User can press `[s]` to toggle algorithms

**Visual style**: Branching patterns, more organic maze distribution.

---

## How the Maze Works Internally

### Grid Representation

The maze is stored as a 2D grid where each cell is a single integer (0-15):

```
Bit position → Wall direction
0 (value 1)  = North wall (top)
1 (value 2)  = East wall (right)
2 (value 4)  = South wall (bottom)
3 (value 8)  = West wall (left)
```

Example: 
- `0xF` (15 = `1111` binary) = all 4 walls present (closed cell)
- `0x0` (0 = `0000` binary) = no walls (open cell)
- `0x5` (5 = `0101` binary) = North + South walls only

### Wall Carving

When removing a wall between two cells:
```python
# If cell A is west of cell B:
A &= ~E  # Clear East bit in A
B &= ~W  # Clear West bit in B
```

Both cells must agree there's no wall between them for a proper passage.

### Hex Output Format

Each cell (0-15) encodes as one hex digit (0-F). A 20×10 maze = 20 characters per line × 10 lines.

---

## Output File Format

The `maze.txt` output contains:

```
BD13953953917953913B    ← Line 1-N: Hex-encoded grid (one row per line)
A96C6BC2D2EC543AAAAA
... (more rows)

0,0                     ← Entry coordinates
19,9                    ← Exit coordinates
SSENENESENEESENE...     ← Solution path (N/E/S/W moves)
```

Each hex digit represents one cell's wall configuration.

---

## Solving Algorithm: BFS

The shortest path is found using **Breadth-First Search (BFS)**:

```
1. Start at entry. Add to queue.
2. Process queue (FIFO):
   - Take first cell
   - If it's the exit: done! Return path.
   - For each direction (N, E, S, W):
     → If no wall AND neighbor not visited:
       → Add to queue with path
3. Repeat until exit found
```

**Why BFS**: Explores cells layer-by-layer. First time reaching the exit = guaranteed shortest path.

Result: A string like `"EESSWWSSEENNN"` (each char = one step).

---

## The "42" Pattern

Every maze embeds pixel art of the digits **4** and **2** in the center. These are "blocked" cells that keep all 4 walls and appear as `###` in the display. The generation algorithm treats them as obstacles and carves around them—they remain visible in every maze as an homage to 42 School.

Defined as 3×5 pixel grids in `mazegen/directions.py`.

---

## Project Structure

```
amazeing/
├── a_maze_ing.py          ← Main entry point (orchestrates everything)
├── config.py              ← Configuration file parsing and validation
├── constants.py           ← ANSI color codes for terminal colors
├── renderer.py            ← ASCII maze rendering engine
├── file_io.py             ← Saves maze to output file
├── animation.py           ← Maze generation + solving animation (bonus)
├── config.txt             ← Default configuration
├── maze.txt               ← Generated output (hex format)
├── Makefile               ← Build automation (install, run, lint, build)
├── pyproject.toml         ← Package metadata for mazegen
├── README.md              ← This file
└── mazegen/               ← **REUSABLE PACKAGE** (can be installed and imported)
    ├── __init__.py        ← Package entry point
    ├── directions.py      ← Constants (wall bits, pixels, direction mappings)
    └── generator.py       ← MazeGenerator class (the core algorithm engine)
```

### File Descriptions

| File | Purpose |
|------|---------|
| `a_maze_ing.py` | Entry point: reads config, creates maze, runs interactive loop |
| `config.py` | Parses `KEY=VALUE` config files, validates required fields |
| `constants.py` | ANSI escape codes for terminal colors and cursor control |
| `renderer.py` | Converts maze grid to ASCII art with wall drawing and colors |
| `file_io.py` | Saves maze to hex format with entry, exit, solution path |
| `animation.py` | Real-time animation: generation visualization + BFS solving |
| `mazegen/` | Standalone reusable package with core algorithm logic |


---

## Reusable Package: `mazegen`

The `mazegen/` module is designed to be **completely independent** from the display layer:

```python
from mazegen import MazeGenerator

# Create and generate a maze
maze = MazeGenerator(width=20, height=15, seed=42)
maze.generate(algorithm="backtracker", perfect=True)

# Solve it
path = maze.solve()  # Returns "EESSWN..." string

# Export
hex_grid = maze.to_hex()  # Hex-encoded grid
coords = maze.path_coords(path)  # Set of (x, y) on solution
```

**This can be used in any Python project** without needing the terminal display code. Install via pip after building:

```bash
pip install ./dist/mazegen-1.0.0-py3-none-any.whl
```

Then import from anywhere:
```python
from mazegen import MazeGenerator, N, E, S, W
```

---

## Team & Project Management

### Team Composition
- **mdamouh**: Core engine, algorithm implementation, package architecture
- **mzougari**: Display, animation, configuration, error handling

### Planning & Evolution

**Initial Plan**:
- Minimal: Single algorithm, basic ASCII display, essential files only

**Evolution**:
1. **Phase 1** ✅ — Core backtracker algorithm + hex output
2. **Phase 2** ✅ — Terminal rendering with ANSI colors + interactive menu
3. **Phase 3** ✅ — BFS solver + animation system (bonus)
4. **Phase 4** ✅ — Added Prim's algorithm (bonus) + algorithm switching
5. **Phase 5** ✅ — Refactored into reusable `mazegen` package
6. **Phase 6** ✅ — Code cleanup: full type hints, docstrings, linting

**Key pivot**: Decided to make `mazegen` a standalone package early—this enabled better testing, code reuse, and separation of concerns.

### What Worked Well

✅ **Modular architecture**: Separate algorithm engine from display logic  
✅ **Type hints throughout**: Caught errors early, enabled better IDE support  
✅ **Callback-based animation**: Clean way to pass generation progress to display  
✅ **Prim's algorithm bonus**: Different visual style, educational value  
✅ **Reusable package design**: Can be installed/imported independently  
✅ **Interactive menu**: Intuitive and responsive controls  
✅ **Clean code standards**: 0 flake8/mypy errors

### What Could Be Improved

⚠️ **Performance for large mazes**: No optimization for 100×100+ grids (not needed for 42 requirements)  
⚠️ **Animation speed control**: Currently hardcoded; could be configurable in config.txt  
⚠️ **Unit tests**: No formal test suite (validation done manually)  
⚠️ **Documentation**: Deep WALKTHROUGH.md but could use quick-reference cheatsheet  
⚠️ **Error recovery**: Could retry invalid config instead of immediate exit

### Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Primary language |
| **flake8** | Code style checker (PEP 8 compliance) |
| **mypy** | Static type checker (ensures type hint correctness) |
| **Make** | Build automation (install, run, clean, lint, build) |
| **pip** | Package installation and distribution |
| **ANSI escape codes** | Terminal colors and cursor control |
| **Git** | Version control |
| **VS Code** | Development environment |

---

## Resources & References

### Documentation
- **[Python Maze Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)** — Overview of DFS, Kruskal's, Prim's
- **[Recursive Backtracking](https://en.wikipedia.org/wiki/Depth-first_search)** — DFS algorithm foundations
- **[Prim's Algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm)** — Minimum spanning tree / maze generation
- **[Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search)** — Shortest path finding
- **[ANSI Escape Codes](https://en.wikipedia.org/wiki/ANSI_escape_code)** — Terminal text formatting

### Tutorials
- "The Coding Train" — Maze generation videos (Processing language, but algorithm concepts transfer)
- PEP 257 — Python Docstring Conventions
- PEP 8 — Python Style Guide

### AI Usage

**Where AI was used**:

| Task | AI Contribution |
|------|-----------------|
| **Algorithm research** | Clarified differences between backtracker, Kruskal's, and Prim's approaches |
| **Type hints design** | Helped structure proper type annotations (`AnimCb` callback typing) |
| **Error handling** | Suggested appropriate exception handling patterns |
| **Code review** | Identified edge cases (entry/exit in bounds, overlap with "42" pattern) |
| **Documentation** | Generated structure for README and code walkthroughs |
| **Testing suggestions** | Proposed test cases and validation scenarios |

**What was NOT AI-generated**:
- Core algorithm implementations (backtracker, Prim's, BFS) — written from scratch
- All ASCII rendering logic — hand-coded
- Animation callback system — custom-designed
- Interactive menu system — custom-built
