#!/bin/bash
# Swara Installation Script

set -e  # Exit on error

echo "========================================="
echo "  Swara Installation Script"
echo "========================================="
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Step 1: Check system dependencies
echo "Step 1: Checking system dependencies..."
echo ""

MISSING_DEPS=()

check_command() {
    if command -v "$1" &> /dev/null; then
        print_status "$1 found"
        return 0
    else
        print_error "$1 not found"
        MISSING_DEPS+=("$1")
        return 1
    fi
}

check_command "python3"
check_command "pip"
check_command "git"
check_command "make"
check_command "gcc" || check_command "clang"
check_command "wl-paste"
check_command "wl-copy"
check_command "notify-send"
check_command "paplay" || check_command "aplay"

# Check ydotool
if ! check_command "ydotool"; then
    echo ""
    print_warning "ydotool is required but not installed"
    echo "Install with: sudo pacman -S ydotool"
    echo "Then add user to input group: sudo usermod -aG input \$USER"
    echo "And reboot or re-login"
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    print_error "Missing dependencies: ${MISSING_DEPS[*]}"
    echo "Please install them and run this script again."
    exit 1
fi

echo ""

# Step 2: Check user in input group
echo "Step 2: Checking user permissions..."
if groups | grep -q "input"; then
    print_status "User is in 'input' group"
else
    print_error "User is NOT in 'input' group"
    echo ""
    echo "Run: sudo usermod -aG input \$USER"
    echo "Then reboot or re-login for changes to take effect"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# Step 3: Create virtual environment
echo "Step 3: Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

echo ""

# Step 4: Install Python dependencies
echo "Step 4: Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
print_status "Python dependencies installed"

echo ""

# Step 5: Download and compile whisper.cpp
echo "Step 5: Setting up Whisper.cpp..."

WHISPER_DIR="$HOME/whisper.cpp"

if [ -d "$WHISPER_DIR" ]; then
    print_status "Whisper.cpp already installed at $WHISPER_DIR"
else
    echo "Downloading whisper.cpp..."
    cd "$HOME"
    git clone https://github.com/ggerganov/whisper.cpp
    cd whisper.cpp
    
    echo "Compiling whisper.cpp..."
    make
    
    print_status "Whisper.cpp compiled successfully"
fi

echo ""

# Step 6: Download Whisper model
echo "Step 6: Downloading Whisper base model..."

MODEL_FILE="$WHISPER_DIR/models/ggml-base.bin"

if [ -f "$MODEL_FILE" ]; then
    print_status "Whisper base model already downloaded"
else
    cd "$WHISPER_DIR"
    bash ./models/download-ggml-model.sh base
    print_status "Whisper base model downloaded"
fi

echo ""

# Step 7: Create .env file
echo "Step 7: Setting up environment..."
cd "$PROJECT_ROOT"

if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning ".env file created - EDIT IT to add your GEMINI_API_KEY"
    echo "Get your API key from: https://makersuite.google.com/app/apikey"
else
    print_status ".env file already exists"
fi

echo ""

# Step 8: Create log directory
echo "Step 8: Creating directories..."
mkdir -p logs models
print_status "Directories created"

echo ""

# Step 9: Setup ydotoold service
echo "Step 9: Setting up ydotoold service..."
mkdir -p ~/.config/systemd/user/

cat > ~/.config/systemd/user/ydotoold.service <<'EOF'
[Unit]
Description=ydotool daemon
Documentation=https://github.com/ReimuNotMoe/ydotool

[Service]
Type=simple
ExecStart=/usr/bin/ydotoold
Restart=on-failure

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now ydotoold.service

if systemctl --user is-active --quiet ydotoold.service; then
    print_status "ydotoold service started and enabled"
else
    print_warning "ydotoold service setup - please check: systemctl --user status ydotoold"
fi

echo ""

# Step 10: Test installation
echo "Step 10: Testing installation..."

echo "Testing Python imports..."
python3 -c "import swara_core; print('✓ swara_core imports successfully')" 2>&1 | grep -q "✓" && print_status "Core library OK" || print_error "Core library import failed"

echo "Testing Whisper.cpp..."
if [ -f "$WHISPER_DIR/main" ]; then
    print_status "Whisper.cpp executable OK"
else
    print_error "Whisper.cpp executable not found"
fi

echo ""

# Summary
echo "========================================="
echo "  Installation Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env file and add your GEMINI_API_KEY:"
echo "   nano .env"
echo ""
echo "2. Setup Hyprland keybindings:"
echo "   bash scripts/setup-keybindings.sh"
echo ""
echo "3. Test the installation:"
echo "   source venv/bin/activate"
echo "   python3 src/swara-write.py"
echo ""
echo "Keybindings (after setup):"
echo "  SUPER+ALT+D : Write Mode (fast dictation)"
echo "  SUPER+ALT+C : Command Mode (AI-powered)"
echo ""
