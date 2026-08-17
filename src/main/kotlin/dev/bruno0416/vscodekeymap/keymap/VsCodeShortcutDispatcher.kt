package dev.bruno0416.vscodekeymap.keymap

import com.intellij.ide.DataManager
import com.intellij.openapi.Disposable
import com.intellij.openapi.actionSystem.ActionManager
import com.intellij.openapi.actionSystem.CommonDataKeys
import com.intellij.openapi.keymap.Keymap
import com.intellij.openapi.keymap.KeymapManager
import com.intellij.openapi.project.Project
import dev.bruno0416.vscodekeymap.actions.HideTerminalAction
import dev.bruno0416.vscodekeymap.actions.ToggleTerminalAction
import java.awt.KeyEventDispatcher
import java.awt.KeyboardFocusManager
import java.awt.event.InputEvent
import java.awt.event.KeyEvent
import java.util.concurrent.atomic.AtomicBoolean

/**
 * Handles VS Code shortcuts that need deterministic behavior before a focused component consumes them.
 *
 * IntelliJ 2025.2's Reworked Terminal can turn Ctrl+J into a line-feed. A Ctrl+J sequence may
 * arrive as KEY_PRESSED with Ctrl followed by a KEY_TYPED line-feed whose modifier mask is empty.
 * We therefore remember the accepted press and consume its typed/released tail explicitly.
 *
 * Alt+Up/Down is also bridged while an editor has focus so VS Code's move-line workflow wins over
 * contextual IntelliJ actions. The bridge delegates to IntelliJ's native MoveLineUp/MoveLineDown
 * actions, preserving selection and editor undo semantics.
 */
class VsCodeShortcutDispatcher : Disposable {
    private val installed = AtomicBoolean()
    private val swallowCtrlJ = AtomicBoolean()
    private val swallowCloseTerminal = AtomicBoolean()
    private val dispatcher = KeyEventDispatcher(::dispatch)

    fun install() {
        if (installed.compareAndSet(false, true)) {
            KeyboardFocusManager.getCurrentKeyboardFocusManager()
                .addKeyEventDispatcher(dispatcher)
        }
    }

    private fun dispatch(event: KeyEvent): Boolean {
        val keymap = activeVsCodeKeymap() ?: return false
        val macosKeymap = keymap.name.contains("(macOS)")

        // KEY_TYPED frequently loses the Ctrl modifier. Consume it based on the accepted press.
        if (event.id == KeyEvent.KEY_TYPED && swallowCtrlJ.get() && isLineFeed(event.keyChar)) {
            event.consume()
            return true
        }

        if (event.id == KeyEvent.KEY_RELEASED && swallowCtrlJ.get() && isJRelease(event)) {
            swallowCtrlJ.set(false)
            event.consume()
            return true
        }

        if (event.id == KeyEvent.KEY_RELEASED && swallowCloseTerminal.get() && event.keyCode == KeyEvent.VK_W) {
            swallowCloseTerminal.set(false)
            event.consume()
            return true
        }

        if (event.id != KeyEvent.KEY_PRESSED) return false

        if (isPanelTogglePress(event, macosKeymap)) {
            swallowCtrlJ.set(true)
            currentProject()
                ?.takeUnless { it.isDisposed }
                ?.let(ToggleTerminalAction::toggle)
            event.consume()
            return true
        }

        if (isMoveLinePress(event) && moveLine(event)) {
            event.consume()
            return true
        }

        if (isCloseTerminalPress(event, macosKeymap)) {
            val project = currentProject()?.takeUnless { it.isDisposed } ?: return false
            if (HideTerminalAction.isVisible(project)) {
                swallowCloseTerminal.set(true)
                HideTerminalAction.hide(project)
                event.consume()
                return true
            }
        }

        return false
    }

    private fun isPanelTogglePress(event: KeyEvent, macosKeymap: Boolean): Boolean {
        if (event.keyCode != KeyEvent.VK_J) return false
        val required = if (macosKeymap) InputEvent.META_DOWN_MASK else InputEvent.CTRL_DOWN_MASK
        val forbidden = if (macosKeymap) {
            InputEvent.CTRL_DOWN_MASK or InputEvent.SHIFT_DOWN_MASK or InputEvent.ALT_DOWN_MASK
        } else {
            InputEvent.META_DOWN_MASK or InputEvent.SHIFT_DOWN_MASK or InputEvent.ALT_DOWN_MASK
        }
        return event.modifiersEx and required != 0 && event.modifiersEx and forbidden == 0
    }

    private fun isMoveLinePress(event: KeyEvent): Boolean {
        if (event.keyCode != KeyEvent.VK_UP && event.keyCode != KeyEvent.VK_DOWN) return false
        val required = InputEvent.ALT_DOWN_MASK
        val forbidden = InputEvent.CTRL_DOWN_MASK or InputEvent.META_DOWN_MASK or InputEvent.SHIFT_DOWN_MASK
        return event.modifiersEx and required != 0 && event.modifiersEx and forbidden == 0
    }

    private fun moveLine(event: KeyEvent): Boolean {
        val focusOwner = KeyboardFocusManager.getCurrentKeyboardFocusManager().focusOwner ?: return false
        val context = DataManager.getInstance().getDataContext(focusOwner)
        if (CommonDataKeys.EDITOR.getData(context) == null) return false

        val actionId = if (event.keyCode == KeyEvent.VK_UP) MOVE_LINE_UP else MOVE_LINE_DOWN
        val actionManager = ActionManager.getInstance()
        val action = actionManager.getAction(actionId) ?: return false
        actionManager.tryToExecute(action, event, focusOwner, null, true)
        return true
    }

    private fun isCloseTerminalPress(event: KeyEvent, macosKeymap: Boolean): Boolean {
        if (event.keyCode != KeyEvent.VK_W) return false
        val primary = if (macosKeymap) InputEvent.META_DOWN_MASK else InputEvent.CTRL_DOWN_MASK
        val required = primary or InputEvent.SHIFT_DOWN_MASK
        val forbidden = if (macosKeymap) InputEvent.CTRL_DOWN_MASK or InputEvent.ALT_DOWN_MASK
        else InputEvent.META_DOWN_MASK or InputEvent.ALT_DOWN_MASK
        return event.modifiersEx and required == required && event.modifiersEx and forbidden == 0
    }

    private fun isJRelease(event: KeyEvent): Boolean =
        event.keyCode == KeyEvent.VK_J || isLineFeed(event.keyChar)

    private fun isLineFeed(char: Char): Boolean = char == '\n' || char == '\u000A'

    private fun activeVsCodeKeymap(): Keymap? {
        val keymap = KeymapManager.getInstance()?.activeKeymap ?: return null
        return keymap.takeIf { it.name.startsWith(KEYMAP_PREFIX) }
    }

    private fun currentProject(): Project? {
        val focusOwner = KeyboardFocusManager.getCurrentKeyboardFocusManager().focusOwner ?: return null
        val context = DataManager.getInstance().getDataContext(focusOwner)
        return CommonDataKeys.PROJECT.getData(context)
    }

    override fun dispose() {
        if (installed.compareAndSet(true, false)) {
            KeyboardFocusManager.getCurrentKeyboardFocusManager()
                .removeKeyEventDispatcher(dispatcher)
        }
        swallowCtrlJ.set(false)
        swallowCloseTerminal.set(false)
    }

    private companion object {
        const val KEYMAP_PREFIX = "VS Code Complete"
        const val MOVE_LINE_UP = "MoveLineUp"
        const val MOVE_LINE_DOWN = "MoveLineDown"
    }
}
