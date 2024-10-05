from math import sqrt, e


def f1(x: float | int) -> float | int:
    return (3 * (x ** 2)) / (1 + (x ** 2))


def f2(x: float | int) -> float | int:
    return sqrt(1 + ((2 * x) / ((e ** (0.5 * x)) + (x ** 2))))


data = [i / 2 for i in range(0, 13)]
y1_list = []
y2_list = []
result = []

for x in data:
    y1 = f1(x)
    y2 = f2(x)
    y1_list.append(y1)
    y2_list.append(y2)
    result.append(y1 * y2)

sorted_result = sorted(result)

min_y = min(sorted_result)

with open('files/data.txt', 'w') as file:
    file.write("y1_list:\n")
    for y1 in y1_list:
        file.write(f"{y1}\n")

    file.write("\ny2_list:\n")
    for y2 in y2_list:
        file.write(f"{y2}\n")

    file.write("\nSorted result list:\n")
    for res in sorted_result:
        file.write(f"{res}\n")

    file.write(f"\nMinimum value in sorted result list: {min_y}\n")
