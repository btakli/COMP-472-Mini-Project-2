from os import path
from pathlib import Path

from utils.BoardManipulation import SubStateGenerator, TreeNode
from utils.BoardReader import BoardReader
from utils.OutputGeneration import OutputGeneration
from utils.SearchAlgorithms import UniformCostSearch, GBFS, A


def main():
    # get absolute path of input_file
    input_file = Path(path.abspath(__file__)).parent.parent / \
        "SampleInputOutput/Sample/sample-input.txt"

    board_reader = BoardReader(input_file)

    boardslist = board_reader.boards
    carslist = board_reader.cars_board
    # board_index = 0

    # board_reader.print_board(board_index)
    # board_reader.print_cars_dict(board_index)

    # search = UniformCostSearch(boardslist[board_index], carslist[board_index], board_reader.exit)
    # win_node = search.search()

    # if not(win_node is None):
    #     print(win_node)
    #     print(search.goal.cost)
    #     print(search.get_exec_time())
    #     print(search.search_path_length)
    #     print(search.solution_path)


    # else:
    #     # Output Files Generation
    #     output_generator = OutputGeneration(search, board_reader, board_index)
    #     output_generator.search_files()
    #     output_generator.solution_files()
    #     print("No solution")

    # print("GBFS")
    # search2 = GBFS(boardslist[board_index], carslist[board_index], board_reader.exit, 1, 2)
    # win_node2 = search2.search()

    # print(win_node2)
    # print(search2.goal.cost)
    # print(search2.get_exec_time())
    # print(search2.search_path_length)
    # print(search2.solution_path_nodes)
    # print(search2.solution_path)

    # exit(0)

    # for each board in the input file
    for i in range(len(boardslist)):
        board_reader.print_board(i)
        board_reader.print_cars_dict(i)
        ucs = UniformCostSearch(boardslist[i], carslist[i], board_reader.exit)
        win_node = ucs.search()
        if win_node is not None:
            print(win_node)
            print(ucs.goal.cost)
            print(ucs.get_exec_time())
            print(ucs.search_path_length)
            print(ucs.solution_path)
        # Output Files Generation for UC Search
        output_generator = OutputGeneration(ucs, board_reader, i, True)
        output_generator.search_files()
        output_generator.solution_files()
        
        # Search Algorithms using Heuristics
        for heuristic in range(1, 4): #TODO change to 5 since we need to add a 4th heuristic
            gbfs = GBFS(boardslist[i], carslist[i], board_reader.exit, heuristic)
            win_node = gbfs.search()
            output_generator = OutputGeneration(gbfs, board_reader, i, True)
            output_generator.search_files()
            output_generator.solution_files()

            # a = A(boardslist[i], carslist[i], board_reader.exit, heuristic)
            # win_node = a.search()
            # output_generator = OutputGeneration(a, board_reader, i, True)
            # output_generator.search_files()
            # output_generator.solution_files()

# main
if __name__ == "__main__":
    main()
