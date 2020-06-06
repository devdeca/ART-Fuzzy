from numpy import ones, zeros


def complement(matrix):
    for line in matrix:
        half = []
        for inp in line:
            half.append(1 - inp)
        line.extend(half)
    return matrix


def run(vector, weights):
    responses = []
    for weight in weights:
        total = 0
        for pos, element in enumerate(vector):
            total = total + min(element, weight[pos])

        responses.append(total / (alpha + sum(weight)))

    return responses


def choose_category(start, responses):
    chosen = start
    for index, response in enumerate(responses):
        if response > responses[chosen]:
            chosen = index
    return chosen


def is_category_valid(line, weights, rho):
    total = 0
    for current, element in enumerate(line):
        total = total + min(element, weights[current])

    x = total / sum(line)
    return x >= rho


def get_valid_category(vector, weights, responses, rho):
    current = choose_category(0, responses)
    while not is_category_valid(vector, weights[current], rho):
        responses[current] = 0
        current = choose_category(current + 1, responses)
    return current


def get_valid_category_ab(matrix, j, current, inputs):

    while not is_category_valid(matrix[current], wab[current], pba):
        inputs[j] = 0
        j = get_valid_category(a[current], wa, inputs, pa)
    return j


def update(matrix, weights, res_pos):
    weights[res_pos] = beta * [min(element, weights[res_pos][pos])for pos, element in enumerate(matrix[res_pos])] \
                            + (1 - beta) * weights[res_pos]


a = [
    [1, 1],
    [0, 1],
    [1, 0],
    [0, 0],
]

b = [
    [1],
    [0],
    [0],
    [0],
]

a = complement(a)
b = complement(b)

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

for pos in range(len(a)):
    res_a = 0
    res_b = 0

    # ARTb
    res_b = run(b[pos], wb)
    K = get_valid_category(b[pos], wb, res_b, pb)
    yb.append([0 for _ in b])
    yb[pos][K] = 1

    # ARTa
    res_a = run(a[pos], wa)
    J = get_valid_category(a[pos], wa, res_a, pa)
    J = get_valid_category_ab(yb, J, pos, res_a)
    ya.append([0 for _ in a])
    ya[pos][J] = 1

    update(b, wb, K)
    update(a, wa, J)
    wab[J] = [0 for _ in wab[J]]
    wab[J][K] = 1

print("Training:")

print(wa)
print(wb)
print(wab)

test = [0, 0, 1, 1]
res_c = run(test, wa)
print(res_c)
print(get_valid_category(test, wa, res_c, pa))
