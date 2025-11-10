#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
DOWNLOADS_DIR = BASE_DIR / "downloads"
GENESIS_REPO_URL = "https://github.com/Genesis-Embodied-AI/Genesis.git"
GENESIS_SRC_DIR = DOWNLOADS_DIR / "Genesis"
VENV_NAME = "env_genesis"
PYTHON_VERSION = "3.11"

def run_cmd(cmd, cwd=None, env=None):
    print(f"▶️ Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, env=env)
    if result.returncode != 0:
        print("❌ Command failed.")
        sys.exit(1)

def is_tool_installed(name):
    return shutil.which(name) is not None

def clone_genesis():
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    if GENESIS_SRC_DIR.exists():
        print(f"📁 Genesis already cloned at {GENESIS_SRC_DIR}. Skipping.")
    else:
        print("⬇️ Cloning Genesis repository (with submodules)...")
        run_cmd(["git", "clone", GENESIS_REPO_URL, str(GENESIS_SRC_DIR)])

def main():
    clone_genesis()

    # 优先使用 uv，其次 conda
    if is_tool_installed("uv"):
        use_uv = True
        use_conda = False
    elif is_tool_installed("conda"):
        use_uv = False
        use_conda = True
    else:
        print("⚠️ Neither 'uv' nor 'conda' found. Installing uv automatically...")
        # 安装 uv via curl (官方推荐方式)
        run_cmd(["curl", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"], shell=True)
        # 重新加载 PATH（简单处理：直接调用绝对路径或假设已生效）
        if not is_tool_installed("uv"):
            # 尝试从常见位置加载
            uv_path = Path.home() / ".cargo" / "bin" / "uv"
            if uv_path.exists():
                os.environ["PATH"] = f"{uv_path.parent}:{os.environ['PATH']}"
            else:
                print("❌ Failed to install or locate 'uv'.")
                sys.exit(1)
        use_uv = True
        use_conda = False

    venv_path = BASE_DIR / VENV_NAME

    if use_uv:
        print("✅ Using uv to manage environment.")
        run_cmd(["uv", "venv", str(venv_path), "--python", PYTHON_VERSION])
        run_cmd([
            "uv", "pip", "install",
            "--cache-dir", str(DOWNLOADS_DIR / "pip-cache"),
            "-e", str(GENESIS_SRC_DIR)
        ], env={**os.environ, "VIRTUAL_ENV": str(venv_path)})

    elif use_conda:
        print("✅ Using conda to manage environment.")
        if not (venv_path / "conda-meta").exists():
            run_cmd(["conda", "create", "-y", "-p", str(venv_path), f"python={PYTHON_VERSION}"])
        python_bin = venv_path / "bin" / "python"
        run_cmd([str(python_bin), "-m", "pip", "install", "--cache-dir", str(DOWNLOADS_DIR / "pip-cache"), "-e", str(GENESIS_SRC_DIR)])

    print(f"\n🎉 Genesis installed in editable mode!")
    print(f"📦 Source: {GENESIS_SRC_DIR}")
    print(f"🐍 Virtual environment: {venv_path}")
    print(f"💡 Activate with: source {venv_path}/bin/activate")

if __name__ == "__main__":
    main()