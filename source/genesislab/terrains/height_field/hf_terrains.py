 # GitHub: https://github.com/Atticlmr/genesislab
 # Author: Li Mingrui
 # Copyright (c) 2025 Li Mingrui, Beihang University
 # License: Apache-2.0
from .utils import hf_to_mesh
import numpy as np
from . import hf_terrians_cfg


@hf_to_mesh(dx=0.1, dy=0.1)
def hf_random_uniform_terrain(cfg: hf_terrians_cfg.HfRandomUniformTerrainCfg) -> np.ndarray:
    h_pix = int(cfg.size[1] / 0.1)      # 0.1 是 dy
    w_pix = int(cfg.size[0] / 0.1)      # 0.1 是 dx
    z_min, z_max = cfg.noise_range
    step = cfg.noise_step

    # 先下采样再插值（兼容 downsampled_scale）
    ds = cfg.downsampled_scale or 0.1
    h_ds = int(cfg.size[1] / ds)
    w_ds = int(cfg.size[0] / ds)
    # 随机采样
    z = np.random.uniform(z_min, z_max, size=(h_ds, w_ds))
    # 量化到 step
    z = np.round(z / step) * step
    # 线性插值回原始分辨率
    from scipy.ndimage import zoom
    hf = zoom(z, (h_pix / h_ds, w_pix / w_ds), order=1)
    return hf

