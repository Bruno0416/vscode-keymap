#!/usr/bin/env python3
"""Generate IntelliJ keymaps from VS Code default JSON plus optional user overrides."""
from __future__ import annotations
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources" / "vscode"
USER_SOURCE = ROOT / "sources" / "user" / "keybindings.local.json"
MAPPINGS = ROOT / "mappings" / "commands.json"
PARENT_CONFLICTS = ROOT / "mappings" / "parent-conflicts.json"
SHORTCUT_OVERRIDES = ROOT / "mappings" / "shortcuts.json"
OUTPUT = ROOT / "src" / "main" / "resources" / "keymaps"

PLATFORMS = {
    "linux": ("VS Code Complete.xml", "VS Code Complete", "$default"),
    "windows": ("VS Code Complete (Windows).xml", "VS Code Complete (Windows)", "$default"),
    "macos": ("VS Code Complete (macOS).xml", "VS Code Complete (macOS)", "Mac OS X 10.5+"),
}

KEY_NAMES = {
    "`": "BACK_QUOTE", "-": "MINUS", "=": "EQUALS", "[": "OPEN_BRACKET",
    "]": "CLOSE_BRACKET", "\\": "BACK_SLASH", ";": "SEMICOLON", "'": "QUOTE",
    ",": "COMMA", ".": "PERIOD", "/": "SLASH", "space": "SPACE",
    "pagedown": "PAGE_DOWN", "pageup": "PAGE_UP", "esc": "ESCAPE",
}
MODIFIERS = {"ctrl": "ctrl", "control": "ctrl", "shift": "shift", "alt": "alt", "cmd": "meta", "meta": "meta", "win": "meta"}


def load_jsonc(path: Path):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"(^|\s)//.*$", r"\1", text, flags=re.M)
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return json.loads(text)


def apply_user_overrides(defaults: list[dict], user: list[dict]) -> list[dict]:
    result = list(defaults)
    for rule in user:
        command = str(rule.get("command", ""))
        key = str(rule.get("key", ""))
        when = rule.get("when")
        if not command:
            continue
        if command.startswith("-"):
            target = command[1:]
            result = [r for r in result if not (
                r.get("command") == target
                and (not key or r.get("key") == key)
                and (when is None or r.get("when") == when)
            )]
            continue
        result.append(rule)
    return result


def normalize_stroke(stroke: str) -> str | None:
    bits = stroke.strip().split("+")
    if not bits:
        return None
    mods = []
    key = None
    for bit in bits:
        lower = bit.lower()
        if lower in MODIFIERS:
            mods.append(MODIFIERS[lower])
        elif bit:
            key = KEY_NAMES.get(lower, bit.upper() if len(bit) > 1 else bit.upper())
    if key is None:
        return None
    ordered = [m for m in ("ctrl", "meta", "alt", "shift") if m in mods]
    return " ".join([*ordered, key]).lower()


def normalize_keybinding(value: str):
    strokes = value.strip().split()
    if not 1 <= len(strokes) <= 2:
        return None
    normalized = [normalize_stroke(s) for s in strokes]
    if any(s is None for s in normalized):
        return None
    return normalized[0], normalized[1] if len(normalized) == 2 else None


def generate(platform: str, mappings: dict, parent_conflicts: dict, shortcut_overrides: dict, user_rules: list[dict] | None) -> tuple[int, int]:
    source = SOURCES / f"default-{platform}.json"
    if not source.exists():
        source = SOURCES / f"default-{platform}.bootstrap.json"
    defaults = load_jsonc(source)
    effective = apply_user_overrides(defaults, user_rules or [])

    output_name, display_name, parent = PLATFORMS[platform]
    root = ET.Element("keymap", {"version": "1", "name": display_name, "parent": parent})
    action_nodes: dict[str, ET.Element] = {}

    # Empty action nodes intentionally clear shortcuts inherited from the parent keymap.
    # This is required for strict VS Code bindings such as Ctrl+D, which IntelliJ
    # otherwise also inherits for EditorDuplicate and several context actions.
    for action_id in parent_conflicts.get(platform, []):
        action_nodes[action_id] = ET.SubElement(root, "action", {"id": action_id})

    emitted = set()
    skipped = 0

    for binding in effective:
        command = binding.get("command")
        key = binding.get("key")
        mapping = mappings.get(command)
        if not mapping or mapping.get("status") == "unsupported" or not key:
            skipped += 1
            continue
        normalized = normalize_keybinding(key)
        if normalized is None:
            skipped += 1
            continue
        action_id = mapping["intellij_action"]
        first, second = normalized
        signature = (action_id, first, second)
        if signature in emitted:
            continue
        emitted.add(signature)
        action = action_nodes.get(action_id)
        if action is None:
            action = ET.SubElement(root, "action", {"id": action_id})
            action_nodes[action_id] = action
        attrs = {"first-keystroke": first}
        if second:
            attrs["second-keystroke"] = second
        ET.SubElement(action, "keyboard-shortcut", attrs)

    # Curated workflow bindings intentionally override/add behavior that is not a direct
    # stock VS Code command mapping (for example hiding IntelliJ Terminal with Ctrl+Shift+W).
    for binding in shortcut_overrides.get(platform, []):
        action_id = binding.get("action")
        key = binding.get("key")
        normalized = normalize_keybinding(key or "")
        if not action_id or normalized is None:
            continue
        first, second = normalized
        signature = (action_id, first, second)
        if signature in emitted:
            continue
        emitted.add(signature)
        action = action_nodes.get(action_id)
        if action is None:
            action = ET.SubElement(root, "action", {"id": action_id})
            action_nodes[action_id] = action
        attrs = {"first-keystroke": first}
        if second:
            attrs["second-keystroke"] = second
        ET.SubElement(action, "keyboard-shortcut", attrs)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    tree.write(OUTPUT / output_name, encoding="utf-8", xml_declaration=True)
    return len(emitted), skipped


def main() -> None:
    mappings = json.loads(MAPPINGS.read_text(encoding="utf-8"))
    parent_conflicts = json.loads(PARENT_CONFLICTS.read_text(encoding="utf-8"))
    shortcut_overrides = json.loads(SHORTCUT_OVERRIDES.read_text(encoding="utf-8"))
    user_rules = load_jsonc(USER_SOURCE) if USER_SOURCE.exists() else None
    for platform in PLATFORMS:
        emitted, skipped = generate(platform, mappings, parent_conflicts, shortcut_overrides, user_rules)
        print(f"{platform}: emitted {emitted} mapped shortcuts; skipped {skipped} unmapped/context-only bindings")
    if user_rules is not None:
        print(f"Applied optional user overrides from {USER_SOURCE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
