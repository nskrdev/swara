# Swara (स्वर) - Intelligent Voice Dictation for Linux

**Swara** (स्वर - "voice/sound/tone" in Sanskrit) is an intelligent voice dictation tool for Linux with context awareness and AI processing.

## Features

- **Two Modes**:
  - **Write Mode**: Fast, accurate transcription
  - **Command Mode**: AI-powered text transformation and generation
  
- **Context Awareness**: Automatically detects and uses selected text
- **Privacy-Focused**: Local Whisper.cpp transcription, optional cloud AI
- **Smart Text Injection**: Multiple strategies with automatic fallback
- **Wayland Native**: Built for modern Linux desktops (Hyprland)

## Quick Start

### Prerequisites

- **OS**: Linux with Wayland (tested on Hyprland)
- **Python**: 3.10+ 
- **System packages**:
  ```bash
  sudo pacman -S ydotool wl-clipboard libnotify python python-pip git make gcc
  ```

### Installation

1. **Clone the repository**:
   ```bash
   cd ~/Projects
   git clone <your-repo-url> swara
   cd swara
   ```

2. **Run installation script**:
   ```bash
   bash scripts/install.sh
   ```

3. **Configure Gemini API**:
   ```bash
   nano .env
   # Add: GEMINI_API_KEY=your_key_here
   ```
   Get your key from: https://makersuite.google.com/app/apikey

4. **Setup keybindings**:
   ```bash
   bash scripts/setup-keybindings.sh
   hyprctl reload
   ```

### Usage

**Write Mode** (`SUPER+ALT+D`):
- Press keybinding → Speak (5 seconds) → Auto-stop
- Text appears in your active application
- Great for: Quick notes, messages, dictation

**Command Mode** (`SUPER+ALT+C`):
- Select text → Press keybinding → Give command
- Examples:
  - "Make this more professional"
  - "Fix grammar"
  - "Summarize this"
  - "Write a reply based on this"

## Documentation

- **[Configuration](./config/default.yaml)**: All configurable settings
- **[Spike Tests](./tests/spike/)**: Manual tests for validation

## Architecture

```
Write Mode Flow:
Record → Transcribe → Inject

Command Mode Flow:
Capture Context → Record → Transcribe → Gemini AI → Inject
```

**Core Technologies**:
- **Speech-to-Text**: Whisper.cpp (local, private)
- **AI**: Google Gemini 2.0 (Command Mode only)
- **Text Injection**: ydotool (Wayland-native)
- **Context Capture**: wl-clipboard

## Testing

Run spike tests to validate setup:

```bash
source venv/bin/activate

# Test context capture
python3 tests/spike/test_selection.py

# Test text injection
python3 tests/spike/test_ydotool.py
```

## Troubleshooting

### Common Issues

**"Permission denied" when typing**:
```bash
# Add user to input group and reboot
sudo usermod -aG input $USER
```

**"ydotool not found"**:
```bash
sudo pacman -S ydotool
```

**"Whisper model not found"**:
```bash
cd ~/whisper.cpp
bash ./models/download-ggml-model.sh base
```

**"No text appears after dictation"**:
```bash
# Make sure ydotoold is running
systemctl --user start ydotoold
systemctl --user enable ydotoold
```

For more troubleshooting, check the logs:
```bash
tail -f logs/swara.log
```

## Configuration

Edit `config/default.yaml` to customize:

```yaml
# Audio settings
audio:
  recording_duration: 5  # Recording duration in seconds
  max_duration: 30
  beep_on_start: true

# Punctuation (disabled by default for speed)
punctuation:
  enabled: false

# AI settings
gemini:
  temperature: 0.3
  model: "gemini-2.0-flash-exp"

# Output settings
output:
  typing_delay: 0.01
  injection_strategy: "auto"
```

## Privacy

- **Write Mode**: 100% local processing (audio never leaves your machine)
- **Command Mode**: Sends transcribed text + context to Gemini API
- **Logs**: Stored locally at `logs/swara.log`

## License

MIT License - see [LICENSE](./LICENSE) file

## Acknowledgments

- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) - Fast local transcription
- [DeepMultilingualPunctuation](https://github.com/oliverguhr/deepmultilingualpunctuation) - Punctuation restoration
- [Google Gemini](https://ai.google.dev/) - AI processing
- [ydotool](https://github.com/ReimuNotMoe/ydotool) - Wayland input simulation

## Roadmap

- [ ] Custom GTK4 status window
- [ ] Voice Activity Detection (VAD)
- [ ] Multiple Whisper model support
- [ ] Local AI option (llama.cpp)
- [ ] Vim/Neovim plugin
- [ ] Multi-language support

## Support

For issues and questions, please open an issue on GitHub.

---

Made for the Linux voice dictation community
