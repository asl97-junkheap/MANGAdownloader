import os

# get current folder
folder = os.path.dirname(os.path.realpath(__file__))

# find all module in folder that doesn't start with _
files = [filename
    for filename in os.listdir(folder)
        if os.path.isfile(os.path.join(folder,filename))
            and not filename.startswith("_")
            and filename.endswith(".py")
    ]

# remove the extension from file name and add it to __all__
__all__ = [os.path.basename(filename)[:-3] for filename in files]

# import everything in __all__ into local namespace
from . import *

# finally remove os and the other stuff
del os, folder, files
