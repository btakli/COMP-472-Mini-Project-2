from os import path
from pathlib import Path

from utils.BoardManipulation import SubStateGenerator, StateTree
from utils.BoardReader import BoardReader
from utils.SearchAlgorithms import UniformCostSearch, GBFS, A


def main():
    # get absolute path of input_file
    input_file = Path(path.abspath(__file__)).parent.parent / \
        "SampleInputOutput/Sample/sample-input.txt"

    board_reader = BoardReader(input_file)

    boardslist = board_reader.boards
    carslist = board_reader.cars_board

    board_reader.print_board(0)
    board_reader.print_cars_dict(0)
    print(carslist[0]['L'].tailposition)

    search = UniformCostSearch(boardslist[0], carslist[0], board_reader.exit)
    win_node = search.search()

    print(search.goal.cost)
    print(win_node)
    print(search.get_exec_time())
    print(search.search_path_length)
    print(search.solution_path)

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
