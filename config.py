import sys
from typing import Dict


def parse_config(path: str) -> Dict[str, str]:
    """Parse KEY=VALUE configuration file.

    Args:
        path: Path to the config file.

    Returns:
        Dictionary of config key-value pairs.
    """
    cfg: Dict[str, str] = {}
    try:
        with open(path) as f:
            for ln in f:
                ln = ln.strip()
                if (
                    ln
                    and not ln.startswith("#")
                    and "=" in ln
                ):
                    k, v = ln.split("=", 1)
                    k, v = k.strip(), v.strip()
                    if not v:
                        print(
                            f"Error: Empty value for"
                            f" '{k}' in config"
                        )
                        sys.exit(1)
                    cfg[k] = v
    except FileNotFoundError:
        print(f"Error: '{path}' not found")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Cannot read '{path}'")
        sys.exit(1)
    return cfg


def validate(cfg: Dict[str, str]) -> None:
    """Validate that all required keys exist.

    Args:
        cfg: Configuration dictionary.
    """
    keys = (
        "WIDTH", "HEIGHT", "ENTRY",
        "EXIT", "OUTPUT_FILE", "PERFECT",
    )
    for k in keys:
        if k not in cfg:
            print(f"Error: Missing '{k}' in config")
            sys.exit(1)
