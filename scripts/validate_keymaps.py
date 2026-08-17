#!/usr/bin/env python3
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
KEYMAP = ROOT / "src/main/resources/keymaps/VS Code Complete.xml"
PLUGIN_XML = ROOT / "src/main/resources/META-INF/plugin.xml"
REQUIRED = {
    ("dev.bruno0416.vscodekeymap.ToggleTerminal", "ctrl j", ""),
    ("dev.bruno0416.vscodekeymap.ToggleTerminal", "ctrl back_quote", ""),
    ("Terminal.NewTab", "ctrl shift back_quote", ""),
    ("dev.bruno0416.vscodekeymap.HideTerminal", "ctrl shift w", ""),
    ("ActivateProjectToolWindow", "ctrl b", ""),
    ("SelectNextOccurrence", "ctrl d", ""),
    ("GotoFile", "ctrl p", ""),
    ("GotoAction", "ctrl shift p", ""),
    ("GotoAction", "f1", ""),
    ("FindInPath", "ctrl shift f", ""),
    ("ReplaceInPath", "ctrl shift h", ""),
    ("MoveLineUp", "alt up", ""),
    ("MoveLineDown", "alt down", ""),
    ("dev.bruno0416.vscodekeymap.OpenKeymapSettings", "ctrl k", "ctrl s"),
}
CLEARED_PARENT_ACTIONS = {
    "InsertLiveTemplate",
    "EditorDuplicate",
    "CompareTwoFiles",
    "Diff.ShowDiff",
    "Compare.SameVersion",
    "SendEOF",
}

root = ET.parse(KEYMAP).getroot()
seen = set()
actions = {}
for action in root.findall("action"):
    action_id = action.get("id", "")
    actions[action_id] = action
    for shortcut in action.findall("keyboard-shortcut"):
        seen.add((
            action_id,
            shortcut.get("first-keystroke", "").lower(),
            (shortcut.get("second-keystroke") or "").lower(),
        ))

missing = REQUIRED - seen
if missing:
    for item in sorted(missing):
        print(f"ERROR: missing required Linux mapping {item}")
    sys.exit(1)

for action_id in sorted(CLEARED_PARENT_ACTIONS):
    action = actions.get(action_id)
    if action is None or action.findall("keyboard-shortcut"):
        print(f"ERROR: inherited conflict not cleared: {action_id}")
        sys.exit(1)

plugin = ET.parse(PLUGIN_XML).getroot()
extensions = plugin.find("extensions")
if extensions is None:
    print("ERROR: plugin extensions missing")
    sys.exit(1)

service = extensions.find("applicationService[@serviceImplementation='dev.bruno0416.vscodekeymap.keymap.VsCodeShortcutDispatcher']")
startup = extensions.find("postStartupActivity[@implementation='dev.bruno0416.vscodekeymap.startup.ShortcutStartupActivity']")
if service is None or startup is None:
    print("ERROR: terminal shortcut dispatcher is not registered")
    sys.exit(1)

action_ids = {a.get("id") for a in plugin.findall("./actions/action")}
required_actions = {
    "dev.bruno0416.vscodekeymap.ToggleTerminal",
    "dev.bruno0416.vscodekeymap.HideTerminal",
    "dev.bruno0416.vscodekeymap.OpenKeymapSettings",
}
if not required_actions.issubset(action_ids):
    print(f"ERROR: plugin actions missing: {sorted(required_actions - action_ids)}")
    sys.exit(1)

print(
    f"Keymap validation passed: {len(seen)} Linux shortcuts; "
    "Terminal toggle/new-tab/close workflow, Ctrl+D cleanup, and Alt+Up/Down move-line workflow present"
)
