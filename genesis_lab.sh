#!/bin/bash

set -e  # 出错立即退出

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETUP_SCRIPT="$SCRIPT_DIR/setup/setup_genesis.py"

# 检查必要工具
for cmd in git python3; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "❌ '$cmd' is required but not installed. Please run:"
        echo "   sudo apt update && sudo apt install -y git python3 python3-pip"
        exit 1
    fi
done

# 确保脚本可执行
chmod +x "$SETUP_SCRIPT"

echo "🚀 Starting Genesis installation on Ubuntu..."
python3 "$SETUP_SCRIPT"

echo
echo "✅ Installation complete!"
echo "To use Genesis, run:"
echo "   source $SCRIPT_DIR/genesis/bin/activate"