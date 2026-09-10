import numpy as np
import matplotlib.pyplot as plt
import pygame

class Renderer:

    def __init__(self, fluid, sim_w):
        self.sim_w = sim_w
        self.scale = sim_w / fluid.width
        self.sim_h = fluid.height * self.scale

        self.fluid = fluid
        self.rgb = np.empty((fluid.width, fluid.height, 3), dtype=np.uint8)

        self.colour_maps = {
            "speed": plt.get_cmap("viridis"),
            "pressure": plt.get_cmap("vanimo"),
            "dye_speed": plt.get_cmap("inferno"),
            "dye_pressure": plt.get_cmap("berlin"),
        }

        self.surface = pygame.Surface((fluid.width, fluid.height))

    def render(self, layer):
        
        if layer == "dye":
            field = self.fluid.dye
            clipped_field = np.clip(field[1:-1, 1:-1], 0, 5)

            img = (clipped_field*255/5).astype(np.uint8)
            self.rgb[:, :, 0] = img
            self.rgb[:, :, 1] = img
            self.rgb[:, :, 2] = img
        elif layer == "speed":
            field = self.fluid.speed()
            clipped_field = np.clip(field[1:-1, 1:-1], 0, 10)

            self.rgb[:] = (self.colour_maps["speed"](clipped_field/10)[:, :, :3]*255).astype(np.uint8)
        elif layer == "pressure":
            field = self.fluid.p
            clipped_field = np.clip(field[1:-1, 1:-1], -100, 100)

            self.rgb[:] = (self.colour_maps["pressure"]((clipped_field + 100)/200)[:, :, :3]*255).astype(np.uint8)

        elif layer == "dye+speed":
            speed = self.fluid.speed()
            clipped_speed = np.clip(speed[1:-1, 1:-1], 0, 10)

            dye = self.fluid.dye
            clipped_dye = np.clip(dye[1:-1, 1:-1], 0, 5)

            self.rgb[:] = np.clip((self.colour_maps["dye_speed"](clipped_speed/10)[:, :, :3]*255)+ np.repeat((clipped_dye*255/5)[:, :, None], 3, axis=2), 0, 255).astype(np.uint8)

        elif layer == "dye+pressure":
            pressure = self.fluid.p
            clipped_pressure = np.clip(pressure[1:-1, 1:-1], -100, 100)

            dye = self.fluid.dye
            clipped_dye = np.clip(dye[1:-1, 1:-1], 0, 5)

            self.rgb[:] = np.clip((self.colour_maps["dye_pressure"]((clipped_pressure + 100)/200)[:, :, :3]*255)+ np.repeat((clipped_dye*255/5)[:, :, None], 3, axis=2), 0, 255).astype(np.uint8)

        return self.rgb
    
    def draw(self, screen, selected_layer):
        self.render(selected_layer)

        pygame.surfarray.blit_array(self.surface, self.rgb)

        scaled = pygame.transform.scale(self.surface, (self.sim_w, self.sim_h))

        screen.blit(scaled, (0, 0))

    def draw_scene(self, screen, scene, tool):
        '''
        for object in scene.boundary_objects:
            pygame.draw.polygon(screen, (255,0,0), object.vertices)
        '''

        if tool.type == "boundary":
            if tool.drawing and len(tool.current_vertices) > 1:

                pygame.draw.lines(screen, (0,255,0), False, tool.current_vertices)

                if tool.mouse_pos is not None:
                    pygame.draw.line(
                        screen,
                        (0,255,0),
                        tool.current_vertices[-1],
                        tool.mouse_pos
                    )
