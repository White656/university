import copy
from typing import List, Union

MatrixType = List[List[Union[int, float]]]
ListType = List[Union[int, float]]


class Matrix:
    __slots__ = ('data',)

    def __init__(self, data: MatrixType):
        if not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Все строки матрицы должны быть одной длины")
        self.data = copy.deepcopy(data)

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if self.shape() != other.shape():
            raise ValueError("Матрицы должны быть одинакового размера для сложения")

        result = [[self.data[i][j] + other.data[i][j] for j in range(len(self.data[0]))]
                  for i in range(len(self.data))]
        return self.__class__(result)

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        if self.shape() != other.shape():
            raise ValueError("Матрицы должны быть одинакового размера для вычитания")

        result = [[self.data[i][j] - other.data[i][j] for j in range(len(self.data[0]))]
                  for i in range(len(self.data))]
        return self.__class__(result)

    def __mul__(self, other: 'Matrix') -> 'Matrix':
        if len(self.data[0]) != len(other.data):
            raise ValueError("Число столбцов первой матрицы должно быть равно числу строк второй матрицы")

        result = [[0 for _ in range(len(other.data[0]))] for _ in range(len(self.data))]

        for i in range(len(self.data)):
            for j in range(len(other.data[0])):
                for k in range(len(other.data)):
                    result[i][j] += self.data[i][k] * other.data[k][j]

        return self.__class__(result)

    def __getitem__(self, index: int) -> list[int | float]:
        return self.data[index]

    def __setitem__(self, index: int, value) -> None:
        self.data[index] = value

    def __delitem__(self, index: int) -> None:
        del self.data[index]

    def __len__(self) -> int:
        return len(self.data)

    def append(self, other: ListType) -> 'Matrix':
        for index, value in enumerate(self.data):
            value.append(other[index])
        return self.__class__(self.data)

    def shape(self) -> tuple:
        return len(self.data), len(self.data[0])

    def __repr__(self) -> str:
        return '\n'.join([' \t\t'.join(map(str, row)) for row in self.data])
