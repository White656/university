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

    return matrix


def defer_gauss(matrix: Matrix) -> list:
    n = matrix.shape[0]
    solution = [0] * n

    for i in range(n - 1, -1, -1):
        solution[i] = matrix[i][n] - sum(matrix[i][j] * solution[j] for j in range(i + 1, n))
        solution[i] = round(solution[i], 2)

    return solution


def LU_method(matrix: Matrix, b: list) -> list:
    n = matrix.shape[0]
    L = Matrix([[0.0] * n for _ in range(n)])
    U = Matrix([[0.0] * n for _ in range(n)])

    for i in range(n):
        # Формируем верхнетреугольную матрицу U
        for k in range(i, n):
            sum_upper = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = matrix[i][k] - sum_upper

        # Формируем нижнетреугольную матрицу L
        for k in range(i, n):
            if i == k:
                L[i][i] = 1  # Диагональ как 1
            else:
                sum_lower = sum(L[k][j] * U[j][i] for j in range(i))
                L[k][i] = (matrix[k][i] - sum_lower) / U[i][i]

    # Решаем Ly = b
    y = [0.0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

    # Решаем Ux = y
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

    return x


# Пример использования
tasks = json.load(open('answers/2.json', 'r', encoding='utf-8'))

number = input('Введите вариант задания: ')

variant = tasks.get(number)

if variant is None:
    raise KeyError(f"{number} is not a valid key for varints variable.")

matrix_a, matrix_b, result = variant.values()

A = Matrix(matrix_a)
b = matrix_b

print("Исходная матрица A:")
print(A)

solution = LU_method(A, b)

gauss = gauss_method(A.append(matrix_b))

print("По методу Гаусса:", defer_gauss(gauss))
print("Решение системы методом LU-разложения:", solution)
print("Правильный ответ:", result)
