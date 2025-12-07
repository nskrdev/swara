#!/usr/bin/env python3
"""
Swara - Command Mode (AI-Powered Processing)

Intelligent processing with context awareness and AI.
Flow: Capture Context → Record → Transcribe → Gemini → Inject
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
    capture_context,
    restore_context,
    process_with_gemini,
    inject_text,
    validate_system_dependencies,
    check_user_in_input_group,
)

logger = get_logger("command")


def main():
    """Main entry point for Command Mode"""

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
        logger.info("=== Swara Command Mode Started ===")

        # Step 1: Capture context
        notifier.capturing_context()
        context = capture_context()

        if context.selected_text:
            logger.info(f"Context captured: {len(context.selected_text)} chars")
        else:
            logger.info("No selection found")

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
                from swara_core import config

                recording_duration = config.get("audio.recording_duration", 5)
                logger.info(f"Recording for {recording_duration}s...")
                time.sleep(recording_duration)
        except (EOFError, OSError):
            # No stdin available, use fixed duration
            from swara_core import config

            recording_duration = config.get("audio.recording_duration", 5)
            logger.info(f"No terminal, recording for {recording_duration}s...")
            time.sleep(recording_duration)

        audio_file = recorder.stop_recording()

        if not audio_file:
            logger.error("Recording failed")
            notifier.error("Recording failed", critical=True)
            return

        # Step 3: Transcribe
        transcription = transcribe(audio_file)

        if not transcription:
            logger.warning("Empty transcription")
            notifier.error("No speech detected")
            return

        logger.info(f"Transcribed: {transcription}")

        # Step 4: Process with Gemini
        result = process_with_gemini(transcription, context)

        if not result:
            logger.error("AI processing failed")
            notifier.error("AI processing failed")
            return

        logger.info(f"AI result: {result}")

        # Step 5: Inject text
        success = inject_text(result, context)

        if success:
            notifier.success(result)
            logger.info("=== Command Mode Complete ===")
        else:
            logger.error("Text injection failed")

        # Step 6: Restore context
        restore_context()

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        notifier.error("Cancelled")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Command mode error: {e}", exc_info=True)
        notifier.error(f"Error: {str(e)}", critical=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
