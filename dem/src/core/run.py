# Generic imports
import os
import time

# Custom imports
from dem.app.app import *

########################
# Run dem simulation
########################
def run(app, save_path=None):

    # Timer and loop data
    start_time = time.time()
    compute    = True

    # Solve
    print('### Solving')
    while (compute):

        # Printings and plot
        app.printings()
        app.plot()

        # Compute forces
        app.forces()

        # Update positions
        app.update()

        # Check stopping criterion
        compute = app.check_stop()

    # Count time
    if save_path:
        print("save to", save_path)
        app.p.save_x(save_path)
    end_time = time.time()
    print("# Loop time = {:f}".format(end_time - start_time))

    # Perform final operations and outputs
    app.finalize()

