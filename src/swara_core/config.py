"""
Swara Core Library - Configuration Module

Loads configuration from YAML files and environment variables.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DEFAULT_CONFIG = CONFIG_DIR / "default.yaml"


class Config:
    """Configuration manager for Swara"""

    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Load configuration from YAML file"""
        if DEFAULT_CONFIG.exists():
            with open(DEFAULT_CONFIG, "r") as f:
                self._config = yaml.safe_load(f) or {}
        else:
            print(f"Warning: Config file not found at {DEFAULT_CONFIG}")
            self._config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Fallback default configuration"""
        return {
            "audio": {
                "mode": "toggle",
                "max_duration": 30,
                "beep_on_start": True,
                "beep_on_stop": True,
                "sample_rate": 16000,
                "channels": 1,
                "chunk_size": 1024,
            },
            "whisper": {
                "model_path": str(
                    Path.home() / "whisper.cpp" / "models" / "ggml-base.bin"
                ),
                "executable": str(Path.home() / "whisper.cpp" / "main"),
                "language": "en",
            },
            "punctuation": {
                "enabled": True,
                "model": "oliverguhr/fullstop-punctuation-multilang-large",
            },
            "gemini": {
                "model": "gemini-2.0-flash-exp",
                "temperature": 0.3,
                "max_tokens": 2048,
                "timeout": 10,
            },
            "context": {
                "auto_detect": True,
                "max_context_length": 5000,
                "capture_timeout": 0.5,
            },
            "output": {
                "typing_delay": 0.01,
                "injection_strategy": "auto",
                "fallback_to_clipboard": True,
                "show_preview_notification": True,
            },
            "notifications": {
                "enabled": True,
                "duration": 2000,
                "show_preview": True,
                "preview_length": 50,
            },
            "logging": {
                "level": "INFO",
                "file": str(PROJECT_ROOT / "logs" / "swara.log"),
            },
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key"""
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable"""
        return os.getenv(key, default)

    @property
    def gemini_api_key(self) -> Optional[str]:
        """Get Gemini API key from environment"""
        return self.get_env("GEMINI_API_KEY")

    @property
    def whisper_executable(self) -> str:
        """Get Whisper executable path"""
        env_path = self.get_env("WHISPER_EXECUTABLE")
        if env_path:
            return env_path
        return str(Path(self.get("whisper.executable")).expanduser())

    @property
    def whisper_model(self) -> str:
        """Get Whisper model path"""
        env_path = self.get_env("WHISPER_MODEL")
        if env_path:
            return env_path
        return str(Path(self.get("whisper.model_path")).expanduser())


# Global config instance
config = Config()
