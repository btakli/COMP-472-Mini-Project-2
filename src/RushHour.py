from os import path
from pathlib import Path

from utils.BoardManipulation import SubStateGenerator
from utils.BoardReader import BoardReader


def win_check(cars_dict: dict) -> bool:
    '''Checks if the ambulance has reached the exit'''
    ambulance = cars_dict["A"]
    if ambulance.position == None:  # Check if the ambulance has reached the exit, meaning it is no longer on the board due to the valet parking
        return True
    else:
        return False


def main():
    # get absolute path of input_file
    input_file = Path(path.abspath(__file__)).parent.parent / \
        "SampleInputOutput/Sample/sample-input.txt"

    board_reader = BoardReader(input_file)

    boardslist = board_reader.boards
    carslist = board_reader.cars_board

    board_reader.print_board(0)
    board_reader.print_cars_dict(0)

    substate_generator = SubStateGenerator(
        boardslist[0], carslist[0], board_reader.exit)
    substate_generator.generate_substates()
    substate_generator.print_substates()


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
