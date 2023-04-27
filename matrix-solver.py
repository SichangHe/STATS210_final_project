from fractions import Fraction
import sys
import numpy


#! set variables, take argv[1] as number of url {
n = int(sys.argv[1])  # number of url
a = [[] for i in range(n)]
b = [0 for i in range(n-1)]
b.append(1)
#! }

#! load the transition matrix file argv[2] into 2D list `a`
# ! transpose it, subtract the diagonal by 1, and make the last row all 1 {
i = 0
with open(sys.argv[2]) as file:
    for line in file:
        numbers = line.split(' ')   # list of numbers in this line
        j = 0
        for number in numbers:
            a[j].append(numpy.float64(Fraction(number)))
            j += 1
        a[i][i] -= 1  # subtract the diagonal with 1
        i += 1
a[-1] = [1 for i in range(n)]
# debug
# for line in a:
#     print(" ".join(str(entry) for entry in line))
#! }

#! solve using numpy {
A = numpy.array(a)
B = numpy.array(b)
numpy.set_printoptions(threshold=numpy.inf)
print(numpy.linalg.solve(A, B))
#! }
