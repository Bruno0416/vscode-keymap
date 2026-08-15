package dev.bruno0416.vscodekeymap.actions

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.options.SearchableConfigurable
import com.intellij.openapi.options.ShowSettingsUtil

/** Opens IntelliJ's Keymap settings, equivalent to VS Code's Keyboard Shortcuts editor. */
class OpenKeymapSettingsAction : AnAction() {
    override fun actionPerformed(event: AnActionEvent) {
        ShowSettingsUtil.getInstance().showSettingsDialog(
            event.project,
            { configurable ->
                configurable is SearchableConfigurable && configurable.id == KEYMAP_CONFIGURABLE_ID
            },
            null,
        )
    }

    private companion object {
        const val KEYMAP_CONFIGURABLE_ID = "preferences.keymap"
    }
}
