import os
import sys


# directory with all saved spider output, must have '/' at the end
dir = sys.argv[1]
with os.scandir(dir) as folder:
    for file in folder:
        try:
            read = open(dir+file.name).read()
            if read == '':
                os.remove(dir+file.name)
        finally:
            continue
