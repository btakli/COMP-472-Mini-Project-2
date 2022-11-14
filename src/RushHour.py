from os import path
from pathlib import Path

from utils.BoardManipulation import SubStateGenerator, StateTree, BoardManipulator
from utils.BoardReader import BoardReader
from utils.SearchAlgorithms import UniformCostSearch, GBFS, A


def main():
    # get absolute path of input_file
    input_file = Path(path.abspath(__file__)).parent.parent / \
        "SampleInputOutput/Sample/sample-input.txt"

    board_reader = BoardReader(input_file)

    boards_list = board_reader.boards
    cars_list = board_reader.cars_board
    board_dimensions = board_reader.board_dimensions
    exit_pos = board_reader.exit

    board_reader.print_board(0)
    board_reader.print_cars_dict(0)

    # bm = BoardManipulator(board_dimensions, cars_list[0], exit_pos)

    # sg = SubStateGenerator(board_dimensions, cars_list[0], exit_pos)
    # sg.generate_substates()
    # sg2 = SubStateGenerator(board_dimensions, sg.substates[0], exit_pos)
    # sg2.generate_substates()
    # sg2.print_substates()

    # treenode = StateTree.TreeNode(board_dimensions, sg2.substates[0], None)

    # print(treenode.check_win(exit_pos))

    # exit(0)

    search = UniformCostSearch(boards_list[0], cars_list[0], exit_pos)
    win_node = search.search()

    print(win_node)
    print(f"Cost: {search.goal.cost}")
    print(search.get_exec_time())
    print(f"Search Path Length: {search.search_path_length}")
    print(f"Solution Path Length: {search.solution_path}")

# main
if __name__ == "__main__":
    main()


    # board_manipulator = BoardManipulator(board_dimensions, cars_list[0], board_reader.exit)
    # board_manipulator.print_board()

    # board_manipulator.move_car("M", "down")
    # board_manipulator.move_car("A", "right")
    # board_manipulator.move_car("B", "right")
    # board_manipulator.move_car("C", "right")

    # board_manipulator.remove_from_valet_if_exists()

    # board_manipulator.print_board()
    # board_manipulator.print_cars_dict()

    # board_reader.print_board(0)
    # board_reader.print_cars_dict(0)

# board_manipulator.remove_from_valet_if_exists()

# board_manipulator.print_board()
# board_manipulator.print_cars_dict()

# board_reader.print_board(0)
# board_reader.print_cars_dict(0)
