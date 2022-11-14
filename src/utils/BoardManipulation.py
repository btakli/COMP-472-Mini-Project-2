from utils.Board import Car
class BoardManipulator:
    '''Class to manipulate the board. NOTE: This class does not modify the original board, it creates a copy of the board and modifies that instead'''

    def __init__(self, board_dimensions: tuple, cars_dict: dict, exit: tuple):
        self.board_dimensions = board_dimensions # (x, y)
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
        # get car tail position
        car_tail_position = self.cars_dict[car_letter].tail_position

        # If position is None, the car is outside the board and cannot move
        if car_position == None:
            return False
        # If A is at the exit, it cannot move
        if car_letter == 'A' and self.cars_dict['A'].tail_position == self.exit:
            return False

        # If fuel level is 0, the car cannot move
        if self.cars_dict[car_letter].fuel == 0:
            return False
        
        # check if car can move in the specified direction
        if direction == 'right':
            # Car needs to be horizontal to move right
            if car_orientation == 'H':
                # Head of the car is on the right side, so check if tail of car is touching the wall or another car REMEMBER BOARD IS board[y][x]!!!
                if car_tail_position[0] < self.board_dimensions[0] - 1 and self._check_if_car_in_way(car_letter, direction) == False:
                    return True
                else:
                    return False
            else:
                return False
        elif direction == 'left':
            # Car needs to be horizontal to move left
            if car_orientation == 'H':
                # Tail of the car is on the left side, so check if head of car is touching the wall or another car
                if car_position[0] > 0 and self._check_if_car_in_way(car_letter, direction) == False:
                    return True
                else:
                    return False
            else:
                return False
        elif direction == 'up':
            # Car needs to be vertical to move up
            if car_orientation == 'V':
                # Tail of the car is on the bottom, so check if head of car is touching the wall or another car
                if car_position[1] > 0 and self._check_if_car_in_way(car_letter, direction) == False:
                    return True
                else:
                    return False
            else:
                return False
        elif direction == 'down':
            # Car needs to be vertical to move down
            if car_orientation == 'V':
                # Head of the car is on the top, so check if tail of car is touching the wall or another car
                if car_tail_position[1] < self.board_dimensions[1] - 1 and self._check_if_car_in_way(car_letter, direction) == False:
                    return True
                else:
                    return False
            else:
                return False
        else:
            print('Invalid direction! Must be "right", "left", "up" or "down"')
            return False

    def _check_if_car_in_way(self, car_letter: str, direction: str) -> bool:
        '''Checks if there's a car in the way based on the dictionary Returns True if there is a car in the way, False otherwise'''
        # car position
        car_position = self.cars_dict[car_letter].position
        # car orientation
        car_orientation = self.cars_dict[car_letter].orientation
        # car tail position
        car_tail_position = self.cars_dict[car_letter].tail_position
        for car in self.cars_dict:
            if car != car_letter:
                # car position
                other_car_position = self.cars_dict[car].position
                # car length
                other_car_length = self.cars_dict[car].length
                # car orientation
                other_car_orientation = self.cars_dict[car].orientation
                # car tail position
                other_car_tail_position = self.cars_dict[car].tail_position
                # Check if the car is in the way based on the orientation and direction we want to move
                if car_orientation == 'H' and other_car_orientation == 'H':
                    if car_position[1] == other_car_position[1]:
                        if direction == 'right':
                            if car_tail_position[0] == other_car_position[0] - 1:
                                return True
                        elif direction == 'left':
                            if car_position[0] == other_car_tail_position[0] + 1:
                                return True
                elif car_orientation == 'V' and other_car_orientation == 'V':
                    if car_position[0] == other_car_position[0]:
                        if direction == 'up':
                            if car_position[1] == other_car_tail_position[1] + 1:
                                return True
                        elif direction == 'down':
                            if car_tail_position[1] == other_car_position[1] - 1:
                                return True
                elif car_orientation == 'H' and other_car_orientation == 'V':
                    # We need to see if the car will collide with the other car. Check if the spot we are going to move to is between the head and tail of the other car!
                    if direction == 'right':
                        if car_tail_position[0] == other_car_position[0] - 1 and car_tail_position[1] >= other_car_position[1] and car_tail_position[1] <= other_car_tail_position[1]:
                            return True
                    elif direction == 'left':
                        if car_position[0] == other_car_tail_position[0] + 1 and car_position[1] >= other_car_position[1] and car_position[1] <= other_car_tail_position[1]:
                            return True
                elif car_orientation == 'V' and other_car_orientation == 'H':
                    if direction == 'up':
                        if car_position[1] == other_car_tail_position[1] + 1 and car_position[0] >= other_car_position[0] and car_position[0] <= other_car_tail_position[0]:
                            return True
                    elif direction == 'down':
                        if car_tail_position[1] == other_car_position[1] - 1 and car_tail_position[0] >= other_car_position[0] and car_tail_position[0] <= other_car_tail_position[0]:
                            return True
                        
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
                # update car position
                self.cars_dict[car_letter].set_position((car_position[0] + 1, car_position[1]))
                # update fuel
                self.cars_dict[car_letter].fuel -= 1
            elif direction == 'left':
                # move car left
                # update car position
                self.cars_dict[car_letter].set_position((car_position[0] - 1, car_position[1]))
                # update fuel
                self.cars_dict[car_letter].fuel -= 1
            elif direction == 'up':
                # move car up
                # update car position
                self.cars_dict[car_letter].set_position((car_position[0], car_position[1] - 1))
                # update fuel
                self.cars_dict[car_letter].fuel -= 1
            elif direction == 'down':
                # move car down
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
        
        for car in self.cars_dict:
            if car != 'A' or remove_A:
                car_tail_position = self.cars_dict[car].tail_position
                car_orientation = self.cars_dict[car].orientation
                if car_orientation == 'H' and car_tail_position == self.exit:
                    if print_debug:
                        print(f"Car {car} has left the board! It's position is now None!")
                    # remove car from board  (set position to None)
                    self.cars_dict[car].set_position(None)
                    break

    def print_cars_dict(self) -> None:
        '''Prints the cars dictionary (car: [length, orientation, [X,Y], fuel]) for the board'''
        print("Format: Car: [Length, Orientation, [X, Y]]")
        for car in self.cars_dict:
            print(car + ": " + str(self.cars_dict[car]))
        print()
    
    def print_board(self) -> None:
        '''Prints the board based on the cars dictionary'''
        # Initialize board
        board = [['.' for i in range(self.board_dimensions[0])] for j in range(self.board_dimensions[1])]
        
        # Add cars to board
        for car in self.cars_dict:
            car_position = self.cars_dict[car].position
            car_orientation = self.cars_dict[car].orientation
            car_length = self.cars_dict[car].length
            if car_orientation == 'H':
                for i in range(car_length):
                    board[car_position[1]][car_position[0] + i] = car
            elif car_orientation == 'V':
                for i in range(car_length):
                    board[car_position[1] + i][car_position[0]] = car
        
        for row in board:
            print(row)
        print()

