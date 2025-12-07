"""
Swara Core Library - Transcription Module

Interfaces with Whisper.cpp for speech-to-text transcription.
"""

import subprocess
import os
from pathlib import Path
from typing import Optional
from .utils import get_logger, cleanup_temp_files
from .config import config
from .notify import notifier

logger = get_logger("transcribe")


class WhisperTranscriber:
    """Whisper.cpp transcription interface"""

    def __init__(self):
        self.executable = config.whisper_executable
        self.model = config.whisper_model
        self.language = config.get("whisper.language", "en")

        # Validate paths
        if not Path(self.executable).exists():
            raise FileNotFoundError(
                f"Whisper executable not found: {self.executable}\n"
                "Run: scripts/install.sh to install whisper.cpp"
            )

        if not Path(self.model).exists():
            raise FileNotFoundError(
                f"Whisper model not found: {self.model}\n"
                "Run: scripts/download-whisper.sh to download models"
            )

    def transcribe(self, audio_file: str) -> str:
        """
        Transcribe audio file to text

        Args:
            audio_file: Path to audio file (WAV format)

        Returns:
            str: Transcribed text
        """
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        logger.info(f"Transcribing: {audio_file}")
        notifier.transcribing()

        try:
            # Run whisper.cpp
            result = subprocess.run(
                [
                    self.executable,
                    "-m",
                    self.model,
                    "-f",
                    audio_file,
                    "-nt",  # No timestamps
                    "-l",
                    self.language,
                    "-otxt",  # Output as txt file
                    "-pp",  # Print progress
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                logger.error(f"Whisper error (stderr): {result.stderr}")
                logger.error(f"Whisper error (stdout): {result.stdout}")
                raise Exception(
                    f"Whisper transcription failed: {result.stderr or result.stdout}"
                )

            # Read output file (whisper.cpp creates audio_file.txt)
            output_file = f"{audio_file}.txt"

            if os.path.exists(output_file):
                with open(output_file, "r", encoding="utf-8") as f:
                    text = f.read().strip()

                # Cleanup output file
                os.remove(output_file)

                if not text:
                    logger.warning("Empty transcription")
                    return ""

                logger.info(f"Transcription: {text[:100]}...")
                return text
            else:
                logger.error("Whisper did not create output file")
                return ""

        except subprocess.TimeoutExpired:
            logger.error("Whisper transcription timeout")
            raise Exception("Transcription timeout - audio too long?")
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise
        finally:
            # Cleanup temp files
            cleanup_temp_files(audio_file)


# Global transcriber instance
_transcriber = None


def get_transcriber() -> WhisperTranscriber:
    """Get or create transcriber instance"""
    global _transcriber
    if _transcriber is None:
        _transcriber = WhisperTranscriber()
    return _transcriber


def transcribe(audio_file: str) -> str:
    """
    Convenience function to transcribe audio

    Args:
        audio_file: Path to audio file

    Returns:
        str: Transcribed text
    """
    transcriber = get_transcriber()
    return transcriber.transcribe(audio_file)
