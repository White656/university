import json

from tools import Matrix


def gauss_method(matrix: Matrix) -> Matrix:
    n = matrix.shape[0]
    for i in range(n):
        pivot = matrix[i][i]
        if pivot == 0:
            raise ValueError("Матрица вырожденная, нет единственного решения")
        matrix[i] = [m / pivot for m in matrix[i]]

        for j in range(i + 1, n):
            factor = matrix[j][i]
            matrix[j] = [matrix[j][k] - factor * matrix[i][k] for k in range(n + 1)]

    solution = [0] * n

    for i in range(n - 1, -1, -1):
        solution[i] = matrix[i][n] - sum(matrix[i][j] * solution[j] for j in range(i + 1, n))
        solution[i] = round(solution[i], 2)

    return solution


tasks = json.load(open('2.json', 'r', encoding='utf-8'))

number = input('Введите вариант задания: ')

variant = tasks.get(number)

if variant is None:
    raise KeyError(f"{number} is not a valid key for varints variable.")

matrix_a, matrix_b, result = variant.values()

A = Matrix(matrix_a).append(matrix_b)

print(A)

print("По методу Гаусса:", gauss_method(A))
print("Правильный ответ:", result)
