import json


def func(x: float) -> float:
    return sin(x) - x


def method_1(interval: list[float], equation: str, epsilon=1e-5) -> float:
    a, b = interval
    x0 = (a + b) / 2  # Середина отрезка

    # Условие выхода: если длина отрезка меньше 2 * epsilon, возвращаем середину
    if abs(b - a) < 2 * epsilon:
        return x0

    # Проверка знаков и рекурсивный вызов метода половинного деления
    if func(a) * func(x0) < 0:
        return method_1([a, x0], equation, epsilon)  # Применяем метод к отрезку [a, x0]
    elif func(x0) * func(equation, b) < 0:
        return method_1([x0, b], equation, epsilon)  # Применяем метод к отрезку [x0, b]
    else:
        # Если корня на отрезке нет, выбрасываем исключение
        raise ValueError("Корень не найден на данном интервале.")


# Загрузка задач
tasks = json.load(open('answers/3.json', 'r', encoding='utf-8'))

number = input('Введите вариант задания: ')

variant = tasks.get(number)

if variant is None:
    raise KeyError(f"{number} не является допустимым ключом.")

# Получаем уравнение, ответ и интервал для выбранного варианта
equation, ans, interval = variant["equation"], variant["answer"], variant["interval"]

# Пример использования
root = method_1(interval, equation)
print(f"Найденный корень: {root}")
