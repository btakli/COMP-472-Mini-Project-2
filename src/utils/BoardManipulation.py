from utils.Board import Car
from collections import OrderedDict
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
        # If A is at the exit, it cannot move
        if car_letter == 'A' and self.board[self.exit[1]][self.exit[0]] == 'A':
            return False

        # If fuel level is 0, the car cannot move
        if self.cars_dict[car_letter].fuel == 0:
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
                self.cars_dict[car_letter].set_position((car_position[0] + 1, car_position[1]))
                # update fuel
                self.cars_dict[car_letter].fuel -= 1
            elif direction == 'left':
                # move car left
                self.board[car_position[1]][car_position[0] - 1] = car_letter
                self.board[car_position[1]][car_position[0] + car_length - 1] = '.'
                # update car position
                self.cars_dict[car_letter].set_position((car_position[0] - 1, car_position[1]))
                # update fuel
                self.cars_dict[car_letter].fuel -= 1
            elif direction == 'up':
                # move car up
                self.board[car_position[1] - 1][car_position[0]] = car_letter
                self.board[car_position[1] + car_length - 1][car_position[0]] = '.'
                # update car position
                self.cars_dict[car_letter].set_position((car_position[0], car_position[1] - 1))
                # update fuel
                self.cars_dict[car_letter].fuel -= 1
            elif direction == 'down':
                # move car down
                self.board[car_position[1] + car_length][car_position[0]] = car_letter
                self.board[car_position[1]][car_position[0]] = '.'
                # update car position
                self.cars_dict[car_letter].set_position((car_position[0], car_position[1] + 1))
                # update fuel
                self.cars_dict[car_letter].fuel -= 1

                self.remove_from_valet_if_exists() # Remove car from valet spot if need be

        else:
            print(f"Invalid move! Car {car_letter} cannot move {direction}")
            return None
    
    def remove_from_valet_if_exists(self, remove_A = False, print_debug = False) -> None:
        '''If a car is in the valet parking spot and in a position to leave, if so remove it from the board
        
        A car can only leave the board if it is horizontal and with its tail in position 3f aka (2, 5)
        By default do NOT remove A, since output wants us to keep it.
        By default do NOT print debug messages since it bloats output.'''
        # check if car is in valet parking spot (3f)
        y_exit = self.exit[1]
        x_exit = self.exit[0]
        if self.board[y_exit][x_exit] != '.':
            if not remove_A: # If we aren't removing A
                if self.board[y_exit][x_exit] == 'A':
                    return None

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
                self.cars_dict[car].tail_position = None
                if print_debug:
                    print(f"Car {car} has left the board! It's position is now None!")
        else:
            if print_debug:
                print("No car in valet parking spot to remove!")
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

