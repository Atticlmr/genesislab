from genesislab.markers.visualize import VisualizationMakers

import time
import os
import numpy as np
import genesis as gs


gs.init(backend=gs.cpu)

# Scene setup
viewer_options = gs.options.ViewerOptions(
    camera_pos=(5.0, -5.0, 2.5),
    camera_lookat=(0.0, 0.0, 0.0),
    camera_fov=40,
    max_FPS=200,
)

scene = gs.Scene(
    viewer_options=viewer_options,
    show_viewer=False,
)

# Add a plane for reference
scene.add_entity(morph=gs.morphs.Plane())
scene.build()


Visualize = VisualizationMakers(scene)

Visualize.draw_box(clear = False)

for i in range(100):
    scene.step()
    time.sleep(0.01)