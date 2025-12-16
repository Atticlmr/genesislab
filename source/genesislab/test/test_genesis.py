import os

import numpy as np
import genesis as gs


########################## init ##########################
gs.init(backend=gs.gpu)

########################## create a scene ##########################
scene = gs.Scene(
    vis_options = gs.options.VisOptions(
        show_world_frame = True, # visualize the coordinate frame of `world` at its origin
        world_frame_size = 1.0, # length of the world frame in meter
        show_link_frame  = False, # do not visualize coordinate frames of entity links
        show_cameras     = False, # do not visualize mesh and frustum of the cameras added
        plane_reflection = True, # turn on plane reflection
        ambient_light    = (0.6, 0.6, 0.6), # ambient light setting
        lights=[
            # 主方向光源
            {
                'type': 'directional',
                'dir': (-0.5, -0.5, -1.0),  # 光照方向
                'color': (1.0, 1.0, 1.0),         # 光源颜色和强度
                'intensity': 1.0,                 # 光源强度
            },],
        background_color=(0.5, 0.5, 0.5),
    ),
    sim_options=gs.options.SimOptions(
        dt=0.01,
    ),
    show_viewer=True,
)
terrain = scene.add_entity(
    gs.morphs.Mesh(
        file="/home/li/Desktop/terrain_stl/HfRandomUniformTerrainCfg.stl",
        
        # 地形通常需要以下设置：
        pos=(0.0, 0.0, 0.0),      # 放在世界原点
        fixed=True,               # 地形固定不动
        visualization=True,       # 需要可视化
        collision=True,           # 需要碰撞检测
        
        # 网格简化设置（地形通常面数很多，需要简化）
        decimate=True,
        decimate_face_num=2000,   # 地形可以简化到2000面
        decimate_aggressiveness=5, # 中等强度简化
        
        # 地形通常不需要凸分解（除非有穿透问题）
        convexify=False,
        
        # 可以设置缩放以适应场景
        scale=(1.0, 1.0, 1.0),    # x,y,z方向的缩放（这里z方向缩小一半）
    )
)
########################## build ##########################
scene.build()


for i in range(10000):
    scene.step()