class SubStateGenerator: 
    '''Generate all possible board states from a given board state'''
    def __init__(self, board: list, cars_dict: dict, exit: tuple):
        '''Constructor without use of StateTree.TreeNode class, sets '''
        self.board = board
        self.cars_dict = cars_dict
        self.exit = exit
        self.substates = [] # list of all possible substates, tuple of (board, cars_dict)
        self.board_manipulator = BoardManipulator(self.board, self.cars_dict, self.exit)


    def generate_substates(self) -> list:
        '''Generate substates based on the current board state
        
        Returns a list of substates, each substate is a tuple of (board, cars_dict). If ambulance is gone, returns []'''
        # check if ambulance is gone
        if self.cars_dict['A'].position == None:
            return []
        # loop through each car
        sorted_cars = OrderedDict(sorted(self.cars_dict.items()))
        for carkey in sorted_cars:
            # check orientation
            if self.cars_dict[carkey].orientation == 'H':
                # check if car can move left
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'left'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'left')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append((new_board_manipulator.board, new_board_manipulator.cars_dict))

                    # Check if car can keep moving left
                    while new_board_manipulator.can_move_car(new_board_manipulator.cars_dict[carkey].char, 'left'):
                        new_board_manipulator = BoardManipulator(new_board_manipulator.board, new_board_manipulator.cars_dict, self.exit)
                        new_board_manipulator.move_car(new_board_manipulator.cars_dict[carkey].char, 'left')
                        self.substates.append((new_board_manipulator.board, new_board_manipulator.cars_dict))

                # check if car can move right
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'right'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'right')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append((new_board_manipulator.board, new_board_manipulator.cars_dict))

                    # Check if car can keep moving right
                    while new_board_manipulator.can_move_car(new_board_manipulator.cars_dict[carkey].char, 'right'):
                        new_board_manipulator = BoardManipulator(new_board_manipulator.board, new_board_manipulator.cars_dict, self.exit)
                        new_board_manipulator.move_car(new_board_manipulator.cars_dict[carkey].char, 'right')
                        self.substates.append((new_board_manipulator.board, new_board_manipulator.cars_dict)) 

            elif self.cars_dict[carkey].orientation == 'V':
                # check if car can move up
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'up'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'up')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append((new_board_manipulator.board, new_board_manipulator.cars_dict))

                    # Check if car can keep moving up
                    while new_board_manipulator.can_move_car(new_board_manipulator.cars_dict[carkey].char, 'up'):
                        new_board_manipulator = BoardManipulator(new_board_manipulator.board, new_board_manipulator.cars_dict, self.exit)
                        new_board_manipulator.move_car(new_board_manipulator.cars_dict[carkey].char, 'up')
                        self.substates.append((new_board_manipulator.board, new_board_manipulator.cars_dict))
                # check if car can move down
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'down'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'down')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append((new_board_manipulator.board, new_board_manipulator.cars_dict))

                    # Check if car can keep moving down
                    while new_board_manipulator.can_move_car(new_board_manipulator.cars_dict[carkey].char, 'down'):
                        new_board_manipulator = BoardManipulator(new_board_manipulator.board, new_board_manipulator.cars_dict, self.exit)
                        new_board_manipulator.move_car(new_board_manipulator.cars_dict[carkey].char, 'down')
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