class SubStateGenerator: 
    '''Generate all possible board states from a given board state'''
    def __init__(self, board_dimensions: tuple, cars_dict: dict, exit: tuple):
        '''Constructor without use of StateTree.TreeNode class, sets '''
        self.board_dimensions = board_dimensions
        self.cars_dict = cars_dict
        self.exit = exit
        self.substates = [] # list of all possible substates, aka cars_dicts 
        self.board_manipulator = BoardManipulator(board_dimensions, self.cars_dict, self.exit)


    def generate_substates(self) -> list:
        '''Generate substates based on the current board state
        
        Returns a list of substates, each substate is a tuple of (board, cars_dict). If ambulance is gone, returns []'''
        # check if ambulance is gone
        if self.cars_dict['A'].position == None:
            return []
        # loop through each car
        for carkey in self.cars_dict:
            # check orientation
            if self.cars_dict[carkey].orientation == 'H':
                # check if car can move left
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'left'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board_dimensions, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'left')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append(new_board_manipulator.cars_dict)
                # check if car can move right
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'right'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board_dimensions, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'right')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append(new_board_manipulator.cars_dict)
            elif self.cars_dict[carkey].orientation == 'V':
                # check if car can move up
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'up'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board_dimensions, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'up')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append(new_board_manipulator.cars_dict)
                # check if car can move down
                if self.board_manipulator.can_move_car(self.cars_dict[carkey].char, 'down'):
                    # move the car
                    new_board_manipulator = BoardManipulator(self.board_dimensions, self.cars_dict, self.exit)
                    new_board_manipulator.move_car(self.cars_dict[carkey].char, 'down')
                    # add the new (board, cars_dict) tuple to the list of substates
                    self.substates.append(new_board_manipulator.cars_dict)

        return self.substates
    
    def print_substates(self) -> None:
        '''Prints all substates'''
        for substate in self.substates:
            for car in substate:
                print(car + ": " + str(substate[car]))
            print()

