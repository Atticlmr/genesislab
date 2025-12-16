import time
import os
import numpy as np
import genesis as gs

class VisualizationMakers():
    def __init__(self, scene):

        self.scene = scene

    def draw_box(self, clear = True, color:tuple = (1, 0, 1, 1)):
        debug_box = self.scene.draw_debug_box(
            bounds = [[-0.25, -0.25, 0], [0.25, 0.25, 0.5]],
            color = color,
            wireframe = True,
            wireframe_radius = 0.005,  # Magenta
        )

        if clear:
            self.scene.clear_debug_object(debug_box)
            
    def draw_line(self, clear  = True, color:tuple = (1, 0, 0, 1)):
        debug_line = self.scene.draw_debug_line(
            start=(0.5, -0.25, 0.5), end=(0.5, 0.25, 0.5), radius=0.01, color=color
        )  
        if clear :
            self.scene.clear_debug_object(debug_line)
            
    def draw_arrow(self, clear = True, color:tuple = (1, 0, 0, 0.5)):
        debug_arrow = self.scene.draw_debug_arrow(pos=(1, 0, 0), vec=(0, 0, 1), radius=0.02, color=color)
        if clear:
            self.scene.clear_debug_object(debug_arrow)

    def draw_sphere(self, clear, color:tuple = (0, 0, 1, 0.5)):
        debug_sphere = self.scene.draw_debug_sphere(pos=(1.5, 0, 0.5), radius=0.1, color=color)  # Blue with alpha
        if clear:
            self.scene.clear_debug_object(debug_sphere)
            
    def draw_frame(self, clear = True):  
        T = np.eye(4)
        T[:3, 3] = [2.5, 0, 0.5]
        debug_frame = self.scene.draw_debug_frame(T=T, axis_length=0.5, origin_size=0.03, axis_radius=0.02)
        if clear:
            self.scene.clear_debug_objects(debug_frame)