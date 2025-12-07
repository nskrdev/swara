"""
Swara Core Library - Text Injection Module

Handles intelligent text injection with multiple strategies and fallbacks.
"""

import subprocess
import time
from typing import Optional
from dataclasses import dataclass
import pyperclip
from .utils import get_logger, escape_for_shell
from .config import config
from .notify import notifier
from .context import Context

logger = get_logger("inject")


@dataclass
class InjectionContext:
    """Context for text injection"""

    had_selection: bool
    selection_length: int
    app_class: str


class SmartTextInjector:
    """Intelligent text injection with strategy selection"""

    # Apps that handle typing-over-selection natively
    NATIVE_REPLACE_APPS = [
        "brave",
        "chromium",
        "firefox",
        "code",
        "cursor",
        "sublime",
        "gedit",
        "kate",
        "mousepad",
    ]

    # Apps that need explicit deletion
    EXPLICIT_DELETE_APPS = [
        "terminal",
        "kitty",
        "alacritty",
        "konsole",
        "ghostty",
        "wezterm",
        "foot",
        "gnome-terminal",
    ]

    def __init__(self):
        self.typing_delay = config.get("output.typing_delay", 0.01)
        self.injection_strategy = config.get("output.injection_strategy", "auto")
        self.fallback_to_clipboard = config.get("output.fallback_to_clipboard", True)

    def inject(
        self, text: str, context: Optional[Context] = None, strategy: str = "auto"
    ) -> bool:
        """
        Inject text with intelligent strategy selection

        Args:
            text: Text to inject
            context: Execution context (optional)
            strategy: 'auto', 'native', 'explicit', or 'paste'

        Returns:
            bool: True if successful
        """
        if not text:
            logger.warning("No text to inject")
            return False

        # Build injection context
        inj_ctx = InjectionContext(
            had_selection=bool(context and context.selected_text),
            selection_length=context.selection_length if context else 0,
            app_class=context.active_window if context else "unknown",
        )

        # Choose strategy
        if strategy == "auto":
            strategy = self._choose_strategy(inj_ctx)

        logger.info(f"Injecting text using strategy: {strategy}")

        # Try primary strategy
        success = self._execute_strategy(text, inj_ctx, strategy)

        if not success and self.fallback_to_clipboard:
            logger.warning("Primary injection failed, falling back to clipboard")
            return self._fallback_paste(text)

        return success

    def _choose_strategy(self, context: InjectionContext) -> str:
        """Choose best injection strategy based on context"""
        if not context.had_selection:
            return "native"  # Simple typing

        app = context.app_class.lower() if context.app_class else ""

        # Check if app handles replace-on-type well
        if any(a in app for a in self.NATIVE_REPLACE_APPS):
            return "native"

        # Terminal-like apps need explicit deletion
        if any(a in app for a in self.EXPLICIT_DELETE_APPS):
            return "explicit"

        # Unknown app - try native first
        return "native"

    def _execute_strategy(
        self, text: str, context: InjectionContext, strategy: str
    ) -> bool:
        """Execute injection strategy"""
        try:
            if strategy == "native":
                # Typing replaces selection automatically in most apps
                return self._type_text(text)

            elif strategy == "explicit":
                # Delete selection first, then type
                if context.had_selection:
                    self._delete_selection()
                    time.sleep(0.1)
                return self._type_text(text)

            elif strategy == "paste":
                # Use Ctrl+V (fastest, but uses clipboard)
                return self._paste_text(text)

            else:
                logger.error(f"Unknown strategy: {strategy}")
                return False

        except Exception as e:
            logger.error(f"Injection failed with {strategy}: {e}")
            return False

    def _type_text(self, text: str) -> bool:
        """Type text character by character using ydotool"""
        try:
            # Escape special characters
            escaped = escape_for_shell(text)

            # Calculate delay in milliseconds
            delay_ms = int(self.typing_delay * 1000)

            subprocess.run(
                ["ydotool", "type", "--key-delay", str(delay_ms), escaped],
                check=True,
                timeout=30,
            )

            logger.info("Text typed successfully")
            return True

        except subprocess.TimeoutExpired:
            logger.error("Typing timeout - text too long?")
            return False
        except FileNotFoundError:
            logger.error("ydotool not found - is it installed?")
            return False
        except Exception as e:
            logger.error(f"Typing failed: {e}")
            return False

    def _delete_selection(self):
        """Delete selection by simulating backspace"""
        try:
            # Single backspace (works if selection still active)
            # Key code 14 = Backspace
            subprocess.run(["ydotool", "key", "14:1", "14:0"], timeout=1)
            logger.debug("Selection deleted")
        except Exception as e:
            logger.warning(f"Could not delete selection: {e}")

    def _paste_text(self, text: str) -> bool:
        """Paste text using Ctrl+V"""
        try:
            # Backup clipboard
            original = pyperclip.paste()

            # Copy new text
            pyperclip.copy(text)
            time.sleep(0.05)

            # Simulate Ctrl+V
            # Key codes: 29=Ctrl, 47=V
            subprocess.run(
                ["ydotool", "key", "29:1", "47:1", "47:0", "29:0"], timeout=1
            )
            time.sleep(0.1)

            # Restore clipboard
            pyperclip.copy(original)

            logger.info("Text pasted successfully")
            return True

        except Exception as e:
            logger.error(f"Paste failed: {e}")
            return False

    def _fallback_paste(self, text: str) -> bool:
        """
        Ultimate fallback: Copy to clipboard and notify user

        Args:
            text: Text to copy

        Returns:
            bool: Always returns True (fallback always "succeeds")
        """
        try:
            pyperclip.copy(text)
            notifier.clipboard_fallback(text)
            logger.info("Text copied to clipboard (manual paste required)")
            return True
        except Exception as e:
            logger.error(f"Clipboard fallback failed: {e}")
            notifier.error("Failed to inject text", critical=True)
            return False


# Global instance
_injector = None


def get_injector() -> SmartTextInjector:
    """Get or create text injector instance"""
    global _injector
    if _injector is None:
        _injector = SmartTextInjector()
    return _injector


def inject_text(text: str, context: Optional[Context] = None) -> bool:
    """
    Convenience function to inject text

    Args:
        text: Text to inject
        context: Execution context (optional)

    Returns:
        bool: True if successful
    """
    injector = get_injector()
    return injector.inject(text, context)
