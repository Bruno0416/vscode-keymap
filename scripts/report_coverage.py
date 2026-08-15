#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "sources/vscode/default-linux.json"
if not source.exists():
    source = ROOT / "sources/vscode/default-linux.bootstrap.json"
bindings = json.loads(source.read_text())
mappings = json.loads((ROOT / "mappings/commands.json").read_text())
commands = {b.get("command") for b in bindings if b.get("command")}
mapped = commands & mappings.keys()
print("VS Code Linux source")
print(f"  bindings          : {len(bindings)}")
print(f"  unique commands   : {len(commands)}")
print(f"  mapped commands   : {len(mapped)}")
print(f"  pending commands  : {len(commands - mappings.keys())}")
print(f"  mapping catalog   : {len(mappings)}")
