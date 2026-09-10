import numpy as np

class Fluid:
    def __init__(self, width, height, rho, mu, boundary, real_width, dt):
        self.width = width
        self.height = height
        self.rho = rho
        self.mu = mu
        self.boundary = boundary
        self.h = real_width/width
        self.dt = dt

        self.u = np.zeros((width + 3, height + 2))
        self.v = np.zeros((width + 2, height + 3))
        self.p = np.zeros((width + 2, height + 2))
        self.dye = np.zeros((width + 2, height + 2))

        self.F_x = np.zeros((width + 2, height + 2))
        self.F_y = np.zeros((width + 2, height + 2))

        self.new_u = self.u.copy()
        self.new_v = self.v.copy()
        self.new_p = self.p.copy()
        self.new_dye = self.dye.copy()

    def update(self):
        self.apply_vel_bcs()

        self.advect()
        self.reassign_layers()
        self.apply_vel_bcs()

        self.diffuse()
        self.reassign_layers()
        self.apply_vel_bcs()

        self.body_force()
        self.reassign_layers()
        self.apply_vel_bcs()

        self.pressure_correction()
        self.reassign_layers()
        self.apply_vel_bcs()

        self.pressure_shift()

        self.advect_dye()

    def reassign_layers(self):
        self.u, self.new_u = self.new_u, self.u 
        self.v, self.new_v = self.new_v, self.v

    def apply_vel_bcs(self):
        i, j = self.boundary.vert_left_no_slip
        self.u[i + 1, j + 1] = 0
        self.v[i, j + 1] = - self.v[i + 1, j + 1]
        self.v[i, j + 2] = - self.v[i + 1, j + 2]

        i, j = self.boundary.vert_right_no_slip
        self.u[i + 1, j + 1] = 0
        self.v[i + 1, j + 1] = - self.v[i, j + 1]
        self.v[i + 1, j + 2] = - self.v[i, j + 2]

        i, j = self.boundary.vert_left_free_slip
        self.u[i + 1, j + 1] = 0
        self.v[i, j + 1] = self.v[i + 1, j + 1]
        self.v[i, j + 2] = self.v[i + 1, j + 2]

        i, j = self.boundary.vert_right_free_slip
        self.u[i + 1, j + 1] = 0
        self.v[i + 1, j + 1] = self.v[i, j + 1]
        self.v[i + 1, j + 2] = self.v[i, j + 2]

        i, j = self.boundary.vert_left_inflow
        self.u[i + 1, j + 1] = self.boundary.u[i, j]
        self.v[i, j + 1] = self.v[i + 1, j + 1]
        self.v[i, j + 2] = self.v[i + 1, j + 2]

        i, j = self.boundary.vert_right_inflow
        self.u[i + 1, j + 1] = self.boundary.u[i, j]
        self.v[i + 1, j + 1] = self.v[i, j + 1]
        self.v[i + 1, j + 2] = self.v[i, j + 2]

        i, j = self.boundary.vert_left_outflow
        self.u[i, j + 1] = self.u[i + 1, j + 1]
        self.v[i, j + 1] = self.v[i + 1, j + 1]
        self.v[i, j + 2] = self.v[i + 1, j + 2]

        i, j = self.boundary.vert_right_outflow
        self.u[i + 1, j + 1] = self.u[i, j + 1]
        self.v[i + 1, j + 1] = self.v[i, j + 1]
        self.v[i + 1, j + 2] = self.v[i, j + 2]

        i, j = self.boundary.horz_up_no_slip
        self.v[i + 1, j + 1] = 0
        self.u[i + 1, j] = - self.u[i + 1, j + 1]
        self.u[i + 2, j] = - self.u[i + 2, j + 1]

        i, j = self.boundary.horz_down_no_slip
        self.v[i + 1, j + 1] = 0
        self.u[i + 1, j + 1] = - self.u[i + 1, j]
        self.u[i + 2, j + 1] = - self.u[i + 2, j]

        i, j = self.boundary.horz_up_free_slip
        self.v[i + 1, j + 1] = 0
        self.u[i + 1, j] = self.u[i + 1, j + 1]
        self.u[i + 2, j] = self.u[i + 2, j + 1]

        i, j = self.boundary.horz_down_free_slip
        self.v[i + 1, j + 1] = 0
        self.u[i + 1, j + 1] = self.u[i + 1, j]
        self.u[i + 2, j + 1] = self.u[i + 2, j]

        i, j = self.boundary.horz_up_inflow
        self.v[i + 1, j + 1] = self.boundary.v[i, j]
        self.u[i + 1, j] = self.u[i + 1, j + 1]
        self.u[i + 2, j] = self.u[i + 2, j + 1]

        i, j = self.boundary.horz_down_inflow
        self.v[i + 1, j + 1] = self.boundary.v[i, j]
        self.u[i + 1, j + 1] = self.u[i + 1, j]
        self.u[i + 2, j + 1] = self.u[i + 2, j]

        i, j = self.boundary.horz_up_outflow
        self.v[i + 1, j] = self.v[i + 1, j + 1]
        self.u[i + 1, j] = self.u[i + 1, j + 1]
        self.u[i + 2, j] = self.u[i + 2, j + 1]

        i, j = self.boundary.horz_down_outflow
        self.v[i + 1, j + 1] = self.v[i + 1, j]
        self.u[i + 1, j + 1] = self.u[i + 1, j]
        self.u[i + 2, j + 1] = self.u[i + 2, j]




    def apply_p_bcs(self):
        i, j = self.boundary.vert_left_boundary
        self.p[i, j + 1] = self.p[i + 1, j + 1]

        i, j = self.boundary.vert_right_boundary
        self.p[i + 1, j + 1] = self.p[i, j + 1]

        i, j = self.boundary.horz_up_boundary
        self.p[i + 1, j] = self.p[i + 1, j + 1]

        i, j = self.boundary.horz_down_boundary
        self.p[i + 1, j + 1] = self.p[i + 1, j]



    def advect(self):

        i, j = self.boundary.vert_none
        x = i * self.h
        y = (j + 0.5) * self.h
        
        u = self.u[i + 1, j + 1]
        v = self.get_v(x, y)
        
        x_prev = x - u*self.dt
        y_prev = y - v*self.dt

        self.new_u[i + 1, j + 1] = self.get_u(x_prev, y_prev)


        i, j = self.boundary.horz_none
        x = (i + 0.5) * self.h
        y = j * self.h
        
        u = self.get_u(x, y)
        v = self.v[i + 1, j + 1]
        
        x_prev = x - u*self.dt
        y_prev = y - v*self.dt

        self.new_v[i + 1, j + 1] = self.get_v(x_prev, y_prev)

    def diffuse(self):
        i, j = self.boundary.vert_none
        lap_u = (self.u[i, j + 1] + self.u[i + 2, j + 1] + self.u[i + 1, j] + self.u[i + 1, j + 2] - 4 * self.u[i + 1, j + 1])/(self.h*self.h)

        self.new_u[i + 1, j + 1] = self.u[i + 1, j + 1] + self.dt * (self.mu / self.rho) * lap_u

        i, j = self.boundary.horz_none
        lap_v = (self.v[i, j + 1] + self.v[i + 2, j + 1] + self.v[i + 1, j] + self.v[i + 1, j + 2] - 4 * self.v[i + 1, j + 1])/(self.h*self.h)

        self.new_v[i + 1, j + 1] = self.v[i + 1, j + 1] + self.dt * (self.mu / self.rho) * lap_v
        
    def body_force(self):
        i, j = self.boundary.vert_none
        self.new_u[i + 1, j + 1] = self.u[i + 1, j + 1] + self.dt * 0.5 * (self.F_x[i, j + 1] + self.F_x[i + 1, j + 1])

        i, j = self.boundary.horz_none
        self.new_v[i + 1, j + 1] = self.v[i + 1, j + 1] + self.dt * 0.5 * (self.F_y[i + 1, j] + self.F_y[i + 1, j + 1])


    def pressure_correction(self):       
        rhs = (self.rho / self.dt) * ((self.u[2:-1, 1:-1] - self.u[1:-2, 1:-1])/self.h + (self.v[1:-1, 2:-1] - self.v[1:-1, 1:-2])/self.h)

        for i in range(50):
            self.pressure_step(rhs)

        self.new_u[1:-1, 1:-1] = self.u[1:-1, 1:-1] - (self.dt / self.rho) * (self.p[1:, 1:-1] - self.p[0:-1, 1:-1]) / self.h

        self.new_v[1:-1, 1:-1] = self.v[1:-1, 1:-1] - (self.dt / self.rho) * (self.p[1:-1, 1:] - self.p[1:-1, 0:-1]) / self.h


    def pressure_step(self, rhs):
        self.new_p[1:-1, 1:-1] = 0.25 * (self.p[0:-2, 1:-1] + self.p[2:, 1:-1] + self.p[1:-1, 0:-2] + self.p[1:-1, 2:] - self.h*self.h*rhs[:,:])
        
        self.p, self.new_p = self.new_p, self.p

        self.apply_p_bcs()

    def pressure_shift(self):
        self.p -= np.mean(self.p)

    def advect_dye(self):
        x = (np.arange(self.width) + 0.5) * self.h
        y = (np.arange(self.height) + 0.5) * self.h

        X, Y = np.meshgrid(x, y, indexing="ij")

        u = self.get_u(X, Y)
        v = self.get_v(X, Y)
        
        x_prev = X - u*self.dt
        y_prev = Y - v*self.dt

        self.new_dye[1:-1, 1:-1] = self.get_dye(x_prev, y_prev)

        self.dye, self.new_dye = self.new_dye, self.dye

    def get_u(self, x, y):
        x = np.clip(x, -1*self.h, (self.width + 1)*self.h) #change this to reflect etc.
        y = np.clip(y, -0.5*self.h, (self.height + 0.5)*self.h)

        i = (x / self.h + 1).astype(np.int32)
        j = (y / self.h + 0.5).astype(np.int32)

        s_x = x / self.h + 1 - i
        s_y = y / self.h + 0.5 - j

        return (1-s_y) * ((1-s_x) * self.u[i, j] + s_x * self.u[i + 1, j]) + s_y * ((1-s_x) * self.u[i, j+1] + s_x * self.u[i + 1, j+1])

    def get_v(self, x, y):
        x = np.clip(x, -0.5*self.h, (self.width + 0.5)*self.h) #change this to reflect etc.
        y = np.clip(y, -1*self.h, (self.height + 1)*self.h)

        i = (x / self.h + 0.5).astype(np.int32)
        j = (y / self.h + 1).astype(np.int32)

        s_x = x / self.h + 0.5 - i
        s_y = y / self.h + 1 - j

        return (1-s_y) * ((1-s_x) * self.v[i, j] + s_x * self.v[i + 1, j]) + s_y * ((1-s_x) * self.v[i, j+1] + s_x * self.v[i + 1, j+1])

    def get_dye(self, x, y):
        x = np.clip(x, -0.5*self.h, (self.width + 0.5)*self.h) #change this to reflect etc.
        y = np.clip(y, -0.5*self.h, (self.height + 0.5)*self.h)

        i = (x / self.h + 0.5).astype(np.int32)
        j = (y / self.h + 0.5).astype(np.int32)

        s_x = x / self.h + 0.5 - i
        s_y = y / self.h + 0.5 - j

        return (1-s_y) * ((1-s_x) * self.dye[i, j] + s_x * self.dye[i + 1, j]) + s_y * ((1-s_x) * self.dye[i, j+1] + s_x * self.dye[i + 1, j+1])


    def speed(self):
        i = np.arange(self.width + 2)
        j = np.arange(self.height + 2)

        I, J = np.meshgrid(i, j, indexing="ij")

        x = (I - 0.5) * self.h
        y = (J - 0.5) * self.h

        u = self.get_u(x, y)
        v = self.get_v(x, y)

        speed = np.sqrt(u*u + v*v)

        return speed
        
