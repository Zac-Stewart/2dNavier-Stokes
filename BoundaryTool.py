from BoundaryObject import BoundaryObject

class BoundaryTool:

    def __init__(self):
        self.type = "boundary"
        self.current_vertices = []
        self.drawing = False
        self.mouse_pos = None

    def mouse_down(self, pos, fluid, scene):
        if self.drawing == False:
            self.drawing = True

        self.current_vertices.append(pos)

    def enter_down(self, fluid, scene):
        self.drawing = False

        boundary_object = BoundaryObject(self.current_vertices)
        scene.boundary_objects.append(boundary_object)

        scale = scene.w / fluid.width

        fluid.boundary.add_boundary_object(boundary_object, scale)
    
        self.current_vertices = []

    def mouse_move(self, pos): 
        if self.drawing:
            self.mouse_pos = pos