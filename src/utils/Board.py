class Board:
    def __init__(self, board, cars):
        self.board = board
        self.cars = cars

    def __str__(self):
        return f"Board: {self.board}"

class Car:
    def __init__(self, char: str, length: int, orientation: str, position: tuple, fuel: int):
        self.char = char
        self.length = length
        self.orientation = orientation
        self.position = position
        self.fuel = fuel
    
    def __getitem__(self, key):
        if key == 0:
            return self.length
        elif key == 1:
            return self.orientation
        elif key == 2:
            return self.position
        elif key == 3:
            return self.fuel
    
    def __setitem__(self, key, value):
        if key == 0:
            self.length = value
        elif key == 1:
            self.orientation = value
        elif key == 2:
            self.position = value
        elif key == 3:
            self.fuel = value
        

    def __str__(self):
        return f"Car {self.char}: Length={self.length}, Orientation={self.orientation}, Position={self.position}, Fuel={self.fuel}"