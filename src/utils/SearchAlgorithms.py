# Search Algorithms for the game
import time
from collections import deque
from queue import PriorityQueue

from utils.Board import Car
from utils.BoardManipulation import TreeNode, SubStateGenerator


class PriorityQueue(object):
    def __init__(self):
        self.queue = []
 
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
 
    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0
 
    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)
 
    # for popping an element based on Priority
    def pop(self):
        try:
            min_val = 0
            for i in range(len(self.queue)):
                if self.queue[i][0] < self.queue[min_val][0]:
                    min_val = i
            item = self.queue[min_val]
            del self.queue[min_val]
            return item
        except IndexError:
            print()
            exit()


class SearchAlgorithm: # Base class for all search algorithms
    def __init__(self, board: list, cars_dict: dict, exit: tuple, heuristic=0, lambda_value=2.0):
        self.board = board
        self.cars_dict = cars_dict
        self.root = TreeNode(board, cars_dict, None, exit, heuristic, lambda_value)
        self.exit = exit
        self.goal = None
        self.solution_path = []
        self.solution_path_nodes = []
        self.search_path_length = 0
        self.search_time = 0
        self.heuristic = heuristic
        self.result = False

        if lambda_value < 1:
            raise ValueError("Lambda value must be greater than 1")
        self.lambda_value = lambda_value

    def search(self):
        raise NotImplementedError

    def get_exec_time(self):
        '''Returns the execution time of the search algorithm as a formatted string in seconds'''
        return f"{self.search_time:.4f} seconds"

    def get_solution_path(self):
        '''Returns the solution path of the search algorithm'''
        return self.solution_path

    def get_search_path_length(self):
        '''Returns the length of the search path'''
        return self.search_path_length
    
    def _calculate_solution_path(self):
        '''Calculates the solution path as a list of moves'''
        temp_solution_path = []
        temp_node_path = []
        current_node = self.goal
        while current_node.parent is not None:
            temp_solution_path.insert(0, (current_node.car_moved, current_node.direction_moved,current_node.distance_moved))
            temp_node_path.insert(0, current_node)
            current_node = current_node.parent

        self.solution_path, self.solution_path_nodes = self._combine_moves(temp_solution_path, temp_node_path)


    def _combine_moves(self,temp_solution_path: list, temp_node_path: list):
        '''Combines consecutive moves of the same car in the same direction and increments the distance.
        
        Returns (solution_path, node_path) tuple after the combination'''
        i = 0
        while i < len(temp_solution_path)-1:
            if temp_solution_path[i] == None:
                i += 1
                continue
            if temp_solution_path[i][0] == temp_solution_path[i+1][0] and temp_solution_path[i][1] == temp_solution_path[i+1][1]:
                temp_solution_path[i] = (temp_solution_path[i][0], temp_solution_path[i][1], temp_solution_path[i][2]+temp_solution_path[i+1][2])
                temp_solution_path[i+1] = None

                temp_node_path[i+1].distance_moved += temp_node_path[i].distance_moved # increment distance of the next node since it is at the state we want
                temp_node_path[i] = None

                i += 1
            else:
                i += 1
        # remove None values
        solution_path = [move for move in temp_solution_path if move is not None]
        node_path = [node for node in temp_node_path if node is not None]
        return solution_path, node_path

class UniformCostSearch(SearchAlgorithm): 
    ''' Uniform Cost Search Algorithm '''
    def __init__(self, board: list, cars_dict: dict, exit: tuple):
        super().__init__(board, cars_dict, exit)


    def search(self):
        '''Searches for the solution to the game'''
        open_list = PriorityQueue()
        closed_list = []
        visited_boards=[]

        # Start timer 
        start_time = time.perf_counter_ns()
        # PQ is a tuple of (cost, state)
        open_list.insert((self.root.cost, self.root))

        while not(open_list.isEmpty()):           
            current_node = open_list.pop()[1]
            
            if current_node.board in visited_boards:
                continue
            
            self.search_path_length += 1        
            closed_list.append(current_node)
            visited_boards.append(current_node.board)
            if current_node.check_win(self.exit):
                self.goal = current_node
                self._calculate_solution_path()
                end_time = time.perf_counter_ns()
                self.search_time = (end_time - start_time) * 10**-9 # convert to seconds
                self.result = True
                return current_node

            substate_generator = SubStateGenerator(current_node.board, current_node.cars_dict, self.exit)
            substate_generator.generate_substates()

            for substate in substate_generator.substates: 
                if not(substate[0] in visited_boards):
                    child = TreeNode(substate[0], substate[1], current_node, self.exit)
                    current_node.children.append(child)
                    open_list.insert((child.cost, child))

        return None

                    

     
