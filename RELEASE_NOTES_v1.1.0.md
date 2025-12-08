# Swara v1.1.0 - Initial Public Release

## Summary

Initial public release of **Swara** (స్వర - "voice/sound/tone" in Telugu), an intelligent voice dictation tool for Linux with context awareness and AI processing.

## Project Overview

Swara is a privacy-focused voice dictation tool designed for Linux systems running Wayland. It combines local speech recognition with optional cloud AI processing to provide two powerful modes of operation:

- **Write Mode**: Fast, accurate transcription using local Whisper.cpp
- **Command Mode**: AI-powered text transformation and generation using Google Gemini

## Key Features

- 🎤 **Two Modes**: Write mode for fast transcription, Command mode for AI-powered text transformation
- 🧠 **Context Awareness**: Automatically detects and uses selected text
- 🔒 **Privacy-Focused**: Local Whisper.cpp transcription, optional cloud AI
- 💉 **Smart Text Injection**: Multiple strategies with automatic fallback
- 🖥️ **Wayland Native**: Built for modern Linux desktops (tested on Hyprland)

## Technology Stack

- **Language**: Python 3.10+
- **License**: MIT License
- **Speech-to-Text**: Whisper.cpp (local, private)
- **AI**: Google Gemini 2.5 Flash
- **Text Injection**: ydotool (Wayland-native)
- **Context Capture**: wl-clipboard

## Core Components

### Python Modules

- `swara-write.py` - Write mode entry point (fast transcription)
- `swara-command.py` - Command mode entry point (AI-powered)
- `swara_core/audio.py` - Audio recording and processing
- `swara_core/transcribe.py` - Whisper.cpp integration
- `swara_core/gemini.py` - Google Gemini AI integration
- `swara_core/inject.py` - Text injection with multiple strategies
- `swara_core/context.py` - Context capture and management
- `swara_core/config.py` - Configuration management
- `swara_core/notify.py` - Desktop notifications
- `swara_core/punctuation.py` - Punctuation restoration
- `swara_core/utils.py` - Utility functions

### Installation Scripts

- `scripts/install.sh` - Automated installation and setup
- `scripts/setup-keybindings.sh` - Hyprland keybinding configuration

### Configuration

- `config/default.yaml` - Default configuration settings
- `.env.example` - Environment variable template

## Notable Changes in v1.1.0

- Switched to gemini-2.5-flash model (latest stable, verified working)
- Improved error handling for rate limit errors (429)
- Added user-friendly error messages for rate limits
- Better fallback behavior when API fails
- Listed available models in config comments

## System Requirements

- **OS**: Linux with Wayland (tested on Hyprland)
- **Python**: 3.10+
- **System packages**: ydotool, wl-clipboard, libnotify, python, python-pip, git, make, gcc

## Installation

See [README.md](./README.md) for detailed installation instructions.

Quick start:
```bash
cd ~/Projects
git clone https://github.com/nskrdev/swara.git swara
cd swara
bash scripts/install.sh
```

## Usage

- **Write Mode** (`SUPER+ALT+D`): Quick voice-to-text dictation
- **Command Mode** (`SUPER+ALT+C`): AI-powered text transformation

## Testing

Spike tests are included for manual validation:
- `tests/spike/test_selection.py` - Test context capture
- `tests/spike/test_ydotool.py` - Test text injection

## Privacy

- **Write Mode**: 100% local processing (audio never leaves your machine)
- **Command Mode**: Sends transcribed text + context to Gemini API
- **Logs**: Stored locally at `logs/swara.log`

## Dependencies

Key Python dependencies:
- PyAudio >= 0.2.13
- deepmultilingualpunctuation >= 1.0.1
- torch >= 2.0.0
- google-generativeai >= 0.3.0
- pyyaml >= 6.0
- python-dotenv >= 1.0.0

See [requirements.txt](./requirements.txt) for complete list.

## Acknowledgments

- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) - Fast local transcription
- [DeepMultilingualPunctuation](https://github.com/oliverguhr/deepmultilingualpunctuation) - Punctuation restoration
- [Google Gemini](https://ai.google.dev/) - AI processing
- [ydotool](https://github.com/ReimuNotMoe/ydotool) - Wayland input simulation

## Roadmap

Future enhancements planned:
- Custom GTK4 status window
- Voice Activity Detection (VAD)
- Multiple Whisper model support
- Local AI option (llama.cpp)
- Vim/Neovim plugin
- Multi-language support

## Support

For issues and questions, please open an issue on GitHub: https://github.com/nskrdev/swara/issues

---

Made for the Linux voice dictation community
