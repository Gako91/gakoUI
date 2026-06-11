from pathlib import Path

ICONS_DIR = Path(__file__).resolve().parent / "icons"


def icon_path(name: str) -> str:
    """Return the absolute path to a bundled icon, or '' if name is empty."""
    if not name:
        return ""
    return str(ICONS_DIR / name)
