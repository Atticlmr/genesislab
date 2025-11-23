#!/usr/bin/env python3
import os
import subprocess
import shutil
import sys
import json
import urllib.request
from pathlib import Path

BASE_DIR      = Path(__file__).parent.parent.resolve()
DOWNLOADS_DIR = BASE_DIR / "downloads"
VENV_PATH     = BASE_DIR / "env_genesis"
PYTHON_VER    = "3.11"

# GitHub 仓库
REPO_SLUG     = "Atticlmr/Genesis"

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

def github_api(url: str) -> dict:
    """GET GitHub API JSON，无 token 限速 60/h"""
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def download_file(url: str, dst: Path):
    """流式下载，显示简单进度"""
    print(f"⬇️  Downloading {url}")
    urllib.request.urlretrieve(url, dst)
    print(f"✅  Saved to {dst}")

# ---------- 主流程 ----------
def main() -> None:
    DOWNLOADS_DIR.mkdir(exist_ok=True)

    # 1. 获取最新 release
    latest = github_api(f"https://api.github.com/repos/{REPO_SLUG}/releases/latest")
    tag    = latest["tag_name"]
    print(f"📦  Latest release: {tag}")

    # 2. 找到第一个 .whl 资源
    wheels = [a for a in latest["assets"] if a["name"].endswith(".whl")]
    if not wheels:
        print("❌  No wheel file found in release!")
        sys.exit(1)
    wheel_url = wheels[0]["browser_download_url"]
    wheel_file = DOWNLOADS_DIR / wheels[0]["name"]

    # 3. 下载（如已存在则跳过）
    if wheel_file.exists():
        print(f"📁  Wheel already exists: {wheel_file}")
    else:
        download_file(wheel_url, wheel_file)

    # 4. 确保 uv 存在
    ensure_uv()

    # 5. 创建虚拟环境
    run(["uv", "venv", str(VENV_PATH), "--python", PYTHON_VER])

    # 6. 安装 wheel
    os.environ["VIRTUAL_ENV"] = str(VENV_PATH)
    run([
        "uv", "pip", "install",
        "--cache-dir", str(DOWNLOADS_DIR / "pip-cache"),
        str(wheel_file)
    ])

    print("\n🎉  Genesis wheel installed!")
    print(f"📦  Wheel  : {wheel_file}")
    print(f"🐍  Venv   : {VENV_PATH}")
    print(f"💡  Activate: source {VENV_PATH}/bin/activate")

if __name__ == "__main__":
    main()