from graphviz import Digraph

# Создание графа
dot = Digraph(format='png', engine='dot')

# Узлы
dot.node("Start", "Начало", shape="oval")
dot.node("Check1", "func(left) * func(right) >= 0?", shape="diamond")
dot.node("Error1", "Ошибка: знаки на концах интервала одинаковы", shape="rectangle")
dot.node("Init", "iterations = 0\nx_prev = left\nx_curr = right", shape="rectangle")
dot.node("Loop", "abs(x_curr - x_prev) > tolerance?", shape="diamond")
dot.node("Check2", "func(x_curr) == func(x_prev)?", shape="diamond")
dot.node("Error2", "Ошибка: деление на ноль", shape="rectangle")
dot.node("DerivativeCheck", "func_derivative(x_curr) * func_derivative(x_prev) < 0?", shape="diamond")
dot.node("Modified", "x_next = x_curr - func(x_curr) * (x_curr - left) / (func(x_curr) - func(left))", shape="rectangle")
dot.node("Standard", "x_next = x_curr - func(x_curr) * (x_curr - x_prev) / (func(x_curr) - func(x_prev))", shape="rectangle")
dot.node("Update", "x_prev = x_curr\nx_curr = x_next\niterations += 1", shape="rectangle")
dot.node("Return", "Вернуть x_curr, iterations", shape="rectangle")
dot.node("End", "Конец", shape="oval")

# Ребра
dot.edge("Start", "Check1")
dot.edge("Check1", "Error1", label="Да")
dot.edge("Check1", "Init", label="Нет")
dot.edge("Init", "Loop")
dot.edge("Loop", "Check2", label="Да")
dot.edge("Loop", "Return", label="Нет")
dot.edge("Check2", "Error2", label="Да")
dot.edge("Check2", "DerivativeCheck", label="Нет")
dot.edge("DerivativeCheck", "Modified", label="Да")
dot.edge("DerivativeCheck", "Standard", label="Нет")
dot.edge("Modified", "Update")
dot.edge("Standard", "Update")
dot.edge("Update", "Loop")
dot.edge("Return", "End")

# Сохранение и визуализация
dot.render("secant_method_flowchart", view=True)