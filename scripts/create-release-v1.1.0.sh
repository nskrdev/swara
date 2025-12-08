#!/bin/bash
# Script to create GitHub release v1.1.0 for Swara
# This script uses GitHub CLI (gh) to create a release
# Prerequisites: gh CLI must be installed and authenticated

set -e

REPO="nskrdev/swara"
TAG="v1.1.0"
TITLE="v1.1.0"
TARGET_BRANCH="main"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Creating GitHub Release for Swara v1.1.0${NC}"
echo "============================================"
echo ""

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed${NC}"
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if gh is authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI is not authenticated${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

# Check if tag exists
if ! git rev-parse "$TAG" &> /dev/null; then
    echo -e "${RED}Error: Tag $TAG does not exist${NC}"
    exit 1
fi

echo "Repository: $REPO"
echo "Tag: $TAG"
echo "Target Branch: $TARGET_BRANCH"
echo ""

# Create release notes content
RELEASE_NOTES=$(cat <<'EOF'
Initial public release of **Swara** (స్వర - "voice/sound/tone" in Telugu), an intelligent voice dictation tool for Linux with context awareness and AI processing.

## Project Overview

Swara is a privacy-focused voice dictation tool designed for Linux systems running Wayland. It combines local speech recognition with optional cloud AI processing to provide two powerful modes of operation.

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

## Notable Changes in v1.1.0

- Switched to gemini-2.5-flash model (latest stable, verified working)
- Improved error handling for rate limit errors (429)
- Added user-friendly error messages for rate limits
- Better fallback behavior when API fails
- Listed available models in config comments

## Installation

```bash
cd ~/Projects
git clone https://github.com/nskrdev/swara.git swara
cd swara
bash scripts/install.sh
```

For detailed installation instructions, see the [README](./README.md).

## Usage

- **Write Mode** (`SUPER+ALT+D`): Quick voice-to-text dictation
- **Command Mode** (`SUPER+ALT+C`): AI-powered text transformation

## System Requirements

- **OS**: Linux with Wayland (tested on Hyprland)
- **Python**: 3.10+
- **System packages**: ydotool, wl-clipboard, libnotify, python, python-pip, git, make, gcc

## Privacy

- **Write Mode**: 100% local processing (audio never leaves your machine)
- **Command Mode**: Sends transcribed text + context to Gemini API
- **Logs**: Stored locally at `logs/swara.log`

## Support

For issues and questions, please open an issue on [GitHub](https://github.com/nskrdev/swara/issues).

---

Made for the Linux voice dictation community
EOF
)

echo -e "${BLUE}Creating release...${NC}"
echo ""

# Create the release using gh CLI
gh release create "$TAG" \
    --repo "$REPO" \
    --title "$TITLE" \
    --notes "$RELEASE_NOTES" \
    --target "$TARGET_BRANCH" \
    --generate-notes \
    --latest

RELEASE_EXIT_CODE=$?

if [ $RELEASE_EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Release $TAG created successfully!${NC}"
    echo ""
    echo "View the release at: https://github.com/$REPO/releases/tag/$TAG"
else
    echo ""
    echo -e "${RED}✗ Failed to create release${NC}"
    exit 1
fi
