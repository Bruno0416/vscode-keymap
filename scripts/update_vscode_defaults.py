#!/usr/bin/env python3
"""Download Microsoft's generated VS Code default keybinding snapshots."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "sources" / "vscode"
UPSTREAM = SOURCE_DIR / "upstream.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--best-effort", action="store_true", help="keep bootstrap snapshots if download fails")
    args = parser.parse_args()

    meta = json.loads(UPSTREAM.read_text())
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    failures = []

    for platform, url in meta["urls"].items():
        destination = SOURCE_DIR / f"default-{platform}.json"
        bootstrap = SOURCE_DIR / f"default-{platform}.bootstrap.json"
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "vscode-keymap-intellij/0.2.1"})
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
            parsed = json.loads(data)
            if not isinstance(parsed, list) or not parsed:
                raise ValueError("upstream document is not a non-empty JSON array")
            destination.write_bytes(data)
            print(f"Updated {platform}: {len(parsed)} VS Code bindings")
        except Exception as exc:
            failures.append((platform, exc))
            if bootstrap.exists():
                shutil.copy2(bootstrap, destination)
                print(f"WARNING: {platform}: upstream download failed; using bundled bootstrap snapshot: {exc}")
            else:
                print(f"ERROR: {platform}: {exc}", file=sys.stderr)

    if failures and not args.best_effort:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