class StateTree:
    '''A tree of all possible states for a board'''

    class TreeNode:
        '''A node in the state tree'''
        def __init__(self, board_dimensions: tuple, cars_dict: dict, parent: 'StateTree.TreeNode'):
            '''Constructor for a TreeNode, sets the board dimensions, cars_dict, and parent. cars_dict is a copy of the parent's cars_dict, so it won't interfere with the parent's cars_dict'''
            self.board_dimensions = board_dimensions
            self.cars_dict = {key: Car(value.char, value.length, value.orientation, value.position, value.fuel) for key, value in cars_dict.items()}
            self.parent = parent
            self.children = []

            self.car_moved = None
            self._compute_car_moved()

            self.direction_moved = None
            self.distance_moved = None
            self._compute_direction_moved()

            self.cost = 0
            self._compute_cost()
            
        
        def _compute_cost(self) -> None:
            '''Computes the cost of the node'''
            if self.parent is None:
                self.cost = 0
            else:
                if self.car_moved == self.parent.car_moved: # If piece moved is the same as the parent, cost is same as parent
                    self.cost = self.parent.cost
                else:
                    self.cost = self.parent.cost + 1
        
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
            if isinstance(other, self.__class__):
                for car in self.cars_dict:
                    if self.cars_dict[car].position != other.cars_dict[car].position:
                        return False
            return True

        def __lt__(self, other):
            if isinstance(other, self.__class__):
                return self.cost <= other.cost
        
        def check_win(self, exit: tuple) -> bool:
            '''Checks if the board is in a winning state'''
            # check if ambulance is gone (it left the board through the exit) or is at the exit (since we do not want to remove it from the board for our output)
            if self.cars_dict['A'].position == None or self.cars_dict['A'].tail_position == exit:
                return True
            else:
                return False

        def __str__(self) -> str:
            '''returns the node in one line, using the format of the example files'''
            output_list = ["." for i in range(self.board_dimensions[0]*self.board_dimensions[1])] # create a string of all dots of the correct length to start
            # using the dictionary, print out what the board would look like. Uses math to determine right spot to put the car
            for car in self.cars_dict:
                if self.cars_dict[car].position != None:
                    if self.cars_dict[car].orientation == 'H':
                        for i in range(self.cars_dict[car].length):
                            output_list[self.cars_dict[car].position[0] + self.cars_dict[car].position[1] * self.board_dimensions[0] + i] = self.cars_dict[car].char
                    else:
                        for i in range(self.cars_dict[car].length):
                            output_list[self.cars_dict[car].position[0] + self.cars_dict[car].position[1] * self.board_dimensions[0] + i * self.board_dimensions[0]] = self.cars_dict[car].char
            
            output_string = "".join(output_list)
            for car in self.cars_dict:
                fuel = self.cars_dict[car].fuel
                if fuel < 100:
                    output_string += " " + car + "" + str(fuel)
            return output_string


    def __init__(self, board: list, cars_dict: dict, exit: tuple):
        self.board = board
        self.cars_dict = cars_dict
        self.exit = exit
        self.root = StateTree.TreeNode(self.board, self.cars_dict, None)

    def add_node(self, board: list, cars_dict: dict, parent: 'StateTree.TreeNode') -> None:
        '''Add a node to the tree'''
        self.root.children.append(StateTree.TreeNode(board, cars_dict, parent))
