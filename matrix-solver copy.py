from fractions import Fraction
import numpy


n = 0  # number of pages

# load the transition matrix into a 2D list "trans"
trans = []
i = 0
with open('/Users/sichanghe/Desktop/STATS 210/presentation/fraction-matrix-stript.txt') as file:
    for line in file:
        trans.append([])
        n += 1  # record the number of pages
        numbers = line.split(' ')
        for number in numbers:
            if number != '\n' and number != '':
                trans[i].append(Fraction(number))
        i += 1
# print(trans)

# for Ax=b
# create the A
a = []
for i in range(n):
    trans[i][i] -= 1  # subtract the diagonal with 1
    trans[i][-1] = 1  # the last column of trans is all 0's
    a.append([])
    for j in range(n):
        a[i].append(float(trans[j][i]))
print("A:\n\\begin{bmatrix}")
for row in a:
    for number in row:
        if number == 0:
            print(0, end='&')
        elif number == 1:
            print(1, end='&')
        else:
            print("\\frac{", str(number).replace('/', '}{'), end="}&")
    print("\b\\\\[6pt]")
print("\\end{bmatrix}")
A = numpy.array(a)
# print(A)

# create the B
b = [0 for i in range(n-1)]
b.append(1)
# print("\nB:\n\\begin{bmatrix}")
# for number in b:
#     print(number, end='\\\\\n')
# print("\\end{bmatrix}")
B = numpy.array(b)

print("\n", numpy.linalg.solve(A, B))