class GBFS(SearchAlgorithm):
    ''' Greedy Best First Search Algorithm '''
    def __init__(self, board: list, cars_dict: dict, exit: tuple, heuristic: int, lambda_value = 2.0):
        '''Initializes the Greedy Best First Search Algorithm
        
        board: list of lists representing the board
        cars_dict: dictionary of cars
        exit: tuple representing the exit
        heuristic: int representing the heuristic to use (0 = no heuristic, 1 = h1, 2 = h2...)
        lambda_value: float for the lambda value for h3'''
        super().__init__(board, cars_dict, exit, heuristic, lambda_value)

    def search(self):
        '''Searches for the solution to the game'''
        open_list = PriorityQueue()
        closed_list = []
        visited_boards=[]

        # Start timer
        start_time = time.perf_counter_ns()

        # PQ is a tuple of (f(n), state)
        open_list.insert((self.root.h_n, self.root))

        while not(open_list.isEmpty()):
            self.search_path_length += 1
            current_node = open_list.pop()[1]

            if current_node.board in visited_boards:
                continue
            visited_boards.append(current_node.board)
            closed_list.append(current_node)

            if current_node.check_win(self.exit):
                self.goal = current_node
                self._calculate_solution_path()
                end_time = time.perf_counter_ns()
                self.search_time = (end_time - start_time) * 10**-9
                self.result = True
                return current_node

            substate_generator = SubStateGenerator(current_node.board, current_node.cars_dict, self.exit)
            substate_generator.generate_substates()

            for substate in substate_generator.substates: 
                if not(substate[0] in visited_boards):                   
                    child = TreeNode(substate[0], substate[1], current_node, self.exit, self.heuristic, self.lambda_value, False)
                    current_node.children.append(child)
                    open_list.insert((child.h_n, child))
        return None
            



        

class A(SearchAlgorithm):
    ''' A/A* Search Algorithm '''

    def __init__(self, board: list, cars_dict: dict, exit: tuple, heuristic: int, lambda_value=2.0):
        '''Initializes the A/A* Search Algorithm

        board: list of lists representing the board
        cars_dict: dictionary of cars
        exit: tuple representing the exit
        heuristic: int representing the heuristic to use (0 = no heuristic, 1 = h1, 2 = h2...)
        lambda_value: float for the lambda value for h3'''
        super().__init__(board, cars_dict, exit, heuristic, lambda_value)

    def search(self):
        '''Searches for the solution to the game'''
        open_list = PriorityQueue()
        closed_list = []

        # Start timer
        start_time = time.perf_counter_ns()

        # PQ is a tuple of (h(n), state)
        open_list.put((self.root.f_n, self.root))

        while open_list.qsize() > 0:
            self.search_path_length += 1
            current_node = open_list.get()
            closed_list.append(current_node)

            if current_node.check_win(self.exit):
                self.goal = current_node
                self._calculate_solution_path()
                end_time = time.perf_counter_ns()
                self.search_time = (end_time - start_time) * 10 ** -9
                self.result = True
                return current_node

            substate_generator = SubStateGenerator(current_node.board, current_node.cars_dict, self.exit)
            substate_generator.generate_substates()

            for substate in substate_generator.substates:
                in_closed_list = False
                for node in closed_list:
                    if substate[0] == node.board:
                        in_closed_list = True
                        break
                if not in_closed_list:
                    child = TreeNode(substate[0], substate[1], current_node, self.exit, self.heuristic,
                                     self.lambda_value, False)
                    current_node.children.append(child)
                    open_list.put((child.f_n, child))


                    