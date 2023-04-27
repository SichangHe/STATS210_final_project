from fractions import Fraction
import random


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
        # if(sum(trans[i]) == 0):   # dead end
        #     trans[i][i] = 1
        i += 1

# to record the times that the page get visited
arrival = [0 for i in range(n)]
r = Fraction(1, n)

# decide which page to jump to from x


def jump(x):
    y = -1  # page to go, -1 because the first loop always happen
    i = 0  # anti-cap
    if 10*random.random() < 1:   # random URL
        a = random.random()     # cap
        # print("going random, a = ", a)
        while i <= a:
            i += r
            y += 1
        return y

    # random hyperlink
    a = random.random()
    # print("going links, a = ", a)
    while i <= a and y < n-1:
        y += 1
        # print('x = ', x, ', y = ', y)
        i += trans[x][y]
        # print("i += ", trans[x][y], " = ", i)
    return y


# random surf
s = 0
trails = 1048575   # the number of jumps
for j in range(trails):
    arrival[s] += 1
    # print(arrival)
    s = jump(s)
arrival[s] += 1
# print(arrival)

# the raw arrival rate
raw = []
for page in arrival:
    raw.append(Fraction(page, trails+1))

# the adjusted arrival rate
adj = []
pointNine = Fraction(1, 9)
tenNinth = Fraction(10, 9)
for rate in raw:
    adj.append(tenNinth*rate-pointNine*r)

print("index,arrival,raw(frac),raw(float),adj(frac),adj(float)")
for i in range(n):
    print(i+1, ',', arrival[i], ',', raw[i], ',', float(
        raw[i]), ',', adj[i], ',', float(adj[i]))
