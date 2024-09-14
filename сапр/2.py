import json

from tools import Matrix

tasks = json.load(open('2.json', 'r', encoding='utf-8'))

number = input('Введите вариант задания: ')

variant = tasks.get(number)

if variant is None:
    raise KeyError(f"{number} is not a valid key for varints variable.")

matrix_a, matrix_b, result = variant.values()

A = Matrix(matrix_a).append(matrix_b)

print(A)