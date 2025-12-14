#!/usr/bin/env python3
import os
import subprocess
import shutil
import sys
import urllib.request
from pathlib import Path

BASE_DIR      = Path(__file__).parent.parent.resolve()
DOWNLOADS_DIR = BASE_DIR / "downloads"
VENV_PATH     = BASE_DIR / "env_genesis"
PYTHON_VER    = "3.11"

# GitHub 仓库
REPO_URL      = "https://github.com/Atticlmr/Genesis.git"
CLONE_DIR     = DOWNLOADS_DIR / "Genesis"          # 仓库存放路径

# ---------- 工具 ----------
def run(cmd: list[str], cwd=None) -> None:
    print(f"▶️  {' '.join(cmd)}")
    if (code := subprocess.run(cmd, cwd=cwd).returncode) != 0:
        print("❌  Command failed.")
        sys.exit(code)

def ensure_uv() -> None:
    if shutil.which("uv"):
        return
    print("⚠️  uv not found, installing via official script…")
    install_script = "https://astral.sh/uv/install.sh"
    run(["curl", "-LsSf", install_script, "-o", "/tmp/uv_install.sh"])
    run(["sh", "/tmp/uv_install.sh"])
    cargo_bin = Path.home() / ".cargo" / "bin"
    os.environ["PATH"] = f"{cargo_bin}{os.pathsep}{os.environ['PATH']}"
    if not shutil.which("uv"):
        print("❌  still cannot find uv.")
        sys.exit(1)

# ---------- 主流程 ----------
def main() -> None:
    DOWNLOADS_DIR.mkdir(exist_ok=True)

    # 1. 克隆仓库（如已存在则先拉最新代码）
    if CLONE_DIR.exists():
        print(f"📁  Repo exists, pulling latest changes…")
        run(["git", "-C", str(CLONE_DIR), "pull", "--ff-only"])
    else:
        print(f"⬇️  Cloning repo…")
        run(["git", "clone", REPO_URL, str(CLONE_DIR)])

    # 2. 确保 uv 存在
    ensure_uv()

    # 3. 创建虚拟环境
    run(["uv", "venv", str(VENV_PATH), "--python", PYTHON_VER])

    # 4. 可编辑安装
    os.environ["VIRTUAL_ENV"] = str(VENV_PATH)
    run([
        "uv", "pip", "install",
        "--cache-dir", str(DOWNLOADS_DIR / "pip-cache"),
        "-e", str(CLONE_DIR)
    ])

    print("\n🎉  Genesis installed in editable mode!")
    print(f"📁  Repo   : {CLONE_DIR}")
    print(f"🐍  Venv   : {VENV_PATH}")
    print(f"💡  Activate: source {VENV_PATH}/bin/activate")

if __name__ == "__main__":
    main()