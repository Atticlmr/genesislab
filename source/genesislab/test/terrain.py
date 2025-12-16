#!/usr/bin/env python3
"""
独立脚本：生成全部地形并导出 .stl
"""
import pathlib
import trimesh
from typing import Tuple

# 只在这里才导入（保证 hf_terrains 已绑定函数）
from genesislab.terrains.height_field import hf_terrains, hf_terrians_cfg as cfg

OUT_DIR = pathlib.Path("/home/li/Desktop/terrain_stl")
OUT_DIR.mkdir(exist_ok=True)
TERRAIN_SIZE = (10.0, 10.0)

# 定义地形参数池，包含所有必需参数
TERRAIN_POOL = [
    # HfRandomUniformTerrainCfg
    (cfg.HfRandomUniformTerrainCfg, "hf_random_uniform_terrain",
     {
         "size": TERRAIN_SIZE,
         "border_width": 0.0,
         "horizontal_scale": 0.1,
         "vertical_scale": 0.005,
         "slope_threshold": None,
         "noise_range": (0.05, 0.25),
         "noise_step": 0.01
     }),
    
    # HfPyramidSlopedTerrainCfg
    (cfg.HfPyramidSlopedTerrainCfg, "hf_pyramid_sloped_terrain",
     {
         "size": TERRAIN_SIZE,
         "border_width": 0.0,
         "horizontal_scale": 0.1,
         "vertical_scale": 0.005,
         "slope_threshold": None,
         "slope_range": (0.15, 0.3),
         "platform_width": 1.0,
         "inverted": False
     }),
    
    # HfInvertedPyramidSlopedTerrainCfg
    (cfg.HfInvertedPyramidSlopedTerrainCfg, "hf_pyramid_sloped_terrain",
     {
         "size": TERRAIN_SIZE,
         "border_width": 0.0,
         "horizontal_scale": 0.1,
         "vertical_scale": 0.005,
         "slope_threshold": None,
         "slope_range": (0.15, 0.3),
         "platform_width": 1.0,
         "inverted": True
     }),
    
    # HfPyramidStairsTerrainCfg
    (cfg.HfPyramidStairsTerrainCfg, "hf_pyramid_stairs_terrain",
     {
         "size": TERRAIN_SIZE,
         "border_width": 0.0,
         "horizontal_scale": 0.1,
         "vertical_scale": 0.005,
         "slope_threshold": None,
         "step_height_range": (0.2, 0.3),
         "step_width": 1.0,
         "platform_width": 1.0,
         "inverted": False
     }),
    
    # HfInvertedPyramidStairsTerrainCfg
    (cfg.HfInvertedPyramidStairsTerrainCfg, "hf_pyramid_stairs_terrain",
     {
         "size": TERRAIN_SIZE,
         "border_width": 0.0,
         "horizontal_scale": 0.1,
         "vertical_scale": 0.005,
         "slope_threshold": None,
         "step_height_range": (0.2, 0.3),
         "step_width": 1.0,
         "platform_width": 1.0,
         "inverted": True
     }),
    
    # HfDiscreteObstaclesTerrainCfg
    (cfg.HfDiscreteObstaclesTerrainCfg, "hf_discrete_obstacles_terrain",
     {
         "size": TERRAIN_SIZE,
         "border_width": 0.0,
         "horizontal_scale": 0.1,
         "vertical_scale": 0.005,
         "slope_threshold": None,
         "obstacle_height_mode": "choice",
         "obstacle_width_range": (0.3, 0.8),
         "obstacle_height_range": (0.1, 0.4),
         "num_obstacles": 20,
         "platform_width": 1.0
     }),
    
    # HfWaveTerrainCfg
    (cfg.HfWaveTerrainCfg, "hf_wave_terrain",
     {
         "size": TERRAIN_SIZE,
         "border_width": 0.0,
         "horizontal_scale": 0.1,
         "vertical_scale": 0.005,
         "slope_threshold": None,
         "amplitude_range": (0.08, 0.15),
         "num_waves": 3
     }),
    
    # HfSteppingStonesTerrainCfg
    (cfg.HfSteppingStonesTerrainCfg, "hf_stepping_stones_terrain",
 {
     "size": TERRAIN_SIZE,               # (10.0, 10.0)米
     "border_width": 0.0,               # 无边界
     "horizontal_scale": 0.1,           # 0.1米/像素
     "vertical_scale": 0.005,           # 垂直精度
     "slope_threshold": None,           # 无坡度修正
     
     # 石头参数
     "stone_height_max": 0.3,           # 石头最大高度0.3米
     "stone_width_range": (0.5, 1.0),   # 石头宽度0.5-1.0米
     
     # 覆盖率控制
     "stone_coverage": 0.15,            # 目标覆盖率15%
     "min_stone_count": 10,             # 至少生成10个石头
     "max_generation_attempts": 2000,   # 最多尝试2000次
     "stone_min_distance": 0.1,         # 石头间最小距离0.1米
     
     # 其他参数
     "holes_depth": -5.0,               # 坑深-5.0米
     "platform_width": 1.0              # 中心平台1.0米
     }),
]

def main():
    for CfgClass, func_name, params in TERRAIN_POOL:
        try:
            # 创建配置对象
            cfg_obj = CfgClass(**params)
            
            # 获取对应的生成函数
            gen_func = getattr(hf_terrains, func_name)
            
            # 生成地形
            meshes, origin = gen_func(cfg_obj)
            
            # 导出STL文件
            out_file = OUT_DIR / f"{CfgClass.__name__}.stl"
            meshes[0].export(out_file)
            
            print(f"✓ saved {out_file.name}  origin={origin}")
            
        except Exception as e:
            print(f"✗ failed to generate {CfgClass.__name__}: {e}")
    
    print(f"\n✅ All terrain STL files are ready in {OUT_DIR.resolve()}")

if __name__ == "__main__":
    main()