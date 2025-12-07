#!/bin/bash
# Setup Hyprland Keybindings for Swara

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HYPRLAND_CONFIG="$HOME/.config/hypr/hyprland.conf"

echo "========================================="
echo "  Swara Hyprland Keybinding Setup"
echo "========================================="
echo ""

if [ ! -f "$HYPRLAND_CONFIG" ]; then
    echo "Error: Hyprland config not found at $HYPRLAND_CONFIG"
    exit 1
fi

echo "Adding keybindings to Hyprland config..."
echo ""

# Check if keybindings already exist
if grep -q "swara-write" "$HYPRLAND_CONFIG"; then
    echo "Keybindings already exist in config. Skipping..."
else
    cat >> "$HYPRLAND_CONFIG" <<EOF

# Swara Voice Dictation Keybindings
bind = SUPER ALT, D, exec, cd $PROJECT_ROOT/src && $PROJECT_ROOT/venv/bin/python swara-write.py
bind = SUPER ALT, C, exec, cd $PROJECT_ROOT/src && $PROJECT_ROOT/venv/bin/python swara-command.py
EOF
    
    echo "✓ Keybindings added to $HYPRLAND_CONFIG"
fi

echo ""
echo "Keybindings:"
echo "  SUPER+ALT+D : Write Mode (fast dictation)"
echo "  SUPER+ALT+C : Command Mode (AI-powered)"
echo ""
echo "Reload Hyprland config to apply changes:"
echo "  hyprctl reload"
echo ""
