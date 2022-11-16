# Search Algorithms for the game
import time
from collections import deque
from queue import PriorityQueue

from utils.Board import Car
from utils.BoardManipulation import TreeNode, SubStateGenerator

class NodePriorityQueue: 
    def __init__(self):
        self.dict = {}
        self.size = 0
    
    def put(self, node_tuple):
        key = node_tuple[0]
        node = node_tuple[1]
        if key in self.dict:
            self.dict[key].appendleft(node)
        else:
            self.dict[key] = deque([node])
        self.size += 1
    
    def get(self):
        if len(self.dict) == 0:
            return None
        min_key = min(self.dict)
        min_node_list = self.dict[min_key]
        min_node = min_node_list.popleft()
        if len(min_node_list) == 0:
            del self.dict[min_key]
        self.size -= 1
        return min_node

    
    def __len__(self):
        return self.size
    
    def qsize(self):
        return self.size

class SearchAlgorithm: # Base class for all search algorithms
    def __init__(self, board: list, cars_dict: dict, exit: tuple, heuristic=0, lambda_value=2.0):
        self.board = board
        self.cars_dict = cars_dict
        self.root = TreeNode(board, cars_dict, None, exit, heuristic, lambda_value)
        self.exit = exit
        self.goal = None
        self.solution_path = []
        self.search_path_length = 0
        self.search_time = 0
        self.heuristic = heuristic

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
        current_node = self.goal
        while current_node.parent is not None:
            temp_solution_path.insert(0, (current_node.car_moved, current_node.direction_moved,1))
            current_node = current_node.parent
            
        #TODO combine consecutive moves of the same car in the same direction and increment distance

        for i in range(len(temp_solution_path)):
            self.solution_path.append((temp_solution_path[i][0], temp_solution_path[i][1], temp_solution_path[i][2]))



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
        open_list.put((self.root.cost, self.root))

        while open_list.qsize() > 0:           
            current_node = open_list.get()[1]
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
                return current_node

            substate_generator = SubStateGenerator(current_node.board, current_node.cars_dict, self.exit)
            substate_generator.generate_substates()

            for substate in substate_generator.substates: 
                if not(substate[0] in visited_boards):
                    child = TreeNode(substate[0], substate[1], current_node, self.exit)
                    current_node.children.append(child)
                    open_list.put((child.cost, child))

                    

     
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
        open_list = NodePriorityQueue()
        closed_list = []

        # Start timer
        start_time = time.perf_counter_ns()

        # PQ is a tuple of (f(n), state)
        open_list.put((self.root.h_n, self.root))

        while open_list.qsize() > 0:
            self.search_path_length += 1
            current_node = open_list.get()
            closed_list.append(current_node)

            if current_node.check_win(self.exit):
                self.goal = current_node
                self._calculate_solution_path()
                end_time = time.perf_counter_ns()
                self.search_time = (end_time - start_time) * 10**-9
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
                    child = TreeNode(substate[0], substate[1], current_node, self.exit, self.heuristic, self.lambda_value, False)
                    current_node.children.append(child)
                    open_list.put((child.h_n, child))

        

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
        open_list = NodePriorityQueue()
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


                    