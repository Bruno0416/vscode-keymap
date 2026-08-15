# Development

## Refresh official VS Code defaults

```bash
python3 scripts/update_vscode_defaults.py
```

The source URLs are stored in `sources/vscode/upstream.json` and point to Microsoft's generated default keybinding JSON files.

## Optional: import your personal VS Code keybindings

```bash
python3 scripts/import_vscode_keybindings.py
```

or:

```bash
python3 scripts/import_vscode_keybindings.py ~/.config/Code/User/keybindings.json
```

The imported file is written to `sources/user/keybindings.local.json` and is ignored by Git.

Then regenerate:

```bash
python3 scripts/generate_keymaps.py
python3 scripts/validate_keymaps.py
```

## Build

```bash
./scripts/build.sh
```


## Runtime language

Runtime plugin code lives under `src/main/kotlin` and targets JVM 21. Keep adapters small and prefer native IntelliJ actions before adding new Kotlin runtime behavior.
