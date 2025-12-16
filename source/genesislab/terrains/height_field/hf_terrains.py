 # GitHub: https://github.com/Atticlmr/genesislab
 # Author: Li Mingrui
 # Copyright (c) 2025 Li Mingrui, Beihang University
 # License: Apache-2.0
from .utils import hf_to_mesh
import numpy as np
from . import hf_terrians_cfg


@hf_to_mesh(dx=0.1, dy=0.1)
def hf_random_uniform_terrain(cfg: hf_terrians_cfg.HfRandomUniformTerrainCfg) -> np.ndarray:
    h_pix = int(cfg.size[1] / 0.1)
    w_pix = int(cfg.size[0] / 0.1)
    z_min, z_max = cfg.noise_range
    step = cfg.noise_step

    ds = cfg.downsampled_scale or 0.1
    h_ds = int(cfg.size[1] / ds)
    w_ds = int(cfg.size[0] / ds)
    
    z = np.random.uniform(z_min, z_max, size=(h_ds, w_ds))
    z = np.round(z / step) * step
    
    from scipy.ndimage import zoom
    hf = zoom(z, (h_pix / h_ds, w_pix / w_ds), order=1)
    return hf

@hf_to_mesh(dx=0.1, dy=0.1)
def hf_pyramid_sloped_terrain(cfg: hf_terrians_cfg.HfPyramidSlopedTerrainCfg) -> np.ndarray:
    h_pix = int(cfg.size[1] / 0.1)
    w_pix = int(cfg.size[0] / 0.1)
    slope = np.random.uniform(*cfg.slope_range)
    platform_pix = int(cfg.platform_width / 0.1)
    cy, cx = h_pix // 2, w_pix // 2
    y, x = np.ogrid[:h_pix, :w_pix]
    dist = np.maximum(np.abs(x - cx), np.abs(y - cy))
    
    max_dist = max(cx, cy)
    
    platform_radius = platform_pix / 2
    
    if not cfg.inverted:
        platform_edge_height = max(0, max_dist - platform_radius) * 0.1 * np.tan(slope)
        hf = max_dist * 0.1 * np.tan(slope) - dist * 0.1 * np.tan(slope)
        mask = dist <= platform_radius
        hf[mask] = platform_edge_height
    else:
        min_height = -max_dist * 0.1 * np.tan(slope)
        platform_edge_height = min_height + platform_radius * 0.1 * np.tan(slope)
        hf = min_height + dist * 0.1 * np.tan(slope)
        mask = dist <= platform_radius
        hf[mask] = platform_edge_height
    
    return hf

