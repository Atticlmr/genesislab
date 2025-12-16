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

def hf_to_mesh(dx: float = 1.0, dy: float = 1.0, seed: int|None = None):
    """装饰器：2-D 高度图 → ([mesh], 全局最高点 origin)
    
    Args:
        dx: x方向网格间距
        dy: y方向网格间距
        seed: 随机数种子，如果为None则使用配置文件中的seed
    """
    def decorator(func: Callable[[Any], np.ndarray]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 从配置对象中获取seed（如果存在）
            cfg = kwargs.get('cfg', None)
            if cfg is not None and hasattr(cfg, 'seed') and seed is None:
                actual_seed = cfg.seed
            else:
                actual_seed = seed
            
            # 保存当前全局随机状态，避免污染其他随机数生成
            original_state = np.random.get_state()
            
            # 设置随机数种子
            if actual_seed is not None:
                np.random.seed(actual_seed)
            
            try:
                # 执行函数
                hf = func(*args, **kwargs).astype(float)
            finally:
                # 恢复原始随机状态，确保不影响其他代码
                np.random.set_state(original_state)
            
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