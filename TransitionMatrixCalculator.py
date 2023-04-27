import sys
from sortedcontainers import SortedList  # , SortedDict
import os
from fractions import Fraction


#! take argv[1], file with all url and load to list, create empty matrix {
urlFile = sys.argv[1]  # file with all urls sorted
allUrls = SortedList()
allUrls.update(open(urlFile).read().split('\n'))
if allUrls.__contains__(""):
    allUrls.discard("")
matrix = [[Fraction()]*(allUrls.__len__()) for i in range(allUrls.__len__())]
#! }

#! take argv[2], directory with all record, look through every file inside and fill the matrix {
# directory with all saved spider output
dir = sys.argv[2]
if dir[-1] != '/':
    dir = dir+'/'       # for later open file
with os.scandir(dir) as folder:
    for file in folder:
        presentIndex = allUrls.index(
            file.name.replace('÷', '/').replace('…', ':').replace('∞', '%').replace('¿', '?').replace('.jl', ''))
        read = open(dir+file.name).read()
        found = []
        for url in allUrls:
            if url in read:
                found.append(allUrls.index(url))
        # rate = 1/found.__len__()
        rate = Fraction(1, found.__len__())
        for f in found:
            matrix[presentIndex][f] = rate
#! }

#! print the matrix {
for line in matrix:
    print(" ".join(str(entry) for entry in line))
#! }
