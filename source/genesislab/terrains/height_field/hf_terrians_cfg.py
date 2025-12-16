 # GitHub: https://github.com/Atticlmr/genesislab
 # Author: Li Mingrui
 # Copyright (c) 2025 Li Mingrui, Beihang University
 # License: Apache-2.0
 #  This file is derived from Isaac Lab.(https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).

from dataclasses import dataclass,MISSING
@dataclass
class HfTerrainBaseCfg:
    """ Base configuration for height field terrain"""
    size: tuple[float, float]

    border_width: float 
    """The width of the border/padding around the terrain (in m). Defaults to 0.0.

    The border width is subtracted from the :obj:`size` of the terrain. If non-zero, it must be
    greater than or equal to the :obj:`horizontal scale`.
    """

    horizontal_scale: float 
    """The discretization of the terrain along the x and y axes (in m). Defaults to 0.1."""

    vertical_scale: float 
    """The discretization of the terrain along the z axis (in m). Defaults to 0.005."""

    slope_threshold: float | None 
    """The slope threshold above which surfaces are made vertical. Defaults to None,
    in which case no correction is applied."""



@dataclass
class HfRandomUniformTerrainCfg(HfTerrainBaseCfg):
    """Configuration for a random uniform height field terrain."""


    noise_range: tuple[float, float] = MISSING
    """The minimum and maximum height noise (i.e. along z) of the terrain (in m)."""

    noise_step: float = MISSING
    """The minimum height (in m) change between two points."""

    downsampled_scale: float | None = None
    """The distance between two randomly sampled points on the terrain. Defaults to None,
    in which case the :obj:`horizontal scale` is used.

    The heights are sampled at this resolution and interpolation is performed for intermediate points.
    This must be larger than or equal to the :obj:`horizontal scale`.
    """


@dataclass
class HfPyramidSlopedTerrainCfg(HfTerrainBaseCfg):
    """Configuration for a pyramid sloped height field terrain."""
    

    slope_range: tuple[float, float] = MISSING
    """The slope of the terrain (in radians)."""

    platform_width: float = 1.0
    """The width of the square platform at the center of the terrain. Defaults to 1.0."""

    inverted: bool = False
    """Whether the pyramid is inverted. Defaults to False.

    If True, the terrain is inverted such that the platform is at the bottom and the slopes are upwards.
    """

@dataclass
class HfInvertedPyramidSlopedTerrainCfg(HfPyramidSlopedTerrainCfg):
    """Configuration for an inverted pyramid sloped height field terrain.

    Note:
        This is a subclass of :class:`HfPyramidSlopedTerrainCfg` with :obj:`inverted` set to True.
        We make it as a separate class to make it easier to distinguish between the two and match
        the naming convention of the other terrains.
    """

    inverted: bool = True


@dataclass
class HfPyramidStairsTerrainCfg(HfTerrainBaseCfg):
    """Configuration for a pyramid stairs height field terrain."""


    step_height_range: tuple[float, float] = MISSING
    """The minimum and maximum height of the steps (in m)."""

    step_width: float = MISSING
    """The width of the steps (in m)."""

    platform_width: float = 1.0
    """The width of the square platform at the center of the terrain. Defaults to 1.0."""

    inverted: bool = False
    """Whether the pyramid stairs is inverted. Defaults to False.

    If True, the terrain is inverted such that the platform is at the bottom and the stairs are upwards.
    """


@dataclass
class HfInvertedPyramidStairsTerrainCfg(HfPyramidStairsTerrainCfg):
    """Configuration for an inverted pyramid stairs height field terrain.

    Note:
        This is a subclass of :class:`HfPyramidStairsTerrainCfg` with :obj:`inverted` set to True.
        We make it as a separate class to make it easier to distinguish between the two and match
        the naming convention of the other terrains.
    """

    inverted: bool = True

@dataclass
class HfDiscreteObstaclesTerrainCfg(HfTerrainBaseCfg):
    """Configuration for a discrete obstacles height field terrain."""


    obstacle_height_mode: str 
    """The mode to use for the obstacle height. Defaults to "choice".

    The following modes are supported: "choice", "fixed".
    """

    obstacle_width_range: tuple[float, float] = MISSING
    """The minimum and maximum width of the obstacles (in m)."""

    obstacle_height_range: tuple[float, float] = MISSING
    """The minimum and maximum height of the obstacles (in m)."""

    num_obstacles: int = MISSING
    """The number of obstacles to generate."""

    platform_width: float = 1.0
    """The width of the square platform at the center of the terrain. Defaults to 1.0."""


@dataclass
class HfWaveTerrainCfg(HfTerrainBaseCfg):
    """Configuration for a wave height field terrain."""

    amplitude_range: tuple[float, float] = MISSING
    """The minimum and maximum amplitude of the wave (in m)."""

    num_waves: int = 1
    """The number of waves to generate. Defaults to 1."""


@dataclass 
class HfSteppingStonesTerrainCfg(HfTerrainBaseCfg):
    """Configuration for a stepping stones height field terrain."""
    
    stone_height_max: float = MISSING
    """The maximum height of the stones (in m)."""
    
    stone_width_range: tuple[float, float] = MISSING
    """The minimum and maximum width of the stones (in m)."""
    
    stone_coverage: float = 0.15
    """The target coverage percentage of stones in the terrain (0.0 to 1.0). 
    Defaults to 0.15 (15% coverage)."""
    
    min_stone_count: int = 10
    """The minimum number of stones to generate. Defaults to 10."""
    
    max_generation_attempts: int = 1000
    """Maximum attempts to generate stones before giving up. Defaults to 1000."""
    
    stone_min_distance: float = 0.0
    """Minimum distance between stones (in m). Defaults to 0.0 (stones can touch)."""
    
    holes_depth: float = -10.0
    """The depth of the holes (negative obstacles). Defaults to -10.0."""
    
    platform_width: float = 1.0
    
