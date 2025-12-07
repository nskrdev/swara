"""
Swara Core Library

Intelligent voice dictation tool with context awareness and AI processing.
"""

from .config import config
from .utils import get_logger, validate_system_dependencies, check_user_in_input_group
from .notify import notifier
from .audio import AudioRecorder, record_audio
from .transcribe import transcribe, get_transcriber
from .punctuation import restore_punctuation, get_restorer
from .context import Context, ContextManager, capture_context, restore_context
from .gemini import GeminiProcessor, process_with_gemini
from .inject import inject_text, get_injector

__version__ = "1.0.0"
__author__ = "Swara Project"

__all__ = [
    # Config
    "config",
    # Utils
    "get_logger",
    "validate_system_dependencies",
    "check_user_in_input_group",
    # Notifications
    "notifier",
    # Audio
    "AudioRecorder",
    "record_audio",
    # Transcription
    "transcribe",
    "get_transcriber",
    # Punctuation
    "restore_punctuation",
    "get_restorer",
    # Context
    "Context",
    "ContextManager",
    "capture_context",
    "restore_context",
    # AI Processing
    "GeminiProcessor",
    "process_with_gemini",
    # Text Injection
    "inject_text",
    "get_injector",
]
