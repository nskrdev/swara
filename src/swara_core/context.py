"""
Swara Core Library - Context Management Module

Captures context from the active window (selected text, clipboard, etc.)
"""

import subprocess
import time
from dataclasses import dataclass
from typing import Optional
import pyperclip
from .utils import get_logger
from .config import config

logger = get_logger("context")


@dataclass
class Context:
    """Represents the current execution context"""

    selected_text: Optional[str] = None
    selection_length: int = 0
    active_window: Optional[str] = None
    clipboard_backup: Optional[str] = None
    timestamp: float = 0.0

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()
        if self.selected_text:
            self.selection_length = len(self.selected_text)


class ContextManager:
    """Manages context capture and restoration"""

    def __init__(self):
        self.current_context: Optional[Context] = None
        self.capture_timeout = config.get("context.capture_timeout", 0.5)
        self.max_context_length = config.get("context.max_context_length", 5000)

    def capture_context(self) -> Context:
        """
        Capture current execution context
        Priority: Selected text > Clipboard

        Returns:
            Context: Captured context information
        """
        context = Context()

        # CRITICAL: Capture selection FIRST before any UI operations
        # that might steal focus
        context.selected_text = self._quick_selection_capture()

        if context.selected_text:
            # Truncate if too long
            if len(context.selected_text) > self.max_context_length:
                logger.warning(
                    f"Selected text too long ({len(context.selected_text)} chars), "
                    f"truncating to {self.max_context_length}"
                )
                context.selected_text = context.selected_text[: self.max_context_length]

            logger.info(f"Captured selection: {len(context.selected_text)} chars")

        # Get active window info (for context-aware behavior)
        context.active_window = self._get_active_window()

        # Backup clipboard
        try:
            context.clipboard_backup = pyperclip.paste()
        except Exception as e:
            logger.warning(f"Could not backup clipboard: {e}")

        self.current_context = context
        return context

    def restore_context(self):
        """Restore original context (e.g., clipboard)"""
        if self.current_context and self.current_context.clipboard_backup:
            try:
                pyperclip.copy(self.current_context.clipboard_backup)
                logger.debug("Context restored")
            except Exception as e:
                logger.warning(f"Could not restore clipboard: {e}")

    def _quick_selection_capture(self) -> Optional[str]:
        """
        Fast selection capture using multiple methods
        Returns immediately on first success
        """
        methods = [
            ("wl-paste primary", self._wl_paste_primary),
            ("simulate copy", self._simulate_copy),
        ]

        for method_name, method_func in methods:
            try:
                text = method_func()
                if text and len(text.strip()) > 0:
                    logger.debug(f"Selection captured via {method_name}")
                    return text.strip()
            except Exception as e:
                logger.debug(f"{method_name} failed: {e}")
                continue

        logger.debug("No selection found")
        return None

    def _wl_paste_primary(self) -> Optional[str]:
        """Wayland primary selection (fastest method)"""
        try:
            result = subprocess.run(
                ["wl-paste", "--primary"],
                capture_output=True,
                text=True,
                timeout=self.capture_timeout,
            )

            if result.returncode == 0 and result.stdout:
                return result.stdout

        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        return None

    def _simulate_copy(self) -> Optional[str]:
        """Simulate Ctrl+C to get selection (slower but more reliable)"""
        try:
            # Clear clipboard to detect new copy
            original = pyperclip.paste()
            pyperclip.copy("")

            # Simulate Ctrl+C using ydotool
            # Key codes: 29=Ctrl, 46=C
            subprocess.run(
                ["ydotool", "key", "29:1", "46:1", "46:0", "29:0"],
                timeout=self.capture_timeout,
            )

            # Wait for copy to complete
            time.sleep(0.15)

            new_text = pyperclip.paste()

            # Restore original clipboard if nothing new
            if not new_text or new_text == original:
                if original:
                    pyperclip.copy(original)
                return None

            return new_text

        except Exception as e:
            logger.debug(f"Simulate copy failed: {e}")
            return None

    def _get_active_window(self) -> Optional[str]:
        """Get active window class (Hyprland-specific)"""
        try:
            result = subprocess.run(
                ["hyprctl", "activewindow", "-j"],
                capture_output=True,
                text=True,
                timeout=self.capture_timeout,
            )

            if result.returncode == 0:
                import json

                window_info = json.loads(result.stdout)
                return window_info.get("class", "unknown")

        except Exception as e:
            logger.debug(f"Could not get active window: {e}")

        return None


# Global instance
_context_manager = None


def get_context_manager() -> ContextManager:
    """Get or create context manager instance"""
    global _context_manager
    if _context_manager is None:
        _context_manager = ContextManager()
    return _context_manager


def capture_context() -> Context:
    """
    Convenience function to capture context

    Returns:
        Context: Current context
    """
    manager = get_context_manager()
    return manager.capture_context()


def restore_context():
    """Convenience function to restore context"""
    manager = get_context_manager()
    manager.restore_context()
