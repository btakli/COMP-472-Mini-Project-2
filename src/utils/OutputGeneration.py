# Output Generation for the Game's results
import os
from pathlib import Path

from utils.SearchAlgorithms import UniformCostSearch, GBFS, A, SearchAlgorithm
from utils.BoardReader import BoardReader

class OutputGeneration:

    def __init__(self, search: SearchAlgorithm, board_reader: BoardReader, board_index: int, overwrite_results=False):
        '''Initializes the OutputGeneration Class
        search: search algorithm used and to be outputted
        board_reader: board_reader used
        board_index: Board Number
        overwrite_results: If True, will overwrite existing results files'''
        self.search = search
        self.board_reader = board_reader
        self.board_index = board_index
        self.overwrite_results = overwrite_results
        if issubclass(search.__class__, UniformCostSearch):
            self.search_file_title = "ucs-search-"+str(board_index+1)+".txt"
            self.solution_file_title = "ucs-sol-"+str(board_index+1)+".txt"
        elif issubclass(search.__class__, GBFS):
            self.search_file_title = "gbfs-h"+str(search.heuristic)+"-search-"+str(board_index+1)+".txt"
            self.solution_file_title = "gbfs-h"+str(search.heuristic)+"-sol-"+str(board_index+1)+".txt"
        elif issubclass(search.__class__, A):
            self.search_file_title = "a-h"+str(search.heuristic)+"-search-"+str(board_index+1)+".txt"
            self.solution_file_title = "a-h"+str(search.heuristic)+"-sol-"+str(board_index+1)+".txt"
        else:
            # ERROR
            pass

        # Make a directory to store the models if it doesn't already exist
        if not os.path.exists("results"):
            os.makedirs("results")
        self.results_folder = os.path.abspath("results")

    def solution_files(self):
        no_solution = False
        if (not os.path.isfile(f"{self.results_folder}/{self.solution_file_title}")) or self.overwrite_results: # if file doesn't exist or overwrite_results is True
            f = open(f"{self.results_folder}/{self.solution_file_title}", "w")
            sln_path = self.search.get_solution_path()
            if not self.search.result:
                no_solution = True
            # 2.3.1.1 - Initial Config
            output = "Initial Board Configuration: "
            for row in self.search.root.board:
                for char in row:
                    output += char
            for car in self.search.root.cars_dict:
                fuel = self.search.root.cars_dict[car].fuel
                if fuel < 100:
                    output += " " + car + "" + str(fuel)
            f.write(output + "\n")
            f.write("\n")
            # 2.3.1.1 - Initial Board Printing
            for row in self.board_reader.boards[0]:
                f.write(str(row) + "\n")
            f.write("\n")
            f.write("Car fuel Available: ")
            fuel_dict = self.board_reader.fueldicts[self.board_index]
            for car, fuel in fuel_dict.items():
                f.write(car + ":" + str(fuel) + ", ")
            f.write("\n" + "\n")
            if no_solution: # if no solution, write "No Solution Found" and return
                f.write("No Solution Found for This Board, Sorry!\n")
                f.write("Runtime: " + str(self.search.get_exec_time())+"\n")
                f.close()
                return # no need to write the rest of the file
            # 2.3.1.2
            f.write("Runtime: " + str(self.search.get_exec_time())+"\n")
            # 2.3.1.3
            f.write("Search Path Length: " + str(self.search.get_search_path_length())+" states"+"\n")
            # 2.3.1.4
            f.write("Solution Path Length: " + str(self.search.goal.cost)+" moves"+"\n")
            # 2.3.1.5
            output = "Solution Path: "
            node_number = 0
            for node in sln_path:

                # Movement done by node
                output += (str(node[0])+" "+str(node[1])+" "+str(node[2]) + "; ")
                node_number += 1
            f.write(output + "\n")
            f.write("\n")
            # 2.3.1.6
            node_number = 0
            for node in self.search.solution_path_nodes:
                output = ""
                # Movement done by node
                output += (str(sln_path[node_number][0])+" "+str(sln_path[node_number][1])+" "+str(sln_path[node_number][2])).ljust(20)
                # Fuel Remaining in Car moved
                fuel = node.cars_dict[sln_path[node_number][0]].fuel
                if fuel < 100:
                    output += " " + str(fuel) + " "
                # Resulting Board String
                for row in node.board:
                    for char in row:
                        output += char
                # Resulting Fuel Levels
                for car in node.cars_dict:
                    fuel = node.cars_dict[car].fuel
                    if fuel < 100:
                        output += " " + car + "" + str(fuel)
                # Increment node number
                f.write(output + "\n")
                node_number += 1
            f.write("\n")
            # 2.3.1.7
            output = "!"
            for car in node.cars_dict:
                fuel = node.cars_dict[car].fuel
                if fuel < 100:
                    output += " " + car + "" + str(fuel)
            f.write(output + "\n")
            for row in self.search.solution_path_nodes[len(self.search.solution_path_nodes)-1].board:
                f.write(str(row) + "\n")

            f.close()

    def search_files(self):
        if not os.path.isfile(f"{self.results_folder}/{self.search_file_title}") or self.overwrite_results: # if file doesn't exist or overwrite_results is True
            f = open(f"{self.results_folder}/{self.search_file_title}", "w")
            output = str(self.search.root.f_n) + " " + str(self.search.root.g_n) + " " + str(self.search.root.h_n) + " "
            for row in self.search.root.board:
                for char in row:
                    output += char
            for car in self.search.root.cars_dict:
                fuel = self.search.root.cars_dict[car].fuel
                if fuel < 100:
                    output += " " + car + "" + str(fuel)
            f.write(output + "\n")
            for node in self.search.search_path: # search_path is a list of nodes, it is the closed list
                f.write(str(node) + "\n")
            f.close()