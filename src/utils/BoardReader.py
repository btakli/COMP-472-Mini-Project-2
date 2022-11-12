# BoardReader reads an input file and converts it into a 6x6 array for the Rush Hour Game
from utils.Board import Car


class BoardReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.boards = []
        self.fueldicts = []  # List of dictionaries of car: fuel
        # List of dictionaries of car: Car obj which contains [length, orientation, head_position, fuel_level]. head_position is a tuple of (x, y) and None if no longer on the board
        self.cars_board = []
        self.x_size = 6
        self.y_size = 6
        self.exit = (5, 2)  # Exit position (X,Y)
        self._read_boards()

    def _read_boards(self):
        '''Reads the passed in file and gets a list of boards'''
        with open(self.file_path, "r") as file:
            for line in file:
                # Skip all comments or empty lines
                if line.startswith("#") or line.isspace():
                    continue
                else:
                    # Logic for creating the board
                    board = []

                    # Separate the board and fuel indicators
                    # 1 split max since we want the list of fuel levels
                    board_and_fuel = line.split(" ", 1)
                    board_string = board_and_fuel[0].strip()
                    # This ensures that we don't get an index out of range error
                    # if there is blank space after the board string even if no fuel string.
                    if len(board_and_fuel) > 1:
                        fuel_string = board_and_fuel[1].strip()
                    else:
                        fuel_string = ""

                    # turn string into x by y array
                    for i in range(self.y_size):
                        start_index = i * self.x_size  # With x = 6, gives values 0, 6, 12, 18, 24, 30
                        # With x = 6, gives values 6, 12, 18, 24, 30, 36
                        end_index = start_index + self.x_size

                        # Gets the string for a row of the board (x long)
                        row_string = board_string[start_index:end_index]

                        row = []
                        for char in row_string:
                            row.append(char)

                        board.append(row)

                    self.boards.append(board)

                    # Get the cars on the board, then generate a dictionary of cars and their length, orientation, head position and fuel level. Put this into the cars_board list
                    carlist = self._get_cars_on_board(board)
                    self.cars_board.append(
                        self._generate_cars_dict(carlist, board, fuel_string))

                    # Add the fuel dictionary to the list of fuel dictionaries
                    self.fueldicts.append(
                        self._get_fuel_dict(fuel_string, carlist))

    def _get_cars_on_board(self, board) -> list:
        '''Returns a list of cars on the board at the given index'''
        cars = []
        for row in board:
            for car in row:
                if car != "." and car not in cars:
                    cars.append(car)
        return cars

    def _generate_cars_dict(self, carlist: list, board: list, fuel_string: str) -> dict:
        '''Generates a dictionary of cars and their length, orientation and head position

        carlist: List of cars on the board

        board: Board we want to examine

        fuel_string: String of fuel levels for each car
        '''
        car_dict = {}
        fuel_dict = self._get_fuel_dict(fuel_string, carlist)
        for car in carlist:
            car_length = 0
            car_orientation = ""
            # [x, y] position of the head of the car (the first occurance of the car in the board)
            car_head_position = []
            for row in board:
                # If we see the car more than once in a row, it is horizontal!
                if row.count(car) > 1:
                    car_length = row.count(car)
                    car_orientation = "H"
                    car_head_position = (row.index(car), board.index(row))
                    break
                # If we see the car once in a row, it is vertical! Because we assume minimum size is 2
                elif row.count(car) == 1 and car_orientation == "":
                    car_orientation = "V"
                for char in row:
                    if char == car:
                        car_length += 1
                        if car_head_position == []:  # We only want to set the head position once, at the first occurance of the car
                            car_head_position = (
                                row.index(char), board.index(row))

            car_dict[car] = Car(car, car_length, car_orientation,
                             car_head_position, fuel_dict[car])

        return car_dict

    def _get_fuel_dict(self, fuel_string: str, carlist: str) -> dict:
        '''Gets the fuel levels from the fuel string for each car, returns a dictionary of car: fuel. If car is not in fuelstring, assume it has 100 fuel

            fuel_string: String of fuel levels for each car
            carlist: List of cars on the board'''
        fuel_levels = {}
        if fuel_string != "":  # If there is a fuel string, get the fuel levels
            fuel_list = fuel_string.split(" ")
            for fuel in fuel_list:
                car = fuel[0]
                fuel_level = fuel[1:]
                if len(fuel_level) == 0:  # If we have just a char with no number, assume 100 fuel
                    fuel_level = 100

                fuel_levels[car] = int(fuel_level)

        # Check if any cars are missing from the fuel string, if so, assume they have 100 fuel
        for car in carlist:
            if car not in fuel_levels.keys():
                fuel_levels[car] = 100

        return fuel_levels

    def print_board(self, board_index) -> None:
        '''Prints the board at the given index'''
        print("Board: " + str(board_index))
        board = self.boards[board_index]
        for row in board:
            print(row)
        print()

    def print_fuel_dict(self, board_index) -> None:
        '''Prints the fuel dictionary for the board at the given index'''
        print("Fuel Dictionary: " + str(board_index))
        fuel_dict = self.fueldicts[board_index]
        for car, fuel in fuel_dict.items():
            print(car + ": " + str(fuel))
        print()

    def print_cars_dict(self, board_index) -> None:
        '''Prints the cars dictionary (car: [length, orientation, [X,Y], fuel_level]) for the board at the given index'''
        print("Cars Dictionary: " + str(board_index))
        print("Format: Car: [Length, Orientation, [X, Y]]")
        cars_dict = self.cars_board[board_index]
        for car in cars_dict:
            print(car + ": " + str(cars_dict[car]))
        print()
