# Architecture

The runtime plugin is intentionally small and Kotlin-first. Generated IntelliJ keymap XML is the primary runtime data, plus a few Kotlin adapter actions when IntelliJ has no direct action.

## Source pipeline

```text
Microsoft VS Code default JSON
            +
optional local keybindings.json
            |
            v
   effective VS Code bindings
            |
            v
 mappings/commands.json
 VS Code command -> IntelliJ Action ID
            +
 mappings/shortcuts.json
 explicit workflow overrides
            |
            v
 scripts/generate_keymaps.py
            |
            v
 src/main/resources/keymaps/*.xml
```

VS Code source data owns stock shortcuts. The project owns only the semantic translation plus the small, explicit override set in `mappings/shortcuts.json`.

`when` clauses cannot be represented 1:1 by IntelliJ keymap XML. Context-sensitive commands are therefore added only when their IntelliJ action is a safe semantic equivalent. More complex contexts will be implemented as adapter actions only when necessary.


## Runtime code

```text
src/main/kotlin/dev/bruno0416/vscodekeymap/
├── actions/
├── keymap/
└── startup/
```

The runtime adapters use Kotlin/JVM and Java 21. Python remains limited to development-time source synchronization, mapping, generation and validation.
