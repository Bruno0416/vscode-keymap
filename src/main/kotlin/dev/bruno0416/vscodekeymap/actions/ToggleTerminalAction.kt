package dev.bruno0416.vscodekeymap.actions

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.project.DumbAware
import com.intellij.openapi.project.Project
import com.intellij.openapi.wm.ToolWindowManager

/** Toggles IntelliJ's Terminal tool window with VS Code-like panel semantics. */
class ToggleTerminalAction : AnAction(), DumbAware {
    override fun actionPerformed(event: AnActionEvent) {
        event.project?.let(::toggle)
    }

    companion object {
        private const val TERMINAL_TOOL_WINDOW_ID = "Terminal"

        fun toggle(project: Project) {
            val terminal = ToolWindowManager.getInstance(project)
                .getToolWindow(TERMINAL_TOOL_WINDOW_ID)
                ?: return

            if (!terminal.isAvailable) return

            if (terminal.isVisible) {
                terminal.hide()
                return
            }

            terminal.show {
                terminal.activate(null, true)
            }
        }
    }
}
