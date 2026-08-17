# Changelog

## 0.2.6

- Guarantee VS Code's `Alt+Up` / `Alt+Down` move-line workflow while an editor has focus.
- Delegate the shortcut to IntelliJ's native `MoveLineUp` / `MoveLineDown` actions so selected lines move together and undo behavior remains native.
- Keep the mapping as an explicit curated override on Linux, Windows, and macOS so future VS Code source refreshes cannot drop it.
- Extend keymap validation to require the Linux `Alt+Up` / `Alt+Down` bindings.

## 0.2.5

- Finalized the public namespace as `dev.bruno0416.vscodekeymap` before the first repository release.
- Updated plugin ID, Kotlin packages, custom action IDs, vendor metadata, and Gradle group to the GitHub-oriented namespace.
- Corrected the copyright holder name to Bruno Valladares.
- Map `Ctrl+Shift+`` to IntelliJ's native `Terminal.NewTab` action so it creates a new terminal tab instead of merely activating Terminal.
- Add `Ctrl+Shift+W` as an explicit close-terminal workflow binding while Terminal is visible.
- Harden the Ctrl+J dispatcher to consume the complete key sequence, including the modifier-less typed line-feed event produced by the terminal.
- Add `mappings/shortcuts.json` for deliberate workflow overrides while keeping Microsoft VS Code JSON as the source of truth for stock bindings.
- Ignore Gradle/IDE/build/Python/patch artifacts, including the accidental `bin/` output shown during development.

## 0.2.4

- Migrate all IntelliJ runtime code from Java to Kotlin.
- Keep the plugin behavior, action IDs, generated keymaps, terminal bridge and VS Code mapping pipeline unchanged.
- Use Kotlin/JVM 2.1.20 with JVM 21 to keep the plugin Kotlin-first alongside ChromaCore and Flow Icons.
- Remove `src/main/java` from the project.


## 0.2.3

- Make `Ctrl+J` a true global Terminal toggle even while the Terminal has focus.
- Intercept the VS Code panel shortcut before the terminal shell can interpret `Ctrl+J` as a line-feed control character.
- Apply the interceptor only while one of the `VS Code Complete` keymaps is active.
- Clear inherited IntelliJ `Ctrl+D` conflicts so `Ctrl+D` consistently selects the next occurrence in the editor.
- Add an explicit parent-conflict catalog used by the keymap generator.


## 0.2.2

- Added a dedicated Terminal toggle adapter for VS Code panel semantics.
- `Ctrl+J` now opens and focuses Terminal even when the entire bottom tool-window area is hidden.
- `Ctrl+J` hides Terminal when Terminal is already the active tool window.
- `Ctrl+`` uses the same robust toggle behavior; `Ctrl+Shift+`` remains mapped to the VS Code new-terminal workflow.
- No changes to the official VS Code JSON source-of-truth pipeline.

## 0.2.1

- Work around IntelliJ Platform Gradle Plugin 2.18.1 instrumentation race by disabling Gradle Configuration Cache for plugin builds.
- Build and verification scripts now explicitly use `--no-configuration-cache`.
- No runtime keymap behavior changes from 0.2.0.


## 0.2.0

- Replaced the JetBrains VSCode keymap as generation source with VS Code default JSON.
- Added official upstream source metadata for Linux, Windows and macOS.
- Added optional import of personal VS Code `keybindings.json` overrides.
- Added semantic `VS Code command -> IntelliJ Action ID` generation.
- Corrected Linux muscle-memory mappings including Ctrl+J, Ctrl+B and Ctrl+D.
- Kept the Open Keyboard Shortcuts adapter for Ctrl+K Ctrl+S.
- Added coverage and validation tooling for the generated keymap.

## 0.1.0

- Initial JetBrains-baseline prototype.
