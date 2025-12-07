"""
Swara Core Library - Notification Module

Handles desktop notifications and status updates.
"""

import subprocess
from typing import Optional
from .utils import get_logger
from .config import config

logger = get_logger("notify")


class Notifier:
    """Desktop notification manager"""

    def __init__(self):
        self.enabled = config.get("notifications.enabled", True)
        self.duration = config.get("notifications.duration", 2000)
        self.app_name = "Swara"

    def send(
        self,
        title: str,
        message: str = "",
        urgency: str = "normal",
        icon: Optional[str] = None,
    ):
        """
        Send desktop notification

        Args:
            title: Notification title
            message: Notification body
            urgency: 'low', 'normal', or 'critical'
            icon: Icon name or path (optional)
        """
        if not self.enabled:
            return

        try:
            cmd = [
                "notify-send",
                "-u",
                urgency,
                "-t",
                str(self.duration),
                "-a",
                self.app_name,
            ]

            if icon:
                cmd.extend(["-i", icon])

            cmd.append(title)

            if message:
                cmd.append(message)

            subprocess.run(cmd, check=False, timeout=2)
            logger.debug(f"Notification sent: {title}")

        except Exception as e:
            logger.warning(f"Failed to send notification: {e}")

    def recording(self):
        """Show recording notification"""
        self.send("🎤 Recording...", "Speak now", urgency="low")

    def transcribing(self):
        """Show transcribing notification"""
        self.send("✍️ Transcribing...", "Processing audio", urgency="low")

    def processing(self):
        """Show AI processing notification"""
        self.send("🤖 Processing...", "Analyzing with AI", urgency="low")

    def formatting(self):
        """Show formatting notification"""
        self.send("📝 Formatting...", "Adding punctuation", urgency="low")

    def capturing_context(self):
        """Show context capture notification"""
        self.send("📍 Capturing context...", "Reading selection", urgency="low")

    def success(self, preview: str):
        """
        Show success notification with preview

        Args:
            preview: Preview text to show
        """
        preview_length = config.get("notifications.preview_length", 50)
        if len(preview) > preview_length:
            preview = preview[:preview_length] + "..."

        self.send("✓ Done", preview, urgency="normal")

    def error(self, message: str, critical: bool = False):
        """
        Show error notification

        Args:
            message: Error message
            critical: If True, show as critical urgency
        """
        urgency = "critical" if critical else "normal"
        self.send("⚠️ Error", message, urgency=urgency)

    def clipboard_fallback(self, preview: str):
        """Show clipboard fallback notification"""
        preview_length = config.get("notifications.preview_length", 50)
        if len(preview) > preview_length:
            preview = preview[:preview_length] + "..."

        self.send(
            "📋 Copied to Clipboard",
            f"Press Ctrl+V to paste:\n{preview}",
            urgency="normal",
        )


# Global notifier instance
notifier = Notifier()
