# Output Generation for the Game's results
import os
from pathlib import Path

from utils.SearchAlgorithms import UniformCostSearch, GBFS, A
from utils.BoardReader import BoardReader

class OutputGeneration:

    def __init__(self, search, board_reader, board_index):
        '''Initializes the OutputGeneration Class
        search: search algorithm used and to be outputted
        board: board_reader used
        number: Board Number'''
        self.search = search
        self.board_reader = board_reader
        self.board_index = board_index
        if issubclass(search.__class__, UniformCostSearch):
            self.search_file_title = "ucs-search-"+str(board_index)+".txt"
            self.solution_file_title = "ucs-sol-"+str(board_index)+".txt"
        elif issubclass(search.__class__, GBFS):
            self.search_file_title = "gbfs-h"+str(search.heuristic)+"-search-"+str(board_index)+".txt"
            self.solution_file_title = "gbfs-h"+str(search.heuristic)+"-sol-"+str(board_index)+".txt"
        elif issubclass(search.__class__, A):
            self.search_file_title = "a-h"+str(search.heuristic)+"-search-"+str(board_index)+".txt"
            self.solution_file_title = "a-h"+str(search.heuristic)+"-sol-"+str(board_index)+".txt"
        else:
            # ERROR
            pass

        # Make a directory to store the models if it doesn't already exist
        if not os.path.exists("results"):
            os.makedirs("results")
        self.results_folder = os.path.abspath("results")

    def solution_files(self):
        if not os.path.isfile(f"{self.results_folder}/{self.solution_file_title}"):
            f = open(f"{self.results_folder}/{self.solution_file_title}", "w")
            sln_path = self.search.get_solution_path()
            if not self.search.result:
                f.write("no solution")
            else:
                f.write("Initial Board Configuration: " + str(self.search.solution_path_nodes[0])+"\n")
                f.write("\n")
                for row in self.board_reader.boards[0]:
                    f.write(str(row) + "\n")
                f.write("\n")
                f.write("Car fuel Available: ")
                fuel_dict = self.board_reader.fueldicts[self.board_index]
                for car, fuel in fuel_dict.items():
                    f.write(car + ":" + str(fuel) + ", ")
                f.write("\n" + "\n")
                f.write("Runtime: " + str(self.search.get_exec_time())+"\n")
                f.write("Search Path Length: " + str(self.search.get_search_path_length())+" states"+"\n")
                f.write("Solution Path Length: " + str(self.search.goal.cost)+" moves"+"\n")
                f.write("Solution Path: " + str(sln_path) + "\n")
                f.write("\n")
                output = ""
                node_number = 0
                # TODO - Figure out why this part (2.3.1.6 in pdf) isn't outputting
                for node in self.search.solution_path_nodes:
                    # Movement done by node
                    output += (str(sln_path[node_number][0])+" "+str(sln_path[node_number][1])+" "+str(sln_path[node_number][2]))
                    # Fuel Remaining in Car moved
                    fuel = node.cars_dict[sln_path[node_number][0]].fuel
                    if fuel < 100:
                        output += " " + str(fuel)
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
                    node_number += 1

                f.write("\n")
                for row in self.board_reader.boards[len(self.board_reader.boards)-1]:
                    f.write(str(row) + "\n")

            f.close()

    def search_files(self):
        if not os.path.isfile(f"{self.results_folder}/{self.search_file_title}"):
            f = open(f"{self.results_folder}/{self.search_file_title}", "w")
            for node in self.search.solution_path_nodes:
                f.write(str(node) + "\n")
            f.close()