# Generic imports
import os
import math
import random

# Custom imports
from dem.app.base_app import *
import dem.app.config
### ************************************************
### Dropping of several spheres to check inter-particle contacts
class dam_break(base_app):
    ### ************************************************
    ### Constructor
    def __init__(self,
                 name            = 'dam_break',
                 t_max           = 2.5,
                 dt              = 2.5e-5,
                 plot_freq       = 1000,
                 plot_show       = False,
                 plot_trajectory = False,
                 plot_png        = True):
        super().__init__()

        self.name            = name
        self.t_max           = t_max
        self.dt              = dt
        self.plot_freq       = plot_freq
        self.plot_show       = plot_show
        self.plot_trajectory = plot_trajectory
        self.plot_png        = plot_png

        self.nt      = int(self.t_max/self.dt)
        self.plot_it = 0
       
        data = np.load(dem.app.config.np_path)

        self.np  = data['q'].shape[0]
        self.radius = 0.025

        self.p = particles(np        = self.np,
                           nt        = self.nt,
                           material  = "steel",
                           radius    = self.radius,
                           color     = "b",
                           store     = False,
                           search    = "nearest",
                           rad_coeff = 2.0)
        self.p.x = data['q']

        self.p.e_wall[:] = 0.99
        self.p.e_part[:] = 0.99

        colors = np.array(['r', 'g', 'b', 'c', 'm', 'y', 'k'])
        self.p.c = colors[np.random.randint(0,len(colors),size=self.p.np)]

        self.d = domain_factory.create("rectangle",
                                       x_min      = 0.0,
                                       x_max      = 11.0,
                                       y_min      = 0.0,
                                       y_max      = 4.0,
                                       material   = "steel")
        self.d_lst = [self.d]

        self.path = self.base_path+'/'+self.name
        os.makedirs(self.path, exist_ok=True)

        self.reset()

    ### ************************************************
    ### Reset app
    def reset(self):

        self.it = 0
        self.t  = 0.0
        sep = 4.0*self.radius

        for i in range(self.np):
            self.p.x[i,0] += 5.0 # half of x_max(11)


    ### ************************************************
    ### Compute forces
    def forces(self):

        self.p.reset_forces()
        self.p.collisions(self.dt)
        self.d.collisions(self.p, self.dt)
        self.p.gravity(self.g)
