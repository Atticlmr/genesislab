#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETUP_GENESIS_SCRIPT="$SCRIPT_DIR/setup/setup_genesis.py"
VENV_PATH="$SCRIPT_DIR/../env_genesis/bin/activate"

for cmd in git python3; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "❌ '$cmd' is required but not installed. Please run:"
        echo "   sudo apt update && sudo apt install -y git python3 python3-pip"
        exit 1
    fi
done

chmod +x "$SETUP_GENESIS_SCRIPT"
echo "🚀 Starting Genesis installation on Ubuntu..."
python3 "$SETUP_GENESIS_SCRIPT"

echo
echo "✅ Installation complete! Entering Genesis virtual environment…"
echo "   (exit 或者 Ctrl-D 可退出)"
exec bash --rcfile <(echo "source $VENV_PATH; PS1='(genesis) \w \$ '")
