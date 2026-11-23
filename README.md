# 2D Navier–Stokes Solver
 
An interactive Python solver for incompressible flow in two dimensions on a staggered grid. You can draw obstacles and inject dye while it runs, and watch vortices shed in the wakes.
 
![Flow past a triangle and a square](images/velocity_field.jpg)
 
*Flow past a triangle and a square drawn in the app, showing vortex shedding in the wakes.*
 
## Method
 
The solver advances the incompressible Navier–Stokes equations
 
$$
\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u} = -\frac{1}{\rho}\nabla p + \frac{\mu}{\rho}\nabla^2\mathbf{u} + \mathbf{F}, \qquad \nabla\cdot\mathbf{u} = 0,
$$
 
with an operator-splitting (fractional step) scheme. Each time step does the following, applying the boundary conditions after every stage:
 
1. **Advection:** semi-Lagrangian. Each velocity sample is traced backwards along the flow for one time step, and the velocity is bilinearly interpolated at the departure point. This stays stable for large time steps.
2. **Diffusion:** explicit, using the five-point finite-difference Laplacian.
3. **Body force:** an optional force field $\mathbf{F}$ is added.
4. **Pressure projection:** the pressure Poisson equation $\nabla^2 p = \frac{\rho}{\Delta t}\nabla\cdot\mathbf{u}$ is solved with 50 Jacobi iterations. Subtracting $\frac{\Delta t}{\rho}\nabla p$ then makes the velocity divergence-free, so mass is conserved. The mean pressure is removed afterwards to fix the arbitrary constant.
5. **Dye:** a passive dye field is advected with the same semi-Lagrangian scheme for visualisation.
**Grid.** Velocities are stored on a staggered (MAC) grid: $u$ on vertical cell faces, $v$ on horizontal cell faces, and pressure and dye at cell centres. This couples velocity and pressure correctly and avoids the checkerboard pressure modes of a collocated grid.
 
**Boundaries.** Each cell face can be set as no-slip, free-slip, inflow or outflow, using ghost cells. Obstacles drawn as polygons are converted into no-slip boundary faces.
 
## Usage
 
Requires Python 3 with NumPy, Matplotlib, pygame and pygame_gui:
 
```bash
pip install numpy matplotlib pygame pygame_gui
python main.py
```
 
The default scene has a uniform inflow on the left and an outflow on the right.
 
- **Layer menu:** choose what to display: dye, speed, pressure, or dye overlaid on speed or pressure.
- **Dye tool:** click to inject dye.
- **Boundary tool:** click to place the vertices of an obstacle, then press **Enter** to close the polygon and add it to the flow.
Fluid properties (`rho`, `mu`), grid size and time step are set at the top of `main.py`.
