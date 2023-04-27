import sys
from sortedcontainers import SortedList  # , SortedDict
import os
from fractions import Fraction
# import numpy

urlFile = sys.argv[2]  # file with all urls sorted, cannot have empty lines
allUrls = SortedList()
allUrls.update(open(urlFile).read().split('\n'))

# i = 0
# for url in allUrls:
#     print(i, ": ", url)
#     i += 1
matrix = [[Fraction()]*(allUrls.__len__()) for i in range(allUrls.__len__())]
# print(matrix)  # debug


# directory with all saved spider output, must have '/' at the end
dir = sys.argv[1]
with os.scandir(dir) as folder:
    for file in folder:
        presentIndex = allUrls.index(
            file.name.replace('÷', '/').replace('…', ':').replace('∞', '%').replace('.jl', ''))
        # print(presentIndex)  # debug
        # print(dir+file.name)  # debug
        read = open(dir+file.name).read()
        found = []
        for url in allUrls:
            if url in read:
                found.append(allUrls.index(url))
        # rate = 1/found.__len__()
        rate = Fraction(1, found.__len__())
        for f in found:
            matrix[presentIndex][f] = rate
        # matrix[presentIndex][presentIndex] -= 1
# print(matrix)
for line in matrix:
    for entry in line:
        print(entry, ' ', end='')
    print()

# matrix[-1] = [1]*(allUrls.__len__())
# A = numpy.array(matrix)
# b = [0]*(allUrls.__len__()-1)
# b.append(1)
# B = numpy.array(b)
# print(A)  # debug
# print(B)  # debug
# solution = numpy.linalg.solve(A, B)
# print(solution)  # debug

# # record these in a sorted dictionary
# ranks = SortedDict(dict(allUrls, solution))
# print(ranks)
