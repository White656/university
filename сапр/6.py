from typing import Callable


def f(x: float) -> float:
    """
    Здесь задается функция необходимого нам интеграла.
    :param x: значение, которое необходимо подставить в интеграл.
    :return: вычисленный интеграл для заданного x.
    """
    return x ** 2 - 2


def checker(n: int | float, func: Callable, *, e=0.001, p: int = 1) -> bool:
    """
    Проверка верности условия автоматического шага.

    :param func: интегральная функция
    :param n: количество отрезков, на которые бьем интеграл
    :param e: константа (необходимая точность)
    :param p: порядок точности квадратурной формулы.
    :return: Результат проверки на точность
    """
    return (1 / ((2 ** p) - 1)) * abs(func(n) - func(2 * n)) < e


def check_method(n: int) -> float:
    """
    Функция для проверки валидности шага при поиске через площади прямоугольников.
    :param n: числовое значение, количество прямоугольников, на которые разбиваем.
    :return: Результат интеграла.
    """
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n - 1))


def integrate(func: Callable, n: int, y: list[float], x: list[float], *, method: str = 'left') -> float:
    """
    Интегрирование различными методами.
    left - метод левых
    right - метод правых
    midpoint - метод серединных
    trap -
    simson -
    newton -

    :param n: Точность
    :param func: Интегральная функция
    :param y: Список значений функции на отрезке
    :param x: Список значений функции на отрезке
    :param method: Метод интегрирования: 'left', 'right', 'midpoint'
    :return: Результат интегрирования
    """
    methods = {
        'left': lambda: h * sum(y[:-1]),
        'right': lambda: h * sum(y[1:]),
        'midpoint': lambda: h * sum(func(xi + h / 2) for xi in x),
        'trap': lambda: h * ((func(a) + func(b)) / 2 + sum(func(xi) for xi in x[1:-1])),
        'simson': lambda: (h / 3) * (
                y[0] + y[-1] + 4 * sum(y[i] for i in range(1, n, 2)) + 2 * sum(y[i] for i in range(2, n - 1, 2))),
        'newton': lambda: (3 / 8 * h) * (y[0] - y[-1] + 3 * sum(y[i - 2] + y[i - 1] for i in range(1, n, 3)) + 2 * sum(
            y[i] for i in range(1, n, 3)))
    }

    if method in methods:
        return methods[method]()
    else:
        raise ValueError("Unsupported method. Use 'left', 'right', 'midpoint','trap', 'simson' or 'newton'.")


def search_n(step: int, *, p: int = 1, func: Callable = check_method, e: float = 0.001) -> int:
    """
    Функция для поиска оптимального n. Используется модифицированный алгоритм бинарного поиска.
    :param p: чет там не помню
    :param func: функция проверки.
    :param e: допустимая погрешность. Задана по умолчанию.
    :param step: шаг, с которым мы будем двигаться для поиска n.
    :return: числовое значение - необходимое n для заданной погрешности.
    """

    num = step

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


a, b = 0, 5

methods = {
    'left': 1,
    'right': 1,
    'midpoint': 2,
    'trap': 2,
    'simson': 4,
    'newton': 4,
}

for key, value in methods.items():
    n = search_n(step=1, p=value)

    h = (b - a) / n
    x_list = [a + i * h for i in range(n)]
    y_list = [f(x) for x in x_list]
    print(f'По методу: {key}: ', integrate(f, n, y_list, x_list, method='left'))
