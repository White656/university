from math import sin, cos, exp


def func(x):
    """
    Вычисляет значение функции f(x) = sin(x) - x + 0.15.

    :param x: float, точка, в которой вычисляется значение функции
    :return: float, значение функции в точке x
    """
    return sin(x) - x + 0.15


def first_derivative(x):
    """
    Вычисляет значение первой производной функции f'(x) = cos(x) - 1.

    :param x: float, точка, в которой вычисляется значение производной
    :return: float, значение первой производной в точке x
    """
    return cos(x) - 1


def transformed_function(x):
    """
    Трансформированная функция для метода простой итерации: φ(x) = sin(x) + 0.15.

    :param x: float, точка, в которой вычисляется значение функции
    :return: float, значение функции φ(x) в точке x
    """
    return sin(x) + 0.15


def bisection_method(func, left, right, tolerance):
    """
    Находит корень уравнения методом деления интервала пополам.

    :param func: function, непрерывная функция, для которой ищется корень
    :param left: float, левая граница интервала
    :param right: float, правая граница интервала
    :param tolerance: float, требуемая точность
    :return: tuple, корень уравнения и количество итераций
    """
    if func(left) * func(right) >= 0:
        raise ValueError("Функция должна иметь разные знаки на концах интервала")

    iterations = 0

    while (right - left) / 2 > tolerance:
        midpoint = (left + right) / 2
        if func(midpoint) == 0:  # Найден точный корень
            return midpoint, iterations
        elif func(left) * func(midpoint) < 0:
            right = midpoint  # Корень лежит в [left, midpoint]
        else:
            left = midpoint  # Корень лежит в [midpoint, right]
        iterations += 1

    # Возвращаем среднюю точку последнего интервала как приближённый корень
    return (left + right) / 2, iterations


def secant_method(func, func_derivative, left, right, tolerance):
    """
    Находит корень уравнения методом хорд с учетом производных.

    :param func: function, непрерывная функция, для которой ищется корень
    :param func_derivative: function, производная функции func
    :param left: float, левая граница интервала
    :param right: float, правая граница интервала
    :param tolerance: float, требуемая точность
    :return: tuple, корень уравнения и количество итераций
    """
    if func(left) * func(right) >= 0:
        raise ValueError("Функция должна иметь разные знаки на концах интервала")

    iterations = 0
    x_prev = left
    x_curr = right

    while abs(x_curr - x_prev) > tolerance:
        if func(x_curr) == func(x_prev):
            raise ZeroDivisionError("Деление на ноль при вычислении нового приближения")

        # Проверяем знак произведения первой и второй производных
        if func_derivative(x_curr) * func_derivative(x_prev) < 0:
            # Используем модифицированную формулу, если f'(x) * f''(x) < 0
            x_next = x_curr - func(x_curr) * (x_curr - left) / (func(x_curr) - func(left))
        else:
            # Стандартная формула метода хорд
            x_next = x_curr - func(x_curr) * (x_curr - x_prev) / (func(x_curr) - func(x_prev))

        x_prev = x_curr
        x_curr = x_next
        iterations += 1

    return x_curr, iterations


def newton_method(func, first_derivative, second_derivative, initial_guess, tolerance):
    """
    Находит корень уравнения методом Ньютона (касательных) с учетом условий для производных.

    :param func: function, непрерывная функция, для которой ищется корень
    :param first_derivative: function, производная функции func
    :param second_derivative: function, вторая производная функции func
    :param initial_guess: float, начальное приближение корня
    :param tolerance: float, требуемая точность
    :return: tuple, корень уравнения и количество итераций
    """
    # Проверяем начальное приближение на выполнение условия f(x0) * f''(x0) > 0
    if func(initial_guess) * second_derivative(initial_guess) <= 0:
        raise ValueError("Начальное приближение x0 не удовлетворяет условию f(x0) * f''(x0) > 0")

    iterations = 0
    x_current = initial_guess

    while True:
        # Вычисляем новое приближение по формуле метода Ньютона
        x_next = x_current - func(x_current) / first_derivative(x_current)

        # Проверяем условие сходимости
        if abs(x_next - x_current) < tolerance:
            break

        x_current = x_next
        iterations += 1

    return x_next, iterations


def fixed_point_iteration(transformed_function, initial_guess, tolerance, derivative_function=None):
    """
    Находит корень уравнения методом простой итерации.

    :param transformed_function: function, преобразованная функция (phi(x))
    :param initial_guess: float, начальное приближение
    :param tolerance: float, требуемая точность
    :param derivative_function: function, производная функции phi(x), используется для проверки условия сходимости
    :return: tuple, корень уравнения и количество итераций
    """
    if derivative_function:
        # Проверяем условие |phi'(x)| < 1 на интервале
        if not (0 < abs(derivative_function(initial_guess)) < 1):
            raise ValueError("Условие сходимости |phi'(x)| < 1 не выполняется. Метод может не сходиться.")

    iterations = 0
    x_current = initial_guess

    while True:
        x_next = transformed_function(x_current)

        # Проверяем критерий сходимости
        if abs(x_next - x_current) < tolerance:
            break

        x_current = x_next
        iterations += 1

    return x_next, iterations


# Основные параметры
left_bound = 0.5
right_bound = 1
precision = 0.0001

# Выполнение методов
# Метод деления пополам
root_bisection, iter_bisection = bisection_method(func, left_bound, right_bound, precision)
print(f'Корень (метод деления пополам): {root_bisection}, итерации: {iter_bisection}')

# Метод секущих (хорд)
root_secant, iter_secant = secant_method(func, first_derivative, left_bound, right_bound, precision)
print(f'Корень (метод секущих): {root_secant}, итерации: {iter_secant}')

# Метод Ньютона (касательных)
root_newton, iter_newton = newton_method(func, first_derivative, lambda x: -sin(x), right_bound, precision)
print(f'Корень (метод Ньютона): {root_newton}, итерации: {iter_newton}')

# Метод простой итерации
root_fixed_point, iter_fixed_point = fixed_point_iteration(transformed_function, left_bound, precision,
                                                           lambda x: cos(x))
print(f'Корень (метод простой итерации): {root_fixed_point}, итерации: {iter_fixed_point}')
