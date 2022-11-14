# Search Algorithms for the game
import time
from queue import PriorityQueue

from utils.Board import Car
from utils.BoardManipulation import StateTree, SubStateGenerator


class UniformCostSearch:
    ''' Uniform Cost Search Algorithm '''
    def __init__(self, board: list, cars_dict: dict, exit: tuple):
        self.board = board
        self.cars_dict = cars_dict
        self.exit = exit
        self.StateTree = StateTree(board, cars_dict, exit)
        self.goal = None
        self.search_time = 0
        self.search_path_length = 0
        self.solution_path = [] # Each element is a tuple of (car, movement, distance)

    def search(self):
        '''Searches for the solution to the game'''
        open_list = PriorityQueue()
        closed_list = []

        # Start timer 
        start_time = time.perf_counter_ns()
        # PQ is a tuple of (cost, state)
        open_list.put((self.StateTree.root.cost, self.StateTree.root))

        while open_list.qsize() > 0:
            self.search_path_length += 1
            current_tuple = open_list.get()
            current_node = current_tuple[1]
            closed_list.append(current_node)

            if current_node.check_win(self.exit):
                self.goal = current_node
                self._calculate_solution_path()
                end_time = time.perf_counter_ns()
                self.search_time = (end_time - start_time) * 10**-9 # convert to seconds
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
                    child = StateTree.TreeNode(substate[0], substate[1], current_node)
                    current_node.children.append(child)
                    open_list.put((child.cost, child))

    def get_exec_time(self):
        '''Returns the execution time of the search algorithm as a formatted string in seconds'''
        return f"{self.search_time:.4f} seconds"

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

            
        

        


class GBFS:
    ''' Greedy Best First Search Algorithm '''
    def __init__(self, board: list, cars_dict: dict, exit: tuple):
        self.board = board
        self.cars_dict = cars_dict
        self.exit = exit

    def search(self):
        '''Searches for the solution to the game'''
        pass

class A:
    ''' A/A* Search Algorithm '''
    def __init__(self, board: list, cars_dict: dict, exit: tuple):
        self.board = board
        self.cars_dict = cars_dict
        self.exit = exit

    def search(self):
        '''Searches for the solution to the game'''
        pass


                    