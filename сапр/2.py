import json
from tools import Matrix


def gauss_method(matrix: Matrix) -> Matrix:
    """
    Реализует метод Гаусса для решения системы линейных уравнений.
    Выполняет прямой ход с частичным выбором главного элемента (максимального по модулю в каждом столбце).

    :param matrix: Матрица системы уравнений с правой частью, где последний столбец — вектор свободных членов.
    :type matrix: Matrix
    :return: Преобразованная матрица с приведённым треугольным видом.
    :rtype: Matrix
    :raises ValueError: Если матрица вырожденная (определитель равен нулю).
    """
    n = len(matrix)

    for i in range(n):
        # Поиск максимального элемента в столбце
        max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))

        # Перестановка строк, если максимальный элемент не на главной диагонали
        if i != max_row:
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        pivot = matrix[i][i]
        if pivot == 0:
            raise ValueError("Матрица вырожденная, нет единственного решения")

        # Нормализуем строку, делим на ведущий элемент
        matrix[i] = [m / pivot for m in matrix[i]]

        # Обнуляем элементы ниже текущего ведущего элемента
        for j in range(i + 1, n):
            factor = matrix[j][i]
            matrix[j] = [matrix[j][k] - factor * matrix[i][k] for k in range(n + 1)]

    return matrix


def defer_gauss(matrix: Matrix) -> list:
    """
    Реализует обратный ход метода Гаусса (обратная подстановка) для нахождения решения системы уравнений.

    :param matrix: Матрица системы уравнений после прямого хода метода Гаусса.
    :type matrix: Matrix
    :return: Вектор решений системы уравнений.
    :rtype: list
    """
    n = matrix.shape[0]
    solution = [0] * n

    # Обратная подстановка для нахождения решений
    for i in range(n - 1, -1, -1):
        solution[i] = matrix[i][n] - sum(matrix[i][j] * solution[j] for j in range(i + 1, n))
        solution[i] = round(solution[i], 2)

    return solution


def LU_method(matrix: Matrix, b: list) -> list:
    """
    Реализует метод LU-разложения для решения системы линейных уравнений.

    :param matrix: Квадратная матрица системы уравнений.
    :type matrix: Matrix
    :param b: Вектор свободных членов.
    :type b: list
    :return: Вектор решений системы уравнений.
    :rtype: list
    """
    n = matrix.shape[0]
    L = Matrix([[0.0] * n for _ in range(n)])
    U = Matrix([[0.0] * n for _ in range(n)])

    # LU-разложение: матрица представляется как произведение нижней треугольной L и верхней треугольной U матриц
    for i in range(n):
        for k in range(i, n):
            sum_upper = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = matrix[i][k] - sum_upper

        for k in range(i, n):
            if i == k:
                L[i][i] = 1  # Диагональные элементы матрицы L равны 1
            else:
                sum_lower = sum(L[k][j] * U[j][i] for j in range(i))
                L[k][i] = (matrix[k][i] - sum_lower) / U[i][i]

    # Прямой ход для решения LY = B
    y = [0.0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

    # Обратный ход для решения UX = Y
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

    return x


# Основная часть программы
tasks = json.load(open('answers/2.json', 'r', encoding='utf-8'))

# Запрос варианта задания у пользователя
number = input('Введите вариант задания: ')

variant = tasks.get(number)

if variant is None:
    raise KeyError(f"{number} is not a valid key for varints variable.")

# Извлечение данных: матрица A, вектор b и правильный результат
matrix_a, matrix_b, result = variant.values()

A = Matrix(matrix_a)
b = matrix_b

print("Исходная матрица A:")
print(A)

# Решение системы уравнений методом LU-разложения
solution = LU_method(A, b)

# Решение системы методом Гаусса
gauss = gauss_method(A.append(matrix_b))

# Вывод результатов
print("По методу Гаусса:", defer_gauss(gauss))
print("Решение системы методом LU-разложения:", solution)
print("Правильный ответ:", result)
