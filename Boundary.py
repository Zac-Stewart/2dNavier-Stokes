import numpy as np
import math

class Boundary:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.bc_vert_type = np.zeros((width + 1, height), dtype=np.int32)
        self.bc_vert_dir = np.zeros((width + 1, height), dtype=np.int32)
        self.bc_horz_type = np.zeros((width, height + 1), dtype=np.int32)
        self.bc_horz_dir = np.zeros((width, height + 1), dtype=np.int32)

        #self.solid = np.zeros((width, height))

        self.u = np.zeros((width + 1, height))
        self.v = np.zeros((width, height + 1))

        self.update_mask()

    def set_standard(self):
        self.bc_vert_type[0, :] = 1
        self.bc_vert_dir[0, :] = 0

        self.bc_vert_type[-1, :] = 1
        self.bc_vert_dir[-1, :] = 1

        self.bc_horz_type[:, 0] = 1
        self.bc_horz_dir[:, 0] = 0

        self.bc_horz_type[:, -1] = 1
        self.bc_horz_dir[:, -1] = 1
        self.update_mask()

    def update_mask(self):
        self.vert_none = np.nonzero(
            self.bc_vert_type == 0
        )


        self.vert_left_no_slip = np.nonzero(
            (self.bc_vert_type == 1) &
            (self.bc_vert_dir == 0)
        )
        self.vert_left_free_slip = np.nonzero(
            (self.bc_vert_type == 2) &
            (self.bc_vert_dir == 0)
        )
        self.vert_left_inflow = np.nonzero(
            (self.bc_vert_type == 3) &
            (self.bc_vert_dir == 0)
        )
        self.vert_left_outflow = np.nonzero(
            (self.bc_vert_type == 4) &
            (self.bc_vert_dir == 0)
        )
        self.vert_left_boundary = np.nonzero(
            (self.bc_vert_type != 0) &
            (self.bc_vert_dir == 0)
        )


        self.vert_right_no_slip = np.nonzero(
            (self.bc_vert_type == 1) &
            (self.bc_vert_dir == 1)
        )
        self.vert_right_free_slip = np.nonzero(
            (self.bc_vert_type == 2) &
            (self.bc_vert_dir == 1)
        )
        self.vert_right_inflow = np.nonzero(
            (self.bc_vert_type == 3) &
            (self.bc_vert_dir == 1)
        )
        self.vert_right_outflow = np.nonzero(
            (self.bc_vert_type == 4) &
            (self.bc_vert_dir == 1)
        )
        self.vert_right_boundary = np.nonzero(
            (self.bc_vert_type != 0) &
            (self.bc_vert_dir == 1)
        )


        self.horz_none = np.nonzero(
            self.bc_horz_type == 0
        )


        self.horz_up_no_slip = np.nonzero(
            (self.bc_horz_type == 1) &
            (self.bc_horz_dir == 0)
        )
        self.horz_up_free_slip = np.nonzero(
            (self.bc_horz_type == 2) &
            (self.bc_horz_dir == 0)
        )
        self.horz_up_inflow = np.nonzero(
            (self.bc_horz_type == 3) &
            (self.bc_horz_dir == 0)
        )
        self.horz_up_outflow = np.nonzero(
            (self.bc_horz_type == 4) &
            (self.bc_horz_dir == 0)
        )
        self.horz_up_boundary = np.nonzero(
            (self.bc_horz_type != 0) &
            (self.bc_horz_dir == 0)
        )


        self.horz_down_no_slip = np.nonzero(
            (self.bc_horz_type == 1) &
            (self.bc_horz_dir == 1)
        )
        self.horz_down_free_slip = np.nonzero(
            (self.bc_horz_type == 2) &
            (self.bc_horz_dir == 1)
        )
        self.horz_down_inflow = np.nonzero(
            (self.bc_horz_type == 3) &
            (self.bc_horz_dir == 1)
        )
        self.horz_down_outflow = np.nonzero(
            (self.bc_horz_type == 4) &
            (self.bc_horz_dir == 1)
        )
        self.horz_down_boundary = np.nonzero(
            (self.bc_horz_type != 0) &
            (self.bc_horz_dir == 1)
        )

    def add_boundary_object(self, boundary_object, scale):
        """
        Directly overwrites the grid's boundary arrays and velocity fields.
        Immune to vertex ordering (works identically for CW and CCW polygons).
        
        Direction Mapping:
        0 = Positive direction (+x or +y)
        1 = Negative direction (-x or -y)
        """
        vertices = boundary_object.vertices
        edge_types = boundary_object.edges_type      
        edge_rel_vels = boundary_object.edges_rel_vel 
        is_flipped = boundary_object.is_flipped
        
        num_verts = len(vertices)
        if num_verts < 3:
            return

        dx = scale  
        
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        min_i = max(0, math.floor(min(xs) / dx) - 1)
        max_i = min(self.width, math.ceil(max(xs) / dx) + 1)
        min_j = max(0, math.floor(min(ys) / dx) - 1)
        max_j = min(self.height, math.ceil(max(ys) / dx) + 1)

        # --- Winding Number Calculation ---
        def get_winding_number(px, py):
            wn = 0
            for edge_idx in range(num_verts):
                v1 = vertices[edge_idx]
                v2 = vertices[(edge_idx + 1) % num_verts]
                if v1[1] <= py:
                    if v2[1] > py:
                        is_left = (v2[0] - v1[0]) * (py - v1[1]) - (px - v1[0]) * (v2[1] - v1[1])
                        if is_left > 0: wn += 1
                else:
                    if v2[1] <= py:
                        is_left = (v2[0] - v1[0]) * (py - v1[1]) - (px - v1[0]) * (v2[1] - v1[1])
                        if is_left < 0: wn -= 1
            return wn

        # --- Match Face Segment to Closest Cutting Edge ---
        def find_crossing_edge_index(p1, p2):
            min_dist = float('inf')
            best_idx = -1
            def ccw(A, B, C):
                return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
                
            for edge_idx in range(num_verts):
                v1 = vertices[edge_idx]
                v2 = vertices[(edge_idx + 1) % num_verts]
                if ccw(p1, v1, v2) != ccw(p2, v1, v2) and ccw(p1, p2, v1) != ccw(p1, p2, v2):
                    mx, my = (v1[0] + v2[0]) / 2.0, (v1[1] + v2[1]) / 2.0
                    dist = (mx - (p1[0]+p2[0])/2)**2 + (my - (p1[1]+p2[1])/2)**2
                    if dist < min_dist:
                        min_dist = dist
                        best_idx = edge_idx
            return best_idx

        # 3. Cache winding numbers within the active grid patch
        cell_winding = {}
        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                px = (i + 0.5) * dx
                py = (j + 0.5) * dx
                cell_winding[(i, j)] = get_winding_number(px, py)

        # 4. Traverse and update arrays directly
        for i in range(min_i, max_i - 1):
            for j in range(min_j, max_j - 1):
                wn_curr = cell_winding.get((i, j), 0)
                
                # --- PROCESS VERTICAL FACES (U Component) ---
                wn_right = cell_winding.get((i + 1, j), 0)
                if wn_curr != wn_right:
                    p_left = ((i + 0.5) * dx, (j + 0.5) * dx)
                    p_right = ((i + 1.5) * dx, (j + 0.5) * dx)
                    chosen_edge = find_crossing_edge_index(p_left, p_right)
                    
                    if chosen_edge != -1:
                        v1 = vertices[chosen_edge]
                        v2 = vertices[(chosen_edge + 1) % num_verts]
                        
                        dx_e = v2[0] - v1[0]
                        dy_e = v2[1] - v1[1]
                        length = math.hypot(dx_e, dy_e)
                        
                        if length > 0:
                            # Winding order independent inside/outside checking:
                            # If left cell is inside (non-zero) and right cell is outside (zero), outward is +X
                            if wn_curr != 0 and wn_right == 0:
                                nx, ny = 1.0, 0.0
                            else:
                                nx, ny = -1.0, 0.0
                            
                            tx, ty = -ny, nx 
                            
                            # Apply flip logic: pointing inward if True
                            if is_flipped:
                                nx, ny = -nx, -ny
                            
                            v_perp, v_para = edge_rel_vels[chosen_edge]
                            u_val = v_perp * nx + v_para * tx
                            
                            self.bc_vert_type[i + 1, j] = edge_types[chosen_edge]
                            self.bc_vert_dir[i + 1, j] = 0 if nx >= 0 else 1
                            self.u[i + 1, j] = u_val

                # --- PROCESS HORIZONTAL FACES (V Component) ---
                wn_top = cell_winding.get((i, j + 1), 0)
                if wn_curr != wn_top:
                    p_bottom = ((i + 0.5) * dx, (j + 0.5) * dx)
                    p_top = ((i + 0.5) * dx, (j + 1.5) * dx)
                    chosen_edge = find_crossing_edge_index(p_bottom, p_top)
                    
                    if chosen_edge != -1:
                        v1 = vertices[chosen_edge]
                        v2 = vertices[(chosen_edge + 1) % num_verts]
                        
                        dx_e = v2[0] - v1[0]
                        dy_e = v2[1] - v1[1]
                        length = math.hypot(dx_e, dy_e)
                        
                        if length > 0:
                            # If current (bottom) cell is inside and top cell is outside, outward is +Y
                            if wn_curr != 0 and wn_top == 0:
                                nx, ny = 0.0, 1.0
                            else:
                                nx, ny = 0.0, -1.0
                            
                            tx, ty = -ny, nx 
                            
                            if is_flipped:
                                nx, ny = -nx, -ny
                                
                            v_perp, v_para = edge_rel_vels[chosen_edge]
                            v_val = v_perp * ny + v_para * ty
                            
                            self.bc_horz_type[i, j + 1] = edge_types[chosen_edge]
                            self.bc_horz_dir[i, j + 1] = 0 if ny >= 0 else 1
                            self.v[i, j + 1] = v_val
        self.update_mask()