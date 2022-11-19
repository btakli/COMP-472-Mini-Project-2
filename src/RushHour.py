from os import path
from pathlib import Path

from utils.BoardManipulation import SubStateGenerator, TreeNode
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

    search = UniformCostSearch(boardslist[5], carslist[5], board_reader.exit)
    win_node = search.search()

    print(win_node)
    print(search.goal.cost)
    print(search.get_exec_time())
    print(search.search_path_length)
    print(search.solution_path)

    # sg = SubStateGenerator(boardslist[0], carslist[0], board_reader.exit)
    # sg.generate_substates()

    # for substate in sg.substates:
    #     for row in substate[0]:
    #         print(row)
    #     print()

    # t1 = TreeNode(boardslist[0], carslist[0], None, board_reader.exit, 0)
    # t2 = TreeNode(sg.substates[4][0], sg.substates[4][1], t1, board_reader.exit, 0)

    # print(f"{t2.car_moved} {t2.direction_moved} {t2.distance_moved}")
    


    # search2 = GBFS(boardslist[0], carslist[0], board_reader.exit, 1, 1)
    # win_node2 = search2.search()

    # print(win_node2)
    # print(search2.goal.cost)
    # print(search2.get_exec_time())
    # print(search2.search_path_length)
    # print(search2.solution_path)

# main
if __name__ == "__main__":
    main()