class TreeNode:
    '''A node in the state tree'''
    def __init__(self, board: list, cars_dict: dict, parent: 'TreeNode', exit: tuple, heuristic = 0, lambda_val = 2, compute_g_n = True):
        '''Constructor for TreeNode class
        
        board: the board of the node
        cars_dict: the cars dictionary of the node
        parent: the parent of the node
        exit: the exit of the board
        heuristic: the heuristic type to use for the node. 0 for no heuristic, 1 for h1, 2 for h2
        lambda_val: the lambda value to use for h3
        compute_cost: whether or not to compute the cost of the node'''

        self.board = [row[:] for row in board]
        self.cars_dict = {key: Car(value.char, value.length, value.orientation, value.position, value.fuel) for key, value in cars_dict.items()}
        self.parent = parent
        self.children = []
        self.exit = exit

        self.car_moved = None
        self._compute_car_moved()

        self.direction_moved = None
        self.distance_moved = None
        self._compute_direction_moved()

        self.lambda_val = lambda_val # lambda value for h3

        self.h_n = 0
        self.cost = 0
        self.f_n = 0
        self.g_n = 0
        self._compute_cost()
        if compute_g_n:
            self.g_n = self.cost
        else: 
            self.g_n = 0
            
        self._compute_h_n(heuristic)
    
    def set_heuristic(self, h_n: int):
        self.h_n = h_n
        self.f_n = self.g_n + self.h_n
    
    def _compute_cost(self) -> None:
        '''Computes the cost of the node'''
        if self.parent is None:
            self.cost = 0
        else:
            if self.car_moved == self.parent.car_moved: # If piece moved is the same as the parent, cost is same as parent
                self.cost = self.parent.cost
            else:
                self.cost = self.parent.cost + 1
        self.f_n = self.g_n + self.h_n
    
    def _compute_h_n(self, heuristic: int) -> None:
        '''Computes the heuristic of the node'''
        if heuristic == 0:
            self.h_n = 0
        elif heuristic == 1:
            self.h_n = self._h1()
        elif heuristic == 2:
            self.h_n = self._h2()
        elif heuristic == 3:
            self.h_n = self._h3(self.lambda_val)
        self.f_n = self.g_n + self.h_n


    def _h1(self) -> int:
        '''h1: The # of blocking vehicles'''
        # count the number of cars blocking the exit
        count = 0
        blocking_vehicles = []
        for i in range(self.cars_dict['A'].tail_position[0] + 1, self.exit[0]+1):
            if self.board[self.exit[1]][i] != '.':
                if self.board[self.exit[1]][i] not in blocking_vehicles:
                    blocking_vehicles.append(self.board[self.exit[1]][i])
                    count += 1
        return count
    
    def _h2(self) -> int:
        '''h2: #  blocked positions'''
        # count the number of cars blocking the exit
        count = 0
        for i in range(self.cars_dict['A'].tail_position[0] + 1, self.exit[0]+1):
            if self.board[self.exit[1]][i] != '.':
                count += 1
        return count

    def _h3(self, lambda_const) -> int:
        '''h3: h1 times constant'''
        return self._h1() * lambda_const
    
    def _compute_car_moved(self) -> None:
        '''Computes the piece that was moved to get to this node'''
        if self.parent is None:
            self.car_moved = None
        else:
            # loop through each car in the parent's cars_dict
            for car in self.parent.cars_dict:
                # check if the car's position is different
                if self.parent.cars_dict[car].position != self.cars_dict[car].position:
                    self.car_moved = car
                    break
    
    def _compute_direction_moved(self) -> None:
        '''Computes the direction AND DISTANCE that the piece was moved to get to this node'''
        if self.parent is None:
            self.direction_moved = None
        else:
            # if piece position is now None, it was removed and moved right off the board
            if self.cars_dict[self.car_moved].position == None:
                self.direction_moved = 'right'
            # check if the piece moved is horizontal or vertical
            elif self.parent.cars_dict[self.car_moved].orientation == 'H':
                # check if the piece moved left or right
                if self.cars_dict[self.car_moved].position[0] < self.parent.cars_dict[self.car_moved].position[0]:
                    self.direction_moved = 'left'
                    self.distance_moved = self.parent.cars_dict[self.car_moved].position[0] - self.cars_dict[self.car_moved].position[0]
                else:
                    self.direction_moved = 'right' # else since by virtue of being piece_moved it must have moved
                    self.distance_moved = self.cars_dict[self.car_moved].position[0] - self.parent.cars_dict[self.car_moved].position[0]
            else:
                # check if the piece moved up or down
                if self.cars_dict[self.car_moved].position[1] < self.parent.cars_dict[self.car_moved].position[1]:
                    self.direction_moved = 'up'
                    self.distance_moved = self.parent.cars_dict[self.car_moved].position[1] - self.cars_dict[self.car_moved].position[1]
                else:
                    self.direction_moved = 'down'
                    self.distance_moved = self.cars_dict[self.car_moved].position[1] - self.parent.cars_dict[self.car_moved].position[1]
        

    #equals method defined as two boards being the same if they have the same cars in the same positions
    def __eq__(self, other):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != other.board[row][col]:
                    return False
        return True

    def __lt__(self, other):
        return self.f_n <= other.f_n # TODO for priority queue, this is not ideal! 
    
    def check_win(self, exit: tuple) -> bool:
        '''Checks if the board is in a winning state'''
        # check if ambulance is gone (it left the board through the exit) or is at the exit (since we do not want to remove it from the board for our output)
        if self.cars_dict['A'].position == None or (self.board[exit[1]][exit[0]] == 'A'):
            return True
        else:
            return False

    def __str__(self) -> str:
        '''returns the node in one line, using the format of the example files'''
        output = ""
        output += str(self.f_n) + " " + str(self.g_n) + " " + str(self.h_n) + " " 
        for row in self.board:
            for char in row:
                output += char
        
        for car in self.cars_dict:
            fuel = self.cars_dict[car].fuel
            if fuel < 100:
                output += " " + car + "" + str(fuel)
        return output
