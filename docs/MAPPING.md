# Mapping model

Each reviewed VS Code command lives in `mappings/commands.json` with one of these statuses:

- `direct`: semantics match closely.
- `equivalent`: IntelliJ uses a different concept/name but the workflow matches.
- `adapter`: a tiny IntelliJ action is required.
- `unsupported`: intentionally omitted.

Stock bindings are read from the VS Code JSON and the command mapping only translates semantics. A very small set of deliberate workflow overrides lives in `mappings/shortcuts.json`; these are documented separately so they never masquerade as Microsoft defaults.

## Important Linux mappings

| VS Code command | VS Code key | IntelliJ action |
|---|---|---|
| `workbench.action.togglePanel` | `Ctrl+J` | Terminal tool window |
| `workbench.action.toggleSidebarVisibility` | `Ctrl+B` | Project tool window |
| `editor.action.addSelectionToNextFindMatch` | `Ctrl+D` | Select Next Occurrence |
| `workbench.action.terminal.toggleTerminal` | `Ctrl+\`` | Terminal tool window |
| `workbench.action.terminal.new` | `Ctrl+Shift+\`` | `Terminal.NewTab` |
| `workbench.action.quickOpen` | `Ctrl+P` | Go to File |
| `workbench.action.showCommands` | `Ctrl+Shift+P`, `F1` | Find Action |

The `Ctrl+J` translation is intentionally Terminal because IntelliJ has no single equivalent to VS Code's generic bottom panel and Terminal is the closest workflow match for this keymap.

## Curated terminal override

`Ctrl+Shift+W` hides the Terminal when it is visible. This binding is intentionally stored in `mappings/shortcuts.json` rather than in the VS Code command catalog because it is a project-specific workflow choice, not a stock VS Code default.
