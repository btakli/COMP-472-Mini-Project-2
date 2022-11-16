# Output Generation for the Game's results
from os import path
from pathlib import Path

from SearchAlgorithms import UniformCostSearch, GBFS, A

class OutputGeneration:

    def __init__(self, search, board):
        '''Initializes the OutputGeneration Class
        search: search algorithm used and to be outputted'''
        self.search = search
        self.board = board
        if issubclass(search, UniformCostSearch):
            self.search_file_title = "ucs-search-"+self.board.board+".txt"
            self.solution_file_title = "ucs-sol-"+self.board.board+".txt"
        elif issubclass(search,GBFS):
            self.search_file_title = "gbfs-h"+search(GBFS).heuristic+"-search-"+self.board.board+".txt"
            self.solution_file_title = "gbfs-h"+search(GBFS).heuristic+"-sol-"+self.board.board+".txt"
        elif issubclass(search,A):
            self.search_file_title = "a-h"+search(A).heuristic+"-search-"+self.board.board+".txt"
            self.solution_file_title = "a-h"+search(A).heuristic+"-sol-"+self.board.board+".txt"
        else:
            # ERROR
            pass
        super().__init__(search, board)

    def solutionPath(self):

    def searchPath(self):

    def solutionFiles(self):
        f = open(self.solution_file_title, "w")
        f.write("Initial Board Configuration: " + self.board.board)

        if searchResult
            pass

        f.close()
    def searchFiles(self):
        f = open(self.search_file_title, "w")
        for node in self.search.solution_path_nodes:
            f.write("f(n) = " + node + ",")
            f.write(" h(n) = " + node + ",")
            f.write(" g(n) = " + node + ",")
            f.write(" state = " + node + "\n")


        if searchResult
            pass

        f.close()