from typing import Dict

COLORS: Dict[str, str] = {
    "white": "\033[97m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
}

RST: str = "\033[0m"
BLD: str = "\033[1m"
DIM: str = "\033[2m"

COLOR_LIST: list[str] = list(COLORS.keys())

HOME: str = "\033[H"
HIDE_CURSOR: str = "\033[?25l"
SHOW_CURSOR: str = "\033[?25h"
