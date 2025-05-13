# Generic imports
import os
import sys

# Custom imports
from dem.app.app      import *
from dem.src.core.run import *
import dem.app.config

########################
# Run dem simulation
########################
if __name__ == '__main__':

    # Check command-line input
    if (len(sys.argv) == 3):
        app_name = sys.argv[1]
        dem.app.config.np_path = sys.argv[2]
    elif (len(sys.argv) == 2) and (sys.argv[1]!="dam_break" and sys.argv[1]!="column_collapse1"):
        app_name = sys.argv[1]
    else:
        print('Command line error, please use as follows:')
        print('for column collapse: python3 start.py app_name [save_path]')
        print('for other tasks: python3 start.py app_name')
        exit(-1)

    # Instanciate app
    app = app_factory.create(app_name)

    # Run
    run(app, dem.app.config.np_path if app_name == "column_collapse1" else None)
