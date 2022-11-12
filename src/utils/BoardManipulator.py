class BoardManipulator:
    '''Class to manipulate the board'''

    def __init__(self, board: list, cars_dict: dict):
        self.board = [row[:] for row in board] # Need to copy the board so that the original board is not modified
        self.cars_dict = {key: value[:] for key, value in cars_dict.items()} # More complex, need to copy the dictionary manually
        

    def can_move_car(self, car_letter, direction) -> bool:
        '''Checks if the car can move in the specified direction

        car: letter of the car to move  (E.g. 'A')
        direction: direction to move the car (E.g. 'right'). Moves 1 space at a time

        Returns True if car can move, False otherwise'''
        # get car length
        car_length = self.cars_dict[car_letter][0]
        # get car orientation
        car_orientation = self.cars_dict[car_letter][1]
        # get car position
        car_position = self.cars_dict[car_letter][2]

        # check if car can move in the specified direction
        if direction == 'right':
            # Car needs to be horizontal to move right
            if car_orientation == 'H':
                # Head of the car is on the right side, so check if tail of car is touching the wall or another car REMEMBER BOARD IS board[y][x]!!!
                if car_position[0] + car_length < len(self.board[0]) and self.board[car_position[1]][car_position[0] + car_length] == '.':
                    return True
                else:
                    return False
            else:
                return False
        elif direction == 'left':
            # Car needs to be horizontal to move left
            if car_orientation == 'H':
                # Tail of the car is on the left side, so check if head of car is touching the wall or another car
                if car_position[0] > 0 and self.board[car_position[0]][car_position[0] - 1] == '.':
                    return True
                else:
                    return False
            else:
                return False
        elif direction == 'up':
            # Car needs to be vertical to move up
            if car_orientation == 'V':
                # Tail of the car is on the bottom, so check if head of car is touching the wall or another car
                if car_position[1] > 0 and self.board[car_position[1] - 1][car_position[0]] == '.':
                    return True
                else:
                    return False
            else:
                return False
        elif direction == 'down':
            # Car needs to be vertical to move down
            if car_orientation == 'V':
                # Head of the car is on the top, so check if tail of car is touching the wall or another car
                if car_position[1] + car_length < len(self.board[0]) and self.board[car_position[1] + car_length][car_position[0]] == '.':
                    return True
                else:
                    return False
            else:
                return False
        else:
            print('Invalid direction! Must be "right", "left", "up" or "down"')
            return False

    def move_car(self, car_letter: str, direction: str) -> list:
        '''Moves the car in the specified direction

        car_letter: letter of the car to move  (E.g. 'A')
        direction: direction to move the car (E.g. 'right'). Moves 1 space at a time

        Returns True if move is valid, False if the move is invalid'''

        # get car length
        car_length = self.cars_dict[car_letter][0]
        # get car orientation
        car_orientation = self.cars_dict[car_letter][1]
        # get car position
        car_position = self.cars_dict[car_letter][2]

        # check if car can move in the specified direction
        if self.can_move_car(car_letter, direction):
            # move car
            if direction == 'right':
                # move car right
                self.board[car_position[1]][car_position[0] + car_length] = car_letter
                self.board[car_position[1]][car_position[0]] = '.'
                # update car position
                self.cars_dict[car_letter][2] = (car_position[0] + 1, car_position[1])
                # update fuel
                self.cars_dict[car_letter][3] -= 1
            elif direction == 'left':
                # move car left
                self.board[car_position[1]][car_position[0] - 1] = car_letter
                self.board[car_position[1]][car_position[0] + car_length - 1] = '.'
                # update car position
                self.cars_dict[car_letter][2] = (car_position[0] - 1, car_position[1])
                # update fuel
                self.cars_dict[car_letter][3] -= 1
            elif direction == 'up':
                # move car up
                self.board[car_position[1] - 1][car_position[0]] = car_letter
                self.board[car_position[1] + car_length - 1][car_position[0]] = '.'
                # update car position
                self.cars_dict[car_letter][2] = (car_position[0], car_position[1] - 1)
                # update fuel
                self.cars_dict[car_letter][3] -= 1
            elif direction == 'down':
                # move car down
                self.board[car_position[1] + car_length][car_position[0]] = car_letter
                self.board[car_position[1]][car_position[0]] = '.'
                # update car position
                self.cars_dict[car_letter][2] = (car_position[0], car_position[1] + 1)
                # update fuel
                self.cars_dict[car_letter][3] -= 1

        else:
            print(f"Invalid move! Car {car_letter} cannot move {direction}")
            return None
    
    def print_board(self) -> None:
        '''Prints the board'''
        for row in self.board:
            print(row)
        print()

    def print_cars_dict(self) -> None:
        '''Prints the cars dictionary (car: [length, orientation, [X,Y], fuel]) for the board'''
        print("Format: Car: [Length, Orientation, [X, Y]]")
        for car in self.cars_dict:
            print(car + ": " + str(self.cars_dict[car]))
        print()
