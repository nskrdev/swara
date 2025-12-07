"""
Swara Core Library - Punctuation Restoration Module

Adds punctuation and capitalization to transcribed text.
"""

from typing import Optional
from .utils import get_logger
from .config import config
from .notify import notifier

logger = get_logger("punctuation")


class PunctuationRestorer:
    """Restores punctuation to text using deep learning model"""

    def __init__(self):
        self.enabled = config.get("punctuation.enabled", True)
        self._model = None

    @property
    def model(self):
        """Lazy load punctuation model"""
        if self._model is None and self.enabled:
            try:
                logger.info(
                    "Loading punctuation model (first use may take a moment)..."
                )
                from deepmultilingualpunctuation import PunctuationModel

                self._model = PunctuationModel()
                logger.info("Punctuation model loaded")
            except Exception as e:
                logger.error(f"Failed to load punctuation model: {e}")
                self.enabled = False
        return self._model

    def restore(self, text: str) -> str:
        """
        Add punctuation and capitalization to text

        Args:
            text: Input text without punctuation

        Returns:
            str: Text with punctuation restored
        """
        if not text or not text.strip():
            return text

        if not self.enabled:
            logger.debug("Punctuation restoration disabled, returning original text")
            return text

        try:
            logger.debug(f"Restoring punctuation for: {text[:50]}...")
            notifier.formatting()

            result = self.model.restore_punctuation(text)

            logger.info(f"Punctuation restored: {result[:100]}...")
            return result

        except Exception as e:
            logger.error(f"Punctuation restoration failed: {e}")
            # Fallback: return original text
            return text


# Global instance
_restorer = None


def get_restorer() -> PunctuationRestorer:
    """Get or create punctuation restorer instance"""
    global _restorer
    if _restorer is None:
        _restorer = PunctuationRestorer()
    return _restorer


def restore_punctuation(text: str) -> str:
    """
    Convenience function to restore punctuation

    Args:
        text: Input text

    Returns:
        str: Text with punctuation
    """
    restorer = get_restorer()
    return restorer.restore(text)
