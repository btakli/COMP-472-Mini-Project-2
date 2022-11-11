class Board:
    def __init__(self, board, cars):
        self.board = board
        self.cars = cars

    def __str__(self):
        return f"Board: {self.board}"

class Car:
    def __init__(self, char: str, length: int, orientation: str, position: list, fuel: int):
        self.char = char
        self.length = length
        self.orientation = orientation
        self.position = position
        self.fuel = fuel

    def __str__(self):
        return f"Car: {self.length}, {self.orientation}, {self.position}, {self.fuel}"