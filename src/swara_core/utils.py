"""
Swara Core Library - Utilities Module

General utility functions used across the project.
"""

import logging
import os
from pathlib import Path
from typing import Optional
from .config import config

# Setup logging
LOG_FILE = Path(config.get("logging.file"))
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, config.get("logging.level", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

logger = logging.getLogger("swara")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(f"swara.{name}")


def get_temp_audio_file() -> str:
    """Generate temporary audio file path"""
    import tempfile
    import time

    temp_dir = Path(tempfile.gettempdir()) / "swara"
    temp_dir.mkdir(exist_ok=True)

    timestamp = int(time.time() * 1000)
    return str(temp_dir / f"audio_{timestamp}.wav")


def cleanup_temp_files(audio_file: str):
    """Clean up temporary files"""
    try:
        if os.path.exists(audio_file):
            os.remove(audio_file)

        # Also remove any .txt files created by whisper
        txt_file = f"{audio_file}.txt"
        if os.path.exists(txt_file):
            os.remove(txt_file)
    except Exception as e:
        logger.warning(f"Failed to cleanup temp files: {e}")


def validate_system_dependencies() -> dict:
    """
    Validate that all system dependencies are installed

    Returns:
        dict: Status of each dependency
    """
    import shutil

    dependencies = {
        "ydotool": shutil.which("ydotool") is not None,
        "wl-paste": shutil.which("wl-paste") is not None,
        "wl-copy": shutil.which("wl-copy") is not None,
        "notify-send": shutil.which("notify-send") is not None,
        "paplay": shutil.which("paplay") is not None
        or shutil.which("aplay") is not None,
    }

    # Check whisper.cpp
    whisper_exec = Path(config.whisper_executable)
    whisper_model = Path(config.whisper_model)

    dependencies["whisper_executable"] = whisper_exec.exists()
    dependencies["whisper_model"] = whisper_model.exists()

    return dependencies


def check_user_in_input_group() -> bool:
    """Check if user is in the input group (required for ydotool)"""
    import subprocess

    try:
        result = subprocess.run(["groups"], capture_output=True, text=True)
        return "input" in result.stdout
    except:
        return False


def escape_for_shell(text: str) -> str:
    """Escape text for safe shell usage"""
    # Replace problematic characters
    replacements = {
        "\\": "\\\\",
        '"': '\\"',
        "$": "\\$",
        "`": "\\`",
        "\n": "\\n",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text
