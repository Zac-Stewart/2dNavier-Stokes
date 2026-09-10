from geometry import winding
import numpy as np


class BoundaryObject:
    def __init__(self, vertices, edges_type=None, is_flipped=False, edges_rel_vel=None):
        self.vertices = vertices
        self.length = len(self.vertices)

        if edges_type == None:
            self.edges_type = np.ones(self.length, dtype=np.int32)
        else:
            self.edges_type = edges_type

        self.is_flipped = is_flipped

        if edges_rel_vel == None:
            self.edges_rel_vel = np.zeros((self.length, 2)) 
        else:
            self.edges_rel_vel = edges_rel_vel