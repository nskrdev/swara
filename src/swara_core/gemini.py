"""
Swara Core Library - Gemini AI Module

Handles AI-powered text processing using Google's Gemini API.
"""

from typing import Tuple, Optional
import google.generativeai as genai
from .utils import get_logger
from .config import config
from .notify import notifier
from .context import Context

logger = get_logger("gemini")


class GeminiProcessor:
    """AI text processing using Gemini"""

    # Intent keywords for smart detection
    TRANSFORM_KEYWORDS = [
        "rewrite",
        "rephrase",
        "make",
        "convert",
        "change",
        "fix",
        "improve",
        "professional",
        "casual",
        "formal",
        "summarize",
        "expand",
        "simplify",
        "translate",
    ]

    GENERATE_KEYWORDS = [
        "write",
        "create",
        "generate",
        "based on",
        "action items",
        "summary",
        "list",
        "bullet points",
    ]

    COMMAND_KEYWORDS = ["insert", "add", "current", "today", "now"]

    def __init__(self):
        self.api_key = config.gemini_api_key

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment.\n"
                "Create .env file with: GEMINI_API_KEY=your_key_here"
            )

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        self.model_name = config.get("gemini.model", "gemini-2.0-flash-exp")
        self.model = genai.GenerativeModel(self.model_name)

        # Generation config for consistency
        self.generation_config = {
            "temperature": config.get("gemini.temperature", 0.3),
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": config.get("gemini.max_tokens", 2048),
        }

        logger.info(f"Gemini initialized with model: {self.model_name}")

    def process(
        self, voice_input: str, context: Optional[Context] = None
    ) -> Tuple[str, str]:
        """
        Process voice input with context awareness

        Args:
            voice_input: Transcribed speech
            context: Execution context (optional)

        Returns:
            Tuple[str, str]: (processed_text, action_type)
        """
        notifier.processing()

        selected_text = context.selected_text if context else None

        # Analyze intent
        intent = self._analyze_intent(voice_input, selected_text)

        logger.info(f"Intent detected: {intent}")

        # Route to appropriate handler
        if intent == "transform" and selected_text:
            return self._transform_text(voice_input, selected_text)
        elif intent == "generate" and selected_text:
            return self._generate_with_context(voice_input, selected_text)
        elif intent == "command":
            return self._execute_command(voice_input)
        else:
            return self._clean_dictation(voice_input)

    def _analyze_intent(
        self, voice_input: str, selected_text: Optional[str] = None
    ) -> str:
        """
        Determine user intent from voice input and context

        Returns:
            str: 'transform' | 'generate' | 'command' | 'dictation'
        """
        voice_lower = voice_input.lower()

        # Check for command keywords
        if any(kw in voice_lower for kw in self.COMMAND_KEYWORDS):
            return "command"

        # If text is selected, check transform vs generate
        if selected_text:
            if any(kw in voice_lower for kw in self.TRANSFORM_KEYWORDS):
                return "transform"
            elif any(kw in voice_lower for kw in self.GENERATE_KEYWORDS):
                return "generate"

        # Default to dictation
        return "dictation"

    def _transform_text(self, request: str, text: str) -> Tuple[str, str]:
        """Transform selected text according to request"""
        prompt = f"""You are a professional text editor.

ORIGINAL TEXT:
{text}

USER REQUEST:
{request}

TASK:
Transform the original text according to the user's request.
- Maintain the core meaning and key information
- Apply the requested style/tone/format changes
- Return ONLY the transformed text
- No explanations, markdown, or meta-commentary

TRANSFORMED TEXT:"""

        try:
            response = self.model.generate_content(
                prompt, generation_config=self.generation_config
            )
            result = response.text.strip()
            logger.info(f"Transformation complete: {result[:100]}...")
            return result, "transform"

        except Exception as e:
            logger.error(f"Transformation error: {e}")
            notifier.error(f"AI processing failed: {e}")
            # Fallback: return original text
            return text, "error"

    def _generate_with_context(self, request: str, context: str) -> Tuple[str, str]:
        """Generate new text using context"""
        prompt = f"""You are a writing assistant.

CONTEXT:
{context}

USER REQUEST:
{request}

TASK:
Based on the context provided, generate appropriate text that fulfills the user's request.
- Be concise and relevant
- Match the tone/style of the context
- Return ONLY the generated text
- No explanations or markdown

GENERATED TEXT:"""

        try:
            response = self.model.generate_content(
                prompt, generation_config=self.generation_config
            )
            result = response.text.strip()
            logger.info(f"Generation complete: {result[:100]}...")
            return result, "generate"

        except Exception as e:
            logger.error(f"Generation error: {e}")
            notifier.error(f"AI processing failed: {e}")
            return "", "error"

    def _execute_command(self, command: str) -> Tuple[str, str]:
        """Execute special commands (e.g., 'insert date')"""
        from datetime import datetime

        command_lower = command.lower()

        if "date" in command_lower:
            return datetime.now().strftime("%Y-%m-%d"), "command"
        elif "time" in command_lower:
            return datetime.now().strftime("%H:%M"), "command"

        # Default: treat as dictation
        return command, "command"

    def _clean_dictation(self, text: str) -> Tuple[str, str]:
        """Clean up basic dictation"""
        prompt = f"""Clean up this voice transcription:

TRANSCRIPTION:
{text}

TASK:
- Add proper punctuation and capitalization
- Fix obvious transcription errors
- Preserve the original meaning exactly
- Return ONLY the corrected text
- No explanations

CORRECTED TEXT:"""

        try:
            response = self.model.generate_content(
                prompt, generation_config=self.generation_config
            )
            result = response.text.strip()
            logger.info(f"Dictation cleaned: {result[:100]}...")
            return result, "dictation"

        except Exception as e:
            logger.error(f"Dictation cleanup error: {e}")
            notifier.error(f"AI processing failed: {e}")
            return text, "error"


# Global instance
_processor = None


def get_processor() -> GeminiProcessor:
    """Get or create Gemini processor instance"""
    global _processor
    if _processor is None:
        _processor = GeminiProcessor()
    return _processor


def process_with_gemini(voice_input: str, context: Optional[Context] = None) -> str:
    """
    Convenience function to process with Gemini

    Args:
        voice_input: Transcribed voice input
        context: Execution context (optional)

    Returns:
        str: Processed text
    """
    processor = get_processor()
    result, action_type = processor.process(voice_input, context)
    return result
