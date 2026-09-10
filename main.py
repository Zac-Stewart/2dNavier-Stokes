from Boundary import Boundary
from Fluid import Fluid
from Scene import Scene
from Renderer import Renderer
from UI import UI

import pygame


rho = 1
mu = 0.01
width = 250
height = 200

SIM_W = 800
PANEL_W = 250

SCALE = SIM_W / width
SIM_H = height * SCALE

WIN_W = SIM_W + PANEL_W
WIN_H = SIM_H

scene = Scene(SIM_W, SIM_H)

boundary = Boundary(width, height)
boundary.set_standard()

fluid = Fluid(width, height, rho, mu, boundary, 10, 0.005)


boundary.bc_vert_type[0 , :] = 3
boundary.u[0 , :] = 5
boundary.bc_vert_type[-1 , :] = 4

'''
boundary.bc_vert_type[-1 , 10:60] = 4

boundary.bc_horz_type[150:200, -1] = 3
boundary.v[150:200, -1] = -10

boundary.bc_vert_type[70, 25:75] = 1
boundary.bc_vert_dir[70, 25:75] = 1
boundary.bc_vert_type[120, 25:75] = 1
boundary.bc_vert_dir[120, 25:75] = 0

boundary.bc_horz_type[70:120, 25] = 1
boundary.bc_horz_dir[70:120, 25] = 1
boundary.bc_horz_type[70:120, 75] = 1
boundary.bc_horz_dir[70:120, 75] = 0
'''


boundary.update_mask()




pygame.init()

screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Fluid")

clock = pygame.time.Clock()


renderer = Renderer(fluid, SIM_W)
ui = UI(renderer.sim_w, renderer.sim_h, PANEL_W)

running = True


while running:
    time_delta = clock.tick(60) / 1000.0

    running = ui.process_events(fluid, scene)

    fluid.update()

    renderer.draw(screen, ui.selected_layer)
    renderer.draw_scene(screen, scene, ui.selected_tool)

    ui.draw(screen, time_delta)

    pygame.display.flip()

pygame.quit()
    






