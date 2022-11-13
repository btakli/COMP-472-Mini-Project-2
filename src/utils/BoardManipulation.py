from utils.Board import Car
class BoardManipulator:
    '''Class to manipulate the board. NOTE: This class does not modify the original board, it creates a copy of the board and modifies that instead'''

    def __init__(self, board: list, cars_dict: dict, exit: tuple):
        self.board = [row[:] for row in board] # Need to copy the board so that the original board is not modified
        self.cars_dict = {key: Car(value.char, value.length, value.orientation, value.position, value.fuel) for key, value in cars_dict.items()} # More complex, need to copy the dictionary manually
        self.exit = exit # Exit position (X,Y)
        

    def can_move_car(self, car_letter: str, direction: str) -> bool:
        '''Checks if the car can move in the specified direction

        car: letter of the car to move  (E.g. 'A')
        direction: direction to move the car (E.g. 'right'). Moves 1 space at a time

        Returns True if car can move, False otherwise'''
        # get car length
        car_length = self.cars_dict[car_letter].length
        # get car orientation
        car_orientation = self.cars_dict[car_letter].orientation
        # get car position
        car_position = self.cars_dict[car_letter].position

        # If position is None, the car is outside the board and cannot move
        if car_position == None:
            return False
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
                if car_position[0] > 0 and self.board[car_position[1]][car_position[0] - 1] == '.':
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

    def move_car(self, car_letter: str, direction: str) -> None:
        '''Moves the car in the specified direction

        car_letter: letter of the car to move  (E.g. 'A')
        direction: direction to move the car (E.g. 'right'). Moves 1 space at a time

        Returns True if move is valid, False if the move is invalid'''

        # get car length
        car_length = self.cars_dict[car_letter].length
        # get car position
        car_position = self.cars_dict[car_letter].position

        # check if car can move in the specified direction
        if self.can_move_car(car_letter, direction):
            # move car
            if direction == 'right':
                # move car right
                self.board[car_position[1]][car_position[0] + car_length] = car_letter
                self.board[car_position[1]][car_position[0]] = '.'
                # update car position
                self.cars_dict[car_letter].position = (car_position[0] + 1, car_position[1])
                # update fuel
                self.cars_dict[car_letter].fuel -= 1
            elif direction == 'left':
                # move car left
                self.board[car_position[1]][car_position[0] - 1] = car_letter
                self.board[car_position[1]][car_position[0] + car_length - 1] = '.'
                # update car position
                self.cars_dict[car_letter].position = (car_position[0] - 1, car_position[1])
                # update fuel
                self.cars_dict[car_letter].fuel -= 1
            elif direction == 'up':
                # move car up
                self.board[car_position[1] - 1][car_position[0]] = car_letter
                self.board[car_position[1] + car_length - 1][car_position[0]] = '.'
                # update car position
                self.cars_dict[car_letter].position = (car_position[0], car_position[1] - 1)
                # update fuel
                self.cars_dict[car_letter].fuel -= 1
            elif direction == 'down':
                # move car down
                self.board[car_position[1] + car_length][car_position[0]] = car_letter
                self.board[car_position[1]][car_position[0]] = '.'
                # update car position
                self.cars_dict[car_letter].position = (car_position[0], car_position[1] + 1)
                # update fuel
                self.cars_dict[car_letter].fuel -= 1
            
            self.remove_from_valet_if_exists() # Remove car from valet spot if need be

        else:
            print(f"Invalid move! Car {car_letter} cannot move {direction}")
            return None
    
    def remove_from_valet_if_exists(self) -> None:
        '''If a car is in the valet parking spot and in a position to leave, if so remove it from the board
        
        A car can only leave the board if it is horizontal and with its tail in position 3f aka (2, 5)'''
        # check if car is in valet parking spot (3f)
        y_exit = self.exit[1]
        x_exit = self.exit[0]
        if self.board[y_exit][x_exit] != '.':
            car = self.board[y_exit][x_exit]
            car_length = self.cars_dict[car].length
            car_orientation = self.cars_dict[car].orientation
            car_position = self.cars_dict[car].position

            # check if car is horizontal, if so remove it from the board
            if car_orientation == 'H':
                for i in range(car_length):
                    self.board[car_position[1]][car_position[0] + i] = '.'
                # Set position to None since the car is outside the board
                self.cars_dict[car].position = None
                
                print(f"Car {car} has left the board! It's position is now None!")
        else:
            print("No car in valet parking spot to remove!")


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

class SubStateGenerator: 
    '''Generate all possible board states from a given board state'''
    def __init__(self, board: list, cars_dict: dict, exit: tuple):
        self.board = board
        self.cars_dict = cars_dict
        self.exit = exit
        self.substates = [] # list of all possible substates, tuple of (board, cars_dict)
        self.board_manipulator = BoardManipulator(self.board, self.cars_dict, self.exit)
        

    def generate_substates(self) -> list:
        '''Generate substates based on the current board state
        
        Returns a list of substates, each substate is a tuple of (board, cars_dict)'''
        # loop through each car
        for carkey in self.cars_dict:
            # check orientation
            if self.cars_dict[carkey].orientation == 'H':
                # check if car can move left
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'left'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'left')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append((new_board_manipulator.board, new_board_manipulator.cars_dict))
                # check if car can move right
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'right'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'right')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append((new_board_manipulator.board, new_board_manipulator.cars_dict))
            elif self.cars_dict[carkey].orientation == 'V':
                # check if car can move up
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'up'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'up')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append((new_board_manipulator.board, new_board_manipulator.cars_dict))
                # check if car can move down
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'down'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'down')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append((new_board_manipulator.board, new_board_manipulator.cars_dict))
        
        return self.substates
    
    def print_substates(self) -> None:
        '''Prints all substates'''
        for substate in self.substates:
            print("Board:")
            for row in substate[0]:
                print(row)
            for car in substate[1]:
                print(car + ": " + str(substate[1][car]))
        print()


