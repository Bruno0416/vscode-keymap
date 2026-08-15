#!/usr/bin/env python3
"""Import local VS Code/VSCodium user keybindings for optional exact-personal generation."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "sources" / "user" / "keybindings.local.json"

CANDIDATES = [
    Path.home() / ".config/Code/User/keybindings.json",
    Path.home() / ".config/Code - Insiders/User/keybindings.json",
    Path.home() / ".config/Code - OSS/User/keybindings.json",
    Path.home() / ".config/VSCodium/User/keybindings.json",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path)
    args = parser.parse_args()

    source = args.path.expanduser() if args.path else next((p for p in CANDIDATES if p.is_file()), None)
    if source is None or not source.is_file():
        print("No VS Code user keybindings.json found.", file=sys.stderr)
        print("Pass it explicitly: ./scripts/import_vscode_keybindings.py /path/to/keybindings.json", file=sys.stderr)
        return 1

    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, DEST)
    print(f"Imported {source} -> {DEST.relative_to(ROOT)}")
    print("Run ./scripts/generate_keymaps.py to apply the overrides.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
