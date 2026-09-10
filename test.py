from Boundary import Boundary
from Fluid import Fluid
import matplotlib.pyplot as plt
import cProfile
import numpy as np

def on_press(event):
    global painting
    painting = True

def on_release(event):
    global painting
    painting = False

def on_move(event):
    if not painting:
        return
    if event.inaxes != ax:
        return

    i = int(event.xdata / fluid.h + 1)
    j = int(event.ydata / fluid.h + 1)

    fluid.dye[i-3:i+4, j-3:j+4] += 1.0

rho = 1
mu = 0.01
width = 150
height = 100
boundary = Boundary(width, height)
boundary.set_standard()

fluid = Fluid(width, height, rho, mu, boundary, 10, 0.005)


boundary.bc_vert_type[0 , :] = 3
boundary.u[0 , :] = 10

boundary.bc_vert_type[-1 , :] = 4

boundary.bc_horz_type[:, 0] = 2
boundary.bc_horz_type[:, -1] = 2

boundary.bc_vert_type[70, 25:75] = 1
boundary.bc_vert_dir[70, 25:75] = 1
boundary.bc_vert_type[120, 25:75] = 1
boundary.bc_vert_dir[120, 25:75] = 0

boundary.bc_horz_type[70:120, 25] = 1
boundary.bc_horz_dir[70:120, 25] = 1
boundary.bc_horz_type[70:120, 75] = 1
boundary.bc_horz_dir[70:120, 75] = 0


boundary.update_mask()

plt.ion()

fig, ax = plt.subplots()
img = ax.imshow(fluid.dye.T, origin="lower", extent=[-1 * fluid.h, (fluid.width + 1) * fluid.h, -1 * fluid.h, (fluid.height + 1) * fluid.h])
cbar = fig.colorbar(img, ax=ax)
img.set_clim(0, 10)

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_move)

painting = False

cProfile.run('fluid.update()')

while False:

    if not painting:
        fluid.update()

        img.set_data(fluid.dye.T)  

    plt.pause(0.001)          

plt.ioff()
plt.show()





