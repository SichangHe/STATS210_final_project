from fractions import Fraction


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

# initial distribution
r = Fraction(1, n)
a = [r for i in range(n)]
b = []
# print(a, b)

iterations = 256
for i in range(iterations):
    # iterate a and record to b
    b = []
    for y in range(n):      # the state to go
        # print("y = ", y)
        s = 0
        for x in range(n):  # the states come from
            # print("x= ", x)
            # print(type(trans[x][y]), type(a[x]))
            s += trans[x][y]*a[x]
            # print("s + ", trans[x][y]*a[x], " = ", s)
        b.append(s)
    # print(b, sum(b))

    # iterate b and record to a
    a = []
    for y in range(n):      # the state to go
        s = 0
        for x in range(n):  # the states come from
            s += trans[x][y]*b[x]
            # print("s + ", trans[x][y]*b[x], " = ", s)
        a.append(s)
    # print(a, sum(a))

i = 1
print('index,rate(frac),rate(float)')
for rate in a:
    print(i, ',', rate, ',', float(rate))
    i += 1
