def generate_sequence(num):
    seq = []
    i = 1
    while len(seq) < num:
        seq.extend([i] * i)
        i += 1
    return seq[:n]


n = int(input("Введите количество элементов: "))
sequence = generate_sequence(n)
print(sequence)