@hf_to_mesh(dx=0.1, dy=0.1)
def hf_pyramid_stairs_terrain(cfg: hf_terrians_cfg.HfPyramidStairsTerrainCfg) -> np.ndarray:
    h_pix = int(cfg.size[1] / 0.1)
    w_pix = int(cfg.size[0] / 0.1)
    h_min, h_max = cfg.step_height_range
    step_w_pix = int(cfg.step_width / 0.1)
    plat_w_pix = int(cfg.platform_width / 0.1)
    
    layers = int(min(h_pix, w_pix) // 2 // step_w_pix)
    increments = np.random.uniform(h_min, h_max, layers)
    cumulative_heights = np.cumsum(increments)
    
    cy, cx = h_pix // 2, w_pix // 2
    y, x = np.ogrid[:h_pix, :w_pix]
    dist = np.maximum(np.abs(x - cx), np.abs(y - cy))
    hf = np.zeros_like(dist, dtype=float)
    
    if cfg.inverted:
        for n in range(layers):
            r_out = plat_w_pix // 2 + n * step_w_pix
            r_in = r_out + step_w_pix
            mask = (dist >= r_out) & (dist < r_in)
            hf[mask] = cumulative_heights[n]
        hf[dist <= plat_w_pix // 2] = 0
        
        max_height = cumulative_heights[-1] if layers > 0 else 0
        hf = hf - max_height
    else:
        total_height = cumulative_heights[-1] if layers > 0 else 0
        hf[dist <= plat_w_pix // 2] = total_height
        
        for n in range(layers):
            r_out = plat_w_pix // 2 + n * step_w_pix
            r_in = r_out + step_w_pix
            mask = (dist >= r_out) & (dist < r_in)
            if n == 0:
                layer_height = total_height - increments[0]
            else:
                layer_height = total_height - cumulative_heights[n]
            hf[mask] = layer_height
    
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
        if cfg.obstacle_height_mode == "choice":
            hz = np.random.uniform(h_min, h_max)
        else:
            hz = h_max
        wd = int(np.random.uniform(w_min, w_max) / 0.1)
        y0 = np.random.randint(0, h_pix - wd)
        x0 = np.random.randint(0, w_pix - wd)
        hf[y0:y0 + wd, x0:x0 + wd] = hz

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
    h_pix = int(cfg.size[1] / cfg.horizontal_scale)
    w_pix = int(cfg.size[0] / cfg.horizontal_scale)
    
    w_min, w_max = cfg.stone_width_range
    h_max = cfg.stone_height_max
    holes = cfg.holes_depth
    platform_pix = int(cfg.platform_width / cfg.horizontal_scale)
    
    hf = np.full((h_pix, w_pix), holes, dtype=float)
    
    cy, cx = h_pix // 2, w_pix // 2
    half_platform = platform_pix // 2
    hf[cy - half_platform:cy + half_platform,
       cx - half_platform:cx + half_platform] = 0
    
    terrain_area = cfg.size[0] * cfg.size[1]
    platform_area = cfg.platform_width ** 2
    effective_area = terrain_area - platform_area
    target_coverage_area = effective_area * cfg.stone_coverage
    
    avg_stone_width = (w_min + w_max) / 2
    avg_stone_area = avg_stone_width ** 2
    target_stone_count = max(cfg.min_stone_count, int(target_coverage_area / avg_stone_area))
    min_distance_pix = int(cfg.stone_min_distance / cfg.horizontal_scale)
    
    placed_stones = []
    stones_generated = 0
    attempts = 0

    min_radius = half_platform + min_distance_pix
    max_radius = min(h_pix, w_pix) // 2 - int(w_max / cfg.horizontal_scale)
    
    while stones_generated < target_stone_count and attempts < cfg.max_generation_attempts:
        attempts += 1
        
        stone_width_m = np.random.uniform(w_min, w_max)
        stone_width_pix = int(stone_width_m / cfg.horizontal_scale)
        stone_radius_pix = stone_width_pix // 2
        
        angle = np.random.uniform(0, 2 * np.pi)
        radius = np.random.uniform(min_radius, max_radius)
        
        stone_center_x = int(cx + radius * np.cos(angle))
        stone_center_y = int(cy + radius * np.sin(angle))
        
        x0 = stone_center_x - stone_radius_pix
        y0 = stone_center_y - stone_radius_pix
        x1 = stone_center_x + stone_radius_pix
        y1 = stone_center_y + stone_radius_pix
        
        if x0 < 0 or y0 < 0 or x1 >= w_pix or y1 >= h_pix:
            continue
        
        too_close = False
        for (px, py, p_radius) in placed_stones:
            distance = np.sqrt((stone_center_x - px) ** 2 + (stone_center_y - py) ** 2)
            min_required = p_radius + stone_radius_pix + min_distance_pix
            if distance < min_required:
                too_close = True
                break
        
        if too_close:
            continue
        
        stone_height = np.random.uniform(0.1 * h_max, h_max)
        hf[y0:y1, x0:x1] = stone_height
        
        placed_stones.append((stone_center_x, stone_center_y, stone_radius_pix))
        stones_generated += 1
    
    total_stone_area = 0
    for _, _, radius in placed_stones:
        stone_area = (2 * radius * cfg.horizontal_scale) ** 2
        total_stone_area += stone_area
    
    return hf