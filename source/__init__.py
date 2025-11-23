
"""
GenesisLab: An Isaac-Lab-like robotics simulation framework.
"""
from __future__ import annotations

try:
    from importlib.metadata import version, PackageNotFoundError
    __version__ = version("genesislab")   # 与 pyproject.toml 同步
except PackageNotFoundError:              # editable 模式未安装时
    __version__ = "0.0.1"

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())