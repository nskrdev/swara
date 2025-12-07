#!/usr/bin/env python3
"""
Swara - Write Mode (Fast Dictation)

Fast, accurate transcription with punctuation restoration.
Flow: Record → Transcribe → Add Punctuation → Inject
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from swara_core import (
    get_logger,
    notifier,
    AudioRecorder,
    transcribe,
    restore_punctuation,
    inject_text,
    validate_system_dependencies,
    check_user_in_input_group,
    capture_context,
    restore_context,
    config,
)

logger = get_logger("write")


def main():
    """Main entry point for Write Mode"""

    # Validate system
    deps = validate_system_dependencies()
    missing = [name for name, status in deps.items() if not status]

    if missing:
        error_msg = f"Missing dependencies: {', '.join(missing)}"
        logger.error(error_msg)
        notifier.error(error_msg, critical=True)
        sys.exit(1)

    if not check_user_in_input_group():
        error_msg = "User not in 'input' group. Run: sudo usermod -aG input $USER"
        logger.error(error_msg)
        notifier.error(error_msg, critical=True)
        sys.exit(1)

    try:
        logger.info("=== Swara Write Mode Started ===")

        # Step 1: Capture context (for selection replacement)
        context = capture_context()

        # Step 2: Record audio
        notifier.recording()
        recorder = AudioRecorder()
        audio_file = recorder.start_recording()

        # Wait for recording to complete
        # Check if we're in terminal mode or keybinding mode
        import sys
        import time

        try:
            if sys.stdin.isatty():
                # Terminal mode: wait for Enter key
                print("\nRecording... Press ENTER to stop (or wait 30s for auto-stop)")
                input()
            else:
                # Keybinding mode: record for fixed duration
                recording_duration = config.get("audio.recording_duration", 5)
                logger.info(f"Recording for {recording_duration}s...")
                time.sleep(recording_duration)
        except (EOFError, OSError):
            # No stdin available, use fixed duration
            recording_duration = config.get("audio.recording_duration", 5)
            logger.info(f"No terminal, recording for {recording_duration}s...")
            time.sleep(recording_duration)

        audio_file = recorder.stop_recording()

        if not audio_file:
            logger.error("Recording failed")
            notifier.error("Recording failed", critical=True)
            return

        # Step 3: Transcribe
        text = transcribe(audio_file)

        if not text:
            logger.warning("Empty transcription")
            notifier.error("No speech detected")
            return

        logger.info(f"Transcribed: {text}")

        # Step 4: Restore punctuation
        formatted = restore_punctuation(text)

        # Step 5: Inject text
        success = inject_text(formatted, context)

        if success:
            notifier.success(formatted)
            logger.info("=== Write Mode Complete ===")
        else:
            logger.error("Text injection failed")

        # Step 6: Restore context
        restore_context()

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        notifier.error("Cancelled")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Write mode error: {e}", exc_info=True)
        notifier.error(f"Error: {str(e)}", critical=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