@hf_to_mesh(dx=0.1, dy=0.1)
def hf_pyramid_sloped_terrain(cfg: hf_terrians_cfg.HfPyramidSlopedTerrainCfg) -> np.ndarray:
    h_pix = int(cfg.size[1] / 0.1)
    w_pix = int(cfg.size[0] / 0.1)
    slope = np.random.uniform(*cfg.slope_range)          # 弧度
    platform_pix = int(cfg.platform_width / 0.1)
    # 中心坐标
    cy, cx = h_pix // 2, w_pix // 2
    y, x = np.ogrid[:h_pix, :w_pix]
    # 到中心距离
    dist = np.maximum(np.abs(x - cx), np.abs(y - cy))   # 切比雪夫距离（正方形）
    # 高度 = 距离 * tan(坡度)
    hf = dist * 0.1 * np.tan(slope)                     # 0.1 米/像素
    # 平台区域削平
    mask = dist <= platform_pix / 2
    hf[mask] = hf[int(cy + platform_pix // 2), int(cx)]
    # 倒/正
    return -hf if cfg.inverted else hf

@hf_to_mesh(dx=0.1, dy=0.1)
def hf_pyramid_stairs_terrain(cfg: hf_terrians_cfg.HfPyramidStairsTerrainCfg) -> np.ndarray:
    h_pix = int(cfg.size[1] / 0.1)
    w_pix = int(cfg.size[0] / 0.1)
    h_min, h_max = cfg.step_height_range
    step_w_pix = int(cfg.step_width / 0.1)
    plat_w_pix = int(cfg.platform_width / 0.1)
    
    layers = int(min(h_pix, w_pix) // 2 // step_w_pix)
    
    increments = np.random.uniform(h_min, h_max, layers)
    
    step_heights = np.cumsum(increments)
    # 中心坐标
    cy, cx = h_pix // 2, w_pix // 2
    
    y, x = np.ogrid[:h_pix, :w_pix]
    dist = np.maximum(np.abs(x - cx), np.abs(y - cy))
    hf = np.zeros_like(dist, dtype=float)
    
    for n in range(layers):
        r_out = plat_w_pix // 2 + n * step_w_pix
        r_in = r_out + step_w_pix
        mask = (dist >= r_out) & (dist < r_in)
        hf[mask] = step_heights[n]
    
    hf[dist <= plat_w_pix // 2] = 0
    
    if cfg.inverted:
        hf = -hf
    
    return hf

@hf_to_mesh(dx=0.1, dy=0.1)
def hf_discrete_obstacles_terrain(cfg: hf_terrians_cfg.HfDiscreteObstaclesTerrainCfg) -> np.ndarray:
    h_pix = int(cfg.size[1] / 0.1)
    w_pix = int(cfg.size[0] / 0.1)
    w_min, w_max = cfg.obstacle_width_range
    h_min, h_max = cfg.obstacle_height_range
    n_obs = cfg.num_obstacles
    platform_pix = int(cfg.platform_width / 0.1)

    hf = np.zeros((h_pix, w_pix))

    for _ in range(n_obs):
        # 随机宽高
        if cfg.obstacle_height_mode == "choice":
            hz = np.random.uniform(h_min, h_max)
        else:
            hz = h_max
        wd = int(np.random.uniform(w_min, w_max) / 0.1)
        # 随机左上角
        y0 = np.random.randint(0, h_pix - wd)
        x0 = np.random.randint(0, w_pix - wd)
        hf[y0:y0 + wd, x0:x0 + wd] = hz

    # 中心平台清空
    cy, cx = h_pix // 2, w_pix // 2
    half = platform_pix // 2
    hf[cy - half:cy + half, cx - half:cx + half] = 0
    return hf


@hf_to_mesh(dx=0.1, dy=0.1)
def hf_wave_terrain(cfg: hf_terrians_cfg.HfWaveTerrainCfg) -> np.ndarray:
    h_pix = int(cfg.size[1] / 0.1)
    w_pix = int(cfg.size[0] / 0.1)
    a_min, a_max = cfg.amplitude_range
    amp = np.random.uniform(a_min, a_max)
    n_waves = cfg.num_waves

    x = np.linspace(0, n_waves * 2 * np.pi, w_pix)
    y = np.linspace(0, 1, h_pix)
    yy, xx = np.meshgrid(y, x, indexing="ij")
    hf = amp * np.sin(xx)
    return hf


@hf_to_mesh(dx=0.1, dy=0.1)
def hf_stepping_stones_terrain(cfg: hf_terrians_cfg.HfSteppingStonesTerrainCfg) -> np.ndarray:
    """
    生成踏脚石地形
    
    基于覆盖率和石头大小控制石头分布：
    1. 计算地形总面积和需要的石头总面积
    2. 根据覆盖率参数生成足够数量的石头
    3. 石头在中心平台外的区域随机分布
    4. 可以设置石头之间的最小距离避免过度重叠
    """
    
    # 地形尺寸（像素）
    h_pix = int(cfg.size[1] / cfg.horizontal_scale)
    w_pix = int(cfg.size[0] / cfg.horizontal_scale)
    
    # 石头参数
    w_min, w_max = cfg.stone_width_range
    h_max = cfg.stone_height_max
    holes = cfg.holes_depth
    platform_pix = int(cfg.platform_width / cfg.horizontal_scale)
    
    # 初始化地形为深坑
    hf = np.full((h_pix, w_pix), holes, dtype=float)
    
    # 中心平台（安全区域）
    cy, cx = h_pix // 2, w_pix // 2
    half_platform = platform_pix // 2
    
    # 清空中心平台区域（设为0高度）
    hf[cy - half_platform:cy + half_platform, 
       cx - half_platform:cx + half_platform] = 0
    
    # ==================== 计算石头生成参数 ====================
    
    # 计算有效区域面积（除去中心平台）
    terrain_area = cfg.size[0] * cfg.size[1]  # 地形总面积（平方米）
    platform_area = cfg.platform_width ** 2   # 中心平台面积
    effective_area = terrain_area - platform_area  # 可放置石头的区域面积
    
    # 计算需要覆盖的面积
    target_coverage_area = effective_area * cfg.stone_coverage
    
    # 计算平均石头面积
    avg_stone_width = (w_min + w_max) / 2
    avg_stone_area = avg_stone_width ** 2
    
    # 计算目标石头数量
    target_stone_count = max(
        cfg.min_stone_count,  # 至少生成最小数量
        int(target_coverage_area / avg_stone_area)  # 根据覆盖率计算的数量
    )
    
    # 转换为像素单位
    min_distance_pix = int(cfg.stone_min_distance / cfg.horizontal_scale)
    
    # ==================== 生成石头 ====================
    
    placed_stones = []  # 记录已放置的石头：(center_x, center_y, radius)
    stones_generated = 0
    attempts = 0
    
    print(f"踏脚石地形生成:")
    print(f"  地形尺寸: {cfg.size[0]:.1f}x{cfg.size[1]:.1f} m")
    print(f"  目标覆盖率: {cfg.stone_coverage:.1%}")
    print(f"  有效区域: {effective_area:.1f} m²")
    print(f"  目标覆盖面积: {target_coverage_area:.1f} m²")
    print(f"  目标石头数量: {target_stone_count}")
    
    # 可用区域边界（避开中心平台）
    min_radius = half_platform + min_distance_pix
    max_radius = min(h_pix, w_pix) // 2 - int(w_max / cfg.horizontal_scale)
    
    while stones_generated < target_stone_count and attempts < cfg.max_generation_attempts:
        attempts += 1
        
        # 随机石头大小（转换为像素）
        stone_width_m = np.random.uniform(w_min, w_max)
        stone_width_pix = int(stone_width_m / cfg.horizontal_scale)
        stone_radius_pix = stone_width_pix // 2
        
        # 随机位置（极坐标方式，在有效区域内）
        angle = np.random.uniform(0, 2 * np.pi)
        radius = np.random.uniform(min_radius, max_radius)
        
        stone_center_x = int(cx + radius * np.cos(angle))
        stone_center_y = int(cy + radius * np.sin(angle))
        
        # 计算石头边界
        x0 = stone_center_x - stone_radius_pix
        y0 = stone_center_y - stone_radius_pix
        x1 = stone_center_x + stone_radius_pix
        y1 = stone_center_y + stone_radius_pix
        
        # 检查是否在地形边界内
        if x0 < 0 or y0 < 0 or x1 >= w_pix or y1 >= h_pix:
            continue
        
        # 检查是否与其他石头太近
        too_close = False
        for (px, py, p_radius) in placed_stones:
            distance = np.sqrt((stone_center_x - px) ** 2 + (stone_center_y - py) ** 2)
            min_required = p_radius + stone_radius_pix + min_distance_pix
            if distance < min_required:
                too_close = True
                break
        
        if too_close:
            continue
        
        # 生成石头高度（在最大高度范围内随机）
        stone_height = np.random.uniform(0.1 * h_max, h_max)  # 至少10%最大高度
        
        # 放置石头（设为正方形石头）
        hf[y0:y1, x0:x1] = stone_height
        
        # 记录已放置的石头
        placed_stones.append((stone_center_x, stone_center_y, stone_radius_pix))
        stones_generated += 1
        
        # 每生成10个石头打印进度
        if stones_generated % 10 == 0:
            current_coverage = stones_generated * avg_stone_area / effective_area
            print(f"  已生成 {stones_generated}/{target_stone_count} 个石头 (覆盖率: {current_coverage:.1%})")
    
    # ==================== 统计结果 ====================
    
    # 计算实际覆盖率
    total_stone_area = 0
    for _, _, radius in placed_stones:
        stone_area = (2 * radius * cfg.horizontal_scale) ** 2  # 转换为平方米
        total_stone_area += stone_area
    
    actual_coverage = total_stone_area / effective_area
    
    print(f"生成完成:")
    print(f"  实际生成石头: {stones_generated} 个")
    print(f"  实际覆盖面积: {total_stone_area:.1f} m²")
    print(f"  实际覆盖率: {actual_coverage:.1%}")
    print(f"  尝试次数: {attempts}")
    
    return hf