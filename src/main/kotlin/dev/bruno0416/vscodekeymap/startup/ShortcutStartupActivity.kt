package dev.bruno0416.vscodekeymap.startup

import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.startup.StartupActivity
import dev.bruno0416.vscodekeymap.keymap.VsCodeShortcutDispatcher

/** Installs the global VS Code shortcut bridge once the first project is opened. */
class ShortcutStartupActivity : StartupActivity.DumbAware {
    override fun runActivity(project: Project) {
        ApplicationManager.getApplication()
            .getService(VsCodeShortcutDispatcher::class.java)
            .install()
    }
}
