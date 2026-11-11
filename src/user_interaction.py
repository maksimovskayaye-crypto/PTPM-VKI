from abc import ABC, abstractmethod


class IUserInteraction(ABC):

    @abstractmethod
    def get_triangle_sides(self) -> tuple:
        pass


class ConsoleUserInteraction(IUserInteraction):

    def get_triangle_sides(self) -> tuple:
        a = input("Введите сторону A: ")
        b = input("Введите сторону B: ")
        c = input("Введите сторону C: ")
        return a, b, c