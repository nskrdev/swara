"""
Swara Core Library - Audio Recording Module

Handles audio recording from microphone.
"""

import pyaudio
import wave
import threading
import time
from typing import Optional
from .utils import get_logger, get_temp_audio_file
from .config import config
from .notify import notifier

logger = get_logger("audio")


class AudioRecorder:
    """Audio recording manager"""

    def __init__(self):
        self.sample_rate = config.get("audio.sample_rate", 16000)
        self.channels = config.get("audio.channels", 1)
        self.chunk_size = config.get("audio.chunk_size", 1024)
        self.max_duration = config.get("audio.max_duration", 30)
        self.beep_on_start = config.get("audio.beep_on_start", True)
        self.beep_on_stop = config.get("audio.beep_on_stop", True)

        self.is_recording = False
        self.frames = []
        self.audio_file = None

    def start_recording(self) -> str:
        """
        Start recording audio

        Returns:
            str: Path to the audio file that will be created
        """
        if self.is_recording:
            logger.warning("Already recording")
            return None

        self.audio_file = get_temp_audio_file()
        self.frames = []
        self.is_recording = True

        # Audio feedback
        if self.beep_on_start:
            self._play_beep("start")

        # Show notification
        notifier.recording()

        # Start recording in background thread
        thread = threading.Thread(target=self._record_thread, daemon=True)
        thread.start()

        logger.info(f"Recording started: {self.audio_file}")
        return self.audio_file

    def stop_recording(self) -> Optional[str]:
        """
        Stop recording and save to file

        Returns:
            str: Path to the saved audio file, or None if not recording
        """
        if not self.is_recording:
            logger.warning("Not currently recording")
            return None

        self.is_recording = False

        # Wait a bit for thread to finish
        time.sleep(0.2)

        # Audio feedback
        if self.beep_on_stop:
            self._play_beep("stop")

        # Save to file
        if self.frames:
            self._save_to_file()
            logger.info(f"Recording stopped: {self.audio_file}")
            return self.audio_file
        else:
            logger.warning("No audio recorded")
            return None

    def _record_thread(self):
        """Background thread for recording"""
        p = pyaudio.PyAudio()

        try:
            stream = p.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
            )

            start_time = time.time()

            while self.is_recording:
                # Check timeout
                if time.time() - start_time > self.max_duration:
                    logger.info(f"Auto-stopping after {self.max_duration}s")
                    self.is_recording = False
                    break

                try:
                    data = stream.read(self.chunk_size, exception_on_overflow=False)
                    self.frames.append(data)
                except Exception as e:
                    logger.error(f"Error reading audio: {e}")
                    break

            stream.stop_stream()
            stream.close()

        except Exception as e:
            logger.error(f"Recording error: {e}")
            self.is_recording = False
        finally:
            p.terminate()

    def _save_to_file(self):
        """Save recorded frames to WAV file"""
        try:
            wf = wave.open(self.audio_file, "wb")
            wf.setnchannels(self.channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b"".join(self.frames))
            wf.close()
            logger.debug(f"Audio saved: {self.audio_file}")
        except Exception as e:
            logger.error(f"Failed to save audio: {e}")
            raise

    def _play_beep(self, beep_type: str):
        """
        Play audio feedback beep

        Args:
            beep_type: 'start' or 'stop'
        """
        import subprocess

        # System sound files (freedesktop standard)
        beep_files = {
            "start": "/usr/share/sounds/freedesktop/stereo/message.oga",
            "stop": "/usr/share/sounds/freedesktop/stereo/complete.oga",
        }

        beep_file = beep_files.get(beep_type)

        if beep_file:
            try:
                # Try paplay first (PulseAudio/PipeWire)
                subprocess.Popen(
                    ["paplay", beep_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except FileNotFoundError:
                # Fallback to aplay (ALSA)
                try:
                    subprocess.Popen(
                        ["aplay", beep_file],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except FileNotFoundError:
                    logger.debug("No audio player found for beep")


def record_audio() -> str:
    """
    Simple function to record audio (blocking until stopped)
    This is a convenience function for simple use cases.

    Returns:
        str: Path to recorded audio file
    """
    recorder = AudioRecorder()
    audio_file = recorder.start_recording()

    # Wait for user to finish speaking
    # In real usage, this will be controlled by keybinding
    # For now, we'll use a simple approach
    logger.info("Recording... (will auto-stop after max duration)")

    while recorder.is_recording:
        time.sleep(0.1)

    return audio_file
