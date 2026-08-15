# Contributing

Contributions should preserve VS Code-first behavior.

For a shortcut change:

1. Identify the VS Code command and platform-specific default shortcut.
2. Identify the real IntelliJ Action ID with the closest semantic behavior.
3. Classify the mapping as direct, equivalent, adapter, or unsupported.
4. Update the runtime keymap and `mappings/` documentation.
5. Run `./scripts/verify.sh`.

Do not add IntelliJ-native shortcuts solely because they are useful; this project intentionally follows VS Code muscle memory.


## Runtime code

Use Kotlin for IntelliJ runtime code. Keep generated keymaps and mapping logic out of runtime whenever possible; Python scripts remain the development-time generation layer.
