from typing import Callable


def f(x: float) -> float:
    return x ** 2 - 2


# Границы интегрирования
a, b = 0, 5


# Исправленный метод Симпсона
def simpson_method(n: int) -> float:
    h = (b - a) / n
    integral = f(a) + f(b) + 4 * sum(f(a + i * h) for i in range(1, n, 2)) + 2 * sum(
        f(a + i * h) for i in range(2, n - 1, 2))
    return (h / 3) * integral


def newton_method(n: int) -> float:
    h = (b - a) / (3 * n)
    y0 = f(a)
    yn = f(b)

    # Вычисление суммы
    sum_3i_minus_2 = sum(f(a + (3 * i - 2) * h) for i in range(1, n + 1))
    sum_3i_minus_1 = sum(f(a + (3 * i - 1) * h) for i in range(1, n + 1))
    sum_3i = sum(f(a + 3 * i * h) for i in range(1, n + 1))

    # Применение формулы
    result = (3 * (b - a) / (24 * n)) * (y0 - yn + 3 * (sum_3i_minus_2 + sum_3i_minus_1) + 2 * sum_3i)

    return result


# Функции интегрирования для других методов
def left_method(n: int) -> float:
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n))


def right_method(n: int) -> float:
    h = (b - a) / n
    return h * sum(f(a + (i + 1) * h) for i in range(n))


def midpoint_method(n: int) -> float:
    h = (b - a) / n
    return h * sum(f(a + (i + 0.5) * h) for i in range(n))


def trap_method(n: int) -> float:
    h = (b - a) / n
    return h * (0.5 * f(a) + 0.5 * f(b) + sum(f(a + i * h) for i in range(1, n)))


# Проверка для каждого метода
methods = {
    'left': left_method,
    'right': right_method,
    'midpoint': midpoint_method,
    'trap': trap_method,
    'simpson': simpson_method,
    'newton': newton_method
}


def checker(n: int, func: Callable, *, e=0.001, p: int = 1) -> bool:
    """
    Проверка верности условия автоматического шага.
    :param func: интегральная функция
    :param n: количество отрезков, на которые бьем интеграл
    :param e: константа (необходимая точность)
    :param p: порядок точности квадратурной формулы.
    :return: Результат проверки на точность
    """
    return (1 / ((2 ** p) - 1)) * abs(func(n) - func(2 * n)) < e


# Функция поиска оптимального n для каждого метода
def search_n(step: int, *, p: int = 1, func: Callable = left_method, e: float = 0.001) -> int:
    """
    Функция для поиска оптимального n. Используется модифицированный алгоритм бинарного поиска.
    :param p: порядок точности квадратурной формулы
    :param func: функция метода интегрирования
    :param e: допустимая погрешность. Задана по умолчанию.
    :param step: шаг, с которым мы будем двигаться для поиска n.
    :return: необходимое n для заданной погрешности.
    """

    num = max(step, 2)
    while not checker(num, func, e=e, p=p):
        num *= 2

    low, high = num // 2, num

    while low < high:
        mid = (low + high) // 2
        if checker(mid, func, e=e, p=p):
            high = mid
        else:
            low = mid + step

    return low


# Основная часть программы
for key, func in methods.items():
    p = 1 if key in ['left', 'right'] else (2 if key in ['midpoint', 'trap'] else 4)
    n = search_n(step=1, p=p, func=func)
    result = func(n)
    print(f'По методу: {key}: результат интегрирования = {result}')
