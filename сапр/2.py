import json
import numpy as np
from tools import Matrix


def gauss_method(matrix: Matrix) -> Matrix:
    """
    Прямой ход метода Гаусса для приведения матрицы к треугольному виду.

    :param matrix: Матрица системы уравнений с последним столбцом — вектором свободных членов.
    :type matrix: Matrix
    :return: Матрица, приведенная к треугольному виду, или None, если решение невозможно.
    :rtype: Matrix
    """
    n = len(matrix)

    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))

        if i != max_row:
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        pivot = matrix[i][i]
        if pivot == 0:
            print("Предупреждение: Матрица вырожденная, метод Гаусса не применим.")
            return None

        matrix[i] = [m / pivot for m in matrix[i]]

        for j in range(i + 1, n):
            factor = matrix[j][i]
            matrix[j] = [matrix[j][k] - factor * matrix[i][k] for k in range(n + 1)]

    return matrix


def defer_gauss(matrix: Matrix) -> list:
    """
    Обратный ход метода Гаусса для нахождения решений системы.

    :param matrix: Матрица после прямого хода метода Гаусса.
    :type matrix: Matrix
    :return: Вектор решений системы уравнений или None, если входная матрица None.
    :rtype: list
    """
    if matrix is None:
        return None

    n = len(matrix)
    solution = [0] * n

    for i in range(n - 1, -1, -1):
        solution[i] = matrix[i][n] - sum(matrix[i][j] * solution[j] for j in range(i + 1, n))
        solution[i] = round(solution[i], 2)

    return solution


def LU_method(matrix: Matrix, b: list) -> list:
    """
    Решение системы уравнений методом LU-разложения.

    :param matrix: Квадратная матрица системы.
    :type matrix: Matrix
    :param b: Вектор свободных членов.
    :type b: list
    :return: Вектор решений системы уравнений.
    :rtype: list
    """
    n = len(matrix)
    L = Matrix([[0.0] * n for _ in range(n)])
    U = Matrix([[0.0] * n for _ in range(n)])

    for i in range(n):
        for k in range(i, n):
            sum_upper = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = matrix[i][k] - sum_upper
        for k in range(i, n):
            if i == k:
                L[i][i] = 1
            else:
                sum_lower = sum(L[k][j] * U[j][i] for j in range(i))
                L[k][i] = (matrix[k][i] - sum_lower) / U[i][i]

    y = [0.0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

    return x


def calculate_spectral_radius(matrix: Matrix) -> float:
    """
    Вычисляет спектральный радиус матрицы.

    :param matrix: Матрица для вычисления спектрального радиуса.
    :type matrix: Matrix
    :return: Спектральный радиус.
    :rtype: float
    """
    eigenvalues = np.linalg.eigvals(matrix)
    return max(abs(eigenvalues))


def check_convergence_jacobi(matrix: Matrix) -> bool:
    """
    Проверяет условие сходимости для метода Якоби.

    :param matrix: Квадратная матрица системы.
    :type matrix: Matrix
    :return: True, если метод сходится, иначе False.
    :rtype: bool
    """
    n = len(matrix)
    D = np.diag(np.diag(matrix))
    L = np.tril(matrix, -1)
    U = np.triu(matrix, 1)
    B = -np.linalg.inv(D).dot(L + U)
    spectral_radius = calculate_spectral_radius(B)
    return spectral_radius < 1


def check_convergence_seidel(matrix: Matrix) -> bool:
    """
    Проверяет условие сходимости для метода Зейделя.

    :param matrix: Квадратная матрица системы.
    :type matrix: Matrix
    :return: True, если метод сходится, иначе False.
    :rtype: bool
    """
    n = len(matrix)
    D = np.diag(np.diag(matrix))
    L = np.tril(matrix, -1)
    U = np.triu(matrix, 1)
    B = -np.linalg.inv(D + L).dot(U)
    spectral_radius = calculate_spectral_radius(B)
    return spectral_radius < 1


def seidel_method(matrix: Matrix, b: list, tol=1e-5, max_iterations=1000) -> list:
    """
    Решение системы методом Зейделя.

    :param matrix: Квадратная матрица системы.
    :type matrix: Matrix
    :param b: Вектор свободных членов.
    :type b: list
    :param tol: Точность (условие прекращения итераций).
    :type tol: float
    :param max_iterations: Максимальное число итераций.
    :type max_iterations: int
    :return: Вектор решений системы или сообщение о несходимости.
    :rtype: list
    """
    if not check_convergence_seidel(matrix):
        return "Метод Зейделя не сходится для данной матрицы."

    n = len(matrix)
    x = [0.0] * n

    for it in range(max_iterations):
        x_new = x.copy()
        for i in range(n):
            sum1 = sum(matrix[i][j] * x_new[j] for j in range(i))
            sum2 = sum(matrix[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - sum1 - sum2) / matrix[i][i]

        if max(abs(x_new[i] - x[i]) for i in range(n)) < tol:
            return [round(val, 2) for val in x_new]

        x = x_new

    return "Метод Зейделя не сошелся за заданное число итераций."


def jacobi_method(matrix: Matrix, b: list, tol=1e-5, max_iterations=1000) -> list:
    """
    Решение системы методом Якоби.

    :param matrix: Квадратная матрица системы.
    :type matrix: Matrix
    :param b: Вектор свободных членов.
    :type b: list
    :param tol: Точность (условие прекращения итераций).
    :type tol: float
    :param max_iterations: Максимальное число итераций.
    :type max_iterations: int
    :return: Вектор решений системы или сообщение о несходимости.
    :rtype: list
    """
    if not check_convergence_jacobi(matrix):
        return "Метод Якоби не сходится для данной матрицы."

    n = len(matrix)
    x = [0.0] * n

    for it in range(max_iterations):
        x_new = [0.0] * n
        for i in range(n):
            sum1 = sum(matrix[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - sum1) / matrix[i][i]

        if max(abs(x_new[i] - x[i]) for i in range(n)) < tol:
            return [round(val, 2) for val in x_new]

        x = x_new

    return "Метод Якоби не сошелся за заданное число итераций."


# Основная часть программы
tasks = json.load(open('answers/2.json', 'r', encoding='utf-8'))

number = input('Введите вариант задания: ')
variant = tasks.get(number)

if variant is None:
    print(f"Предупреждение: Вариант {number} не найден.")
else:
    matrix_a, matrix_b, result = variant.values()

    A = Matrix(matrix_a)
    b = matrix_b

    print("Исходная матрица A:")
    print(A)

    solution_lu = LU_method(A, b)
    gauss = gauss_method(A.append(matrix_b))
    solution_seidel = seidel_method(A, b)
    solution_jacobi = jacobi_method(A, b)

    print("По методу Гаусса:", defer_gauss(gauss) if gauss else "Метод не применим.")
    print("Решение системы методом LU-разложения:", solution_lu or "Метод не применим.")
    print("Метод Зейделя:", solution_seidel)
    print("Метод Якоби:", solution_jacobi)
    print("Правильный ответ:", result)
