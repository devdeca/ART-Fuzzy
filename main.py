from numpy import ones


def complement(line):
    half = []
    for el in line:
        half.append(1 - el)
    return half


def create_complement(matrix):
    for line in matrix:
        line.extend(complement(line))
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


def update(matrix, weights, res_pos):
    weights[res_pos] = beta * [min(element, weights[res_pos][pos])for pos, element in enumerate(matrix[res_pos])] \
                            + (1 - beta) * weights[res_pos]


# Função para definir se letras estão lado a lado no teclado
def is_lateral(fchar, schar):
    for line in KEYBOARD:
        for pos, char in enumerate(line):
            if char == fchar:
                if schar == line[pos - 1] or schar == line[pos + 1]:
                    return 1
    return 0


# Tratamento das entradas
def input_words(words, weights, rho):
    first_length = len(words[0])

    if first_length != len(words[1]):
        raise Exception('Palavras devem ter o mesmo tamanho!')

    first_input = (first_length - 1) / first_length

    for pos, char in enumerate(words[0]):
        if char != words[1][pos]:
            second_input = is_lateral(char.upper(), words[1][pos].upper())

    inputs = [first_input, second_input]
    inputs.extend(complement(inputs))

    print(f'Teste: {words[0]} vs {words[1]}')
    print(f'Input 1: {first_input}, Input 2: {second_input}')
    res = run(inputs, weights)
    cat = get_valid_category(inputs, weights, res, rho)
    print(f'Output: {res[cat]}({data[cat]})')


KEYBOARD = [['', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', ''],
            ['', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ''],
            ['', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '']]


data = [[1, 1],
        [0.3, 0]]

data = create_complement(data)

ya = []

pa = 0.7
alpha = 0.1
beta = 1

wa = ones((len(data), len(data[0])))

for pos in range(len(data)):
    res_a = 0

    # ARTa
    res_a = run(data[pos], wa)
    J = get_valid_category(data[pos], wa, res_a, pa)
    ya.append([0 for _ in data])
    ya[pos][J] = 1

    update(data, wa, J)

print("Training:")

print(wa)

# Teste 1: soja vs soka. Entradas resultantes 0,75 e 1.
input_words(['soja', 'soka'], wa, pa)

# Teste 2: soja vs soda
input_words(['soja', 'soda'], wa, pa)

# Teste 3: pneumoultramicroscopicossilicovulcanoconiotico vs pneumoultramicroscopicossilicovulcanoconioticp
input_words(['pneumoultramicroscopicossilicovulcanoconiotico', 'pneumoultramicroscopicossilicovulcanoconioticp'], wa, pa)

# Teste 4: james vs jimes
input_words(['james', 'jsmes'], wa, pa)
