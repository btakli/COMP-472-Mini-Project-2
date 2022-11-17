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
    board_index = 0

    boardslist = board_reader.boards
    carslist = board_reader.cars_board

    board_reader.print_board(board_index)
    board_reader.print_cars_dict(board_index)

    # tn = TreeNode(boardslist[board_index], carslist[board_index], None, board_reader.exit, 1, 2.0)
    # print(tn.h_n)
    # sg = SubStateGenerator(boardslist[board_index], carslist[board_index], board_reader.exit)
    # sg.generate_substates()

    # sg2 = SubStateGenerator(sg.substates[0][0], sg.substates[0][1], board_reader.exit)
    # sg2.generate_substates()
    # sg2.print_substates()
    # for substate in sg2.substates:
    #     print(TreeNode(substate[0], substate[1], None, board_reader.exit, 1, 2.0).h_n)

    # exit(0)

    search = UniformCostSearch(boardslist[board_index], carslist[board_index], board_reader.exit)
    win_node = search.search()

    print(win_node)
    print(search.goal.cost)
    print(search.get_exec_time())
    print(search.search_path_length)
    print(search.solution_path)

    # Output Files Generation
    output_generator = OutputGeneration(search, board_reader, board_index)
    output_generator.search_files()
    output_generator.solution_files()

    # search2 = GBFS(boardslist[board_index], carslist[board_index], board_reader.exit, 1, 1)
    # win_node2 = search2.search()

    # print(win_node2)
    # print(search2.goal.cost)
    # print(search2.get_exec_time())
    # print(search2.search_path_length)
    # print(search2.solution_path)

    # # Output Files Generation
    # output_generator2 = OutputGeneration(search2, board_reader, board_index)
    # output_generator2.search_files()
    # output_generator2.solution_files()

    # search3 = A(boardslist[board_index], carslist[board_index], board_reader.exit, 1, 1)
    # win_node3 = search3.search()

    # print(search3.goal.cost)
    # print(search3.get_exec_time())
    # print(search3.search_path_length)
    # print(search3.solution_path)
    # print(win_node3)

    # # Output Files Generation
    # output_generator3 = OutputGeneration(search3, board_reader, board_index)
    # output_generator3.search_files()
    # output_generator3.solution_files()

# main
if __name__ == "__main__":
    main()


# board_manipulator = BoardManipulator(boardslist[0], carslist[0], board_reader.exit)
# board_manipulator.move_car("M", "down")
# board_manipulator.move_car("A", "right")
# board_manipulator.move_car("B", "right")
# board_manipulator.move_car("C", "right")

# board_manipulator.remove_from_valet_if_exists()

# board_manipulator.print_board()
# board_manipulator.print_cars_dict()

# board_reader.print_board(0)
# board_reader.print_cars_dict(0)
