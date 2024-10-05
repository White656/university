import json


def func(equation: str) -> float | int:
    return eval(equation)


def method_1(interval: list[float | int]):
    a, b = interval
    x0 = (a - b) / 2
    if func(x0) == 0:
        return x0
    checker_1 = any([func(a) > 0, func(x0) > 0]) or any([func(a) < 0, func(x0) < 0])
    checker_2 = any([func(x0) > 0, func(b) > 0]) or any([func(x0) < 0, func(b) < 0])

    if not checker_1:
        return method_1([a, x0])
    elif checker_2:
        return method_1([x0, b])


tasks = json.load(open('answers/3.json', 'r', encoding='utf-8'))

number = input('Введите вариант задания: ')

variant = tasks.get(number)

if variant is None:
    raise KeyError(f"{number} is not a valid key for varints variable.")

eq, ans, inter = variant.values()
