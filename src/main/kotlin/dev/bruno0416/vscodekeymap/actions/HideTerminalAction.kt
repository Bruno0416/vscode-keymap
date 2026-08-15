package dev.bruno0416.vscodekeymap.actions

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.project.DumbAware
import com.intellij.openapi.project.Project
import com.intellij.openapi.wm.ToolWindowManager

/** Hides IntelliJ's Terminal tool window when it is visible. */
class HideTerminalAction : AnAction(), DumbAware {
    override fun actionPerformed(event: AnActionEvent) {
        event.project?.let(::hide)
    }

    companion object {
        private const val TERMINAL_TOOL_WINDOW_ID = "Terminal"

        fun hide(project: Project): Boolean {
            val terminal = ToolWindowManager.getInstance(project)
                .getToolWindow(TERMINAL_TOOL_WINDOW_ID)
                ?: return false

            if (!terminal.isVisible) return false
            terminal.hide()
            return true
        }

        fun isVisible(project: Project): Boolean =
            ToolWindowManager.getInstance(project)
                .getToolWindow(TERMINAL_TOOL_WINDOW_ID)
                ?.isVisible == true
    }
}
