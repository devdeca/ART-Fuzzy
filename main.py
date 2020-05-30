from numpy import ones, zeros

a = [
    [1, 0],
    [0, 1],
    [0.5, 0.5],
]

b = [
    [1],
    [0],
    [1]
]

def mirror(matrix):
    for line in matrix:
        half = []
        for inp in line:
            half.append(1 - inp)
        line.extend(half)
    return matrix


a = mirror(a)
b = mirror(b)

ya = []
yb = []

pa = 0.95
pb = 1
pba = 0.95
alpha = 0.1
beta = 1

wa = ones((len(a), len(a[0])))
wb = ones((len(b), len(b[0])))
wab = ones((len(a), len(b)))


def run(vector, weights):
    responses = []
    for weight in weights:
        total = 0
        for pos, element in enumerate(vector):
            total = total + min(element, weight[pos])

        responses.append(total / (alpha + sum(weight)))

    return responses


def max_cat(start, responses):
    chosen = max(responses[start:])
    return responses.index(chosen)


def validate(line, weights, rho):
    total = 0
    for pos, element in enumerate(line):
        total = total + min(element, weights[pos])

    x = total / sum(line)

    return x >= rho


def is_valid(matrix, weights, responses, rho):
    pos = max_cat(0, responses)
    while not validate(matrix[pos], weights[pos], rho):
        if pos + 1 == len(responses):
            return -1
        pos = max_cat(pos, responses)
    return pos


def is_valid_ab(J, pos):

    while not validate(yb[pos], wab[pos], pba):
        if J + 1 == len(res_a):
            return -1
        J = is_valid(a, wa, res_a, pa)
    return J


def update(matrix, weights, res_pos):
    weights[res_pos] = beta * [min(element, weights[res_pos][pos])for pos, element in enumerate(matrix[res_pos])] \
                            + (1 - beta) * weights[res_pos]


for pos in range(len(a)):
    res_a = 0
    res_b = 0

    # ARTb
    res_b = run(b[pos], wb)
    K = is_valid(b, wb, res_b, pb)
    yb.append([0 for _ in b])
    yb[pos][K] = 1
    # ARTa
    res_a = run(a[pos], wa)
    J = is_valid(a, wa, res_a, pa)

    J = is_valid_ab(J, pos)

    if K != -1:
        update(b, wb, K)

    print(J)
    if J != -1:
        update(a, wa, J)
        wab[J] = [0 for _ in wab[J]]
        wab[J][K] = 1
    ya.append([0 for _ in a])
    ya[pos][J] = 1

print(wa)
print(wb)
print(wab)
