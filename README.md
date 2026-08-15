# VS Code Complete Keymap for IntelliJ

A VS Code-first keymap for IntelliJ-based IDEs. Starting with 0.2.0, shortcuts are generated from Microsoft's VS Code default keyboard shortcut JSON instead of from JetBrains' VSCode keymap.

## Why

The goal is to preserve VS Code muscle memory while executing the closest native IntelliJ action. Shortcuts are not invented in the mapping layer: VS Code defines the key, and this plugin translates the command semantics.

## Linux examples

| Shortcut | VS Code intent | IntelliJ equivalent |
|---|---|---|
| `Ctrl+J` | Toggle bottom panel | Terminal tool window |
| `Ctrl+B` | Toggle primary sidebar | Project tool window |
| `Ctrl+D` | Add selection to next match | Select Next Occurrence |
| `Ctrl+\`` | Toggle terminal | Terminal tool window |
| `Ctrl+Shift+\`` | New terminal | New Terminal tab |
| `Ctrl+Shift+W` | Curated close-terminal shortcut | Hide Terminal |
| `Ctrl+P` | Quick Open | Go to File |
| `Ctrl+Shift+P` / `F1` | Command Palette | Find Action |
| `Ctrl+Shift+F` | Find in Files | Find in Files |
| `F2` | Rename Symbol | Rename |
| `Ctrl+.` | Quick Fix | Show Intention Actions |

## Build

```bash
./scripts/build.sh
```

The installable ZIP is created under `build/distributions/`.

## Refresh VS Code defaults

```bash
python3 scripts/update_vscode_defaults.py
```

This downloads the generated default keybinding snapshots published by Microsoft for Linux, Windows, and macOS.

## Use your own VS Code profile

Optionally import your local overrides:

```bash
python3 scripts/import_vscode_keybindings.py
python3 scripts/generate_keymaps.py
```

Typical Linux locations for Code, Code - OSS and VSCodium are detected automatically. The imported local file is Git-ignored.

## Project layout

```text
sources/vscode/          upstream/default VS Code JSON
sources/user/            optional local overrides (Git-ignored)
mappings/commands.json   VS Code command -> IntelliJ Action ID
mappings/shortcuts.json  curated workflow-only bindings
scripts/                  update/resolve/generate/validate tools
src/main/resources/keymaps/ generated IntelliJ keymaps
src/main/kotlin/          minimal IntelliJ adapters only
```

## Kotlin-first runtime

Starting with 0.2.4, every runtime adapter is written in Kotlin. The project uses Kotlin/JVM 2.1.20 with a Java 21 toolchain, matching the rest of the IntelliJ plugin set while keeping the generated keymaps and Python tooling unchanged.

## Current limitation

VS Code `when` clauses do not map directly to IntelliJ keymap XML. The project therefore maps safe command-level equivalents first and will add adapter actions only where context handling is genuinely necessary.

## License

See `LICENSE`.


### Gradle instrumentation workaround

The project intentionally disables Gradle Configuration Cache while using IntelliJ Platform Gradle Plugin 2.18.1. This avoids the upstream concurrent `InstrumentCodeTask` race tracked as JetBrains/intellij-platform-gradle-plugin#2193. Remove the workaround after upgrading to a plugin version where that issue is fixed.

### Terminal toggle behavior

On IntelliJ, the built-in Terminal activation action can behave differently when the entire bottom tool-window area is hidden. The generated keymap therefore maps VS Code's `workbench.action.togglePanel` and `workbench.action.terminal.toggleTerminal` commands to a tiny adapter action:

- `Ctrl+J` shows and focuses Terminal when the bottom area is closed.
- `Ctrl+J` focuses Terminal when another tool window is active.
- `Ctrl+J` hides Terminal when Terminal is already visible.
- `Ctrl+`` uses the same toggle behavior.
- `Ctrl+Shift+`` creates a new Terminal tab through IntelliJ's native `Terminal.NewTab` action.
- `Ctrl+Shift+W` hides Terminal when it is visible. This is a curated workflow override stored separately from the official VS Code defaults.

The shortcut keys still come from the VS Code JSON source; the adapter only implements the closest IntelliJ behavior for those commands.

### IntelliJ 2025.2 terminal shortcut bridge

`Ctrl+J` is intercepted only while a `VS Code Complete` keymap is active. This is necessary because the Reworked Terminal can consume that control character before a normal custom keymap action receives it. The dispatcher consumes the complete Ctrl+J key sequence, including the modifier-less typed line-feed event that can follow the physical key press, so closing Terminal does not leak a newline into the shell. It also intercepts the close-terminal shortcut while Terminal is visible.

The generator also clears known parent-keymap conflicts before emitting strict VS Code bindings. In particular, the inherited IntelliJ `Ctrl+D` duplicate action is removed so the editor binding resolves to **Select Next Occurrence**.
