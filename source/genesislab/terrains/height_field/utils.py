 # File: utils.py
 # Project: height_field
 # GitHub: https://github.com/Atticlmr/genesislab
 # Created Date: Mo Dec 2025
 # Author: Li Mingrui
 # -----
 # Last Modified: Mon Dec 15 2025
 # Modified By: Li Mingrui
 # -----
 # Copyright (c) 2025 Li Mingrui, Beihang University
 # License: Apache-2.0

import functools
import numpy as np
import trimesh
from typing import Callable, List, Tuple, Any

def hf_to_mesh(dx: float = 1.0, dy: float = 1.0):
    """装饰器：2-D 高度图 → ([mesh], 全局最高点 origin)"""
    def decorator(func: Callable[[Any], np.ndarray]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            hf = func(*args, **kwargs).astype(float)
            rows, cols = hf.shape

            # 1. 顶点
            x = np.arange(cols, dtype=np.float32) * dx
            y = np.arange(rows, dtype=np.float32) * dy
            yy, xx = np.meshgrid(y, x, indexing="ij")
            vertices = np.empty((rows * cols, 3), np.float32)
            vertices[:, 0] = xx.ravel()
            vertices[:, 1] = yy.ravel()
            vertices[:, 2] = hf.ravel()

            # 2. 三角面（vectorized）
            a = np.arange(rows * cols).reshape(rows, cols)[:-1, :-1]
            b, c, d = a + 1, a + cols, a + cols + 1
            faces = np.empty((a.size * 2, 3), dtype=np.int32)
            faces[0::2] = np.column_stack((a.ravel(), c.ravel(), b.ravel()))
            faces[1::2] = np.column_stack((b.ravel(), c.ravel(), d.ravel()))

            mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)

            # 3. 原点：直接全局最高
            max_idx = np.argmax(hf)          # 扁平索引
            iy, ix = np.unravel_index(max_idx, hf.shape)
            origin = np.array([xx[iy, ix], yy[iy, ix], hf[iy, ix]], dtype=np.float32)

            return [mesh], origin
        return wrapper
    return decorator