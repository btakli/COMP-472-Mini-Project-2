from utils.BoardReader import BoardReader
from utils.BoardManipulator import BoardManipulator
from pathlib import Path
from os import path

# get absolute path of input_file
input_file = Path(path.abspath(__file__)).parent.parent / "SampleInputOutput/Sample/sample-input.txt"

board_reader = BoardReader(input_file)

boardslist = board_reader.boards
carslist = board_reader.cars_board

board_reader.print_board(0)
board_reader.print_cars_dict(0)

board_manipulator = BoardManipulator(boardslist[0], carslist[0], board_reader.exit)
board_manipulator.move_car("M", "down")
board_manipulator.move_car("A", "right")
board_manipulator.move_car("B", "right")
board_manipulator.move_car("C", "right")

board_manipulator.remove_from_valet_if_exists()

board_manipulator.print_board()
board_manipulator.print_cars_dict()

board_reader.print_board(0)
board_reader.print_cars_dict(0)

# for i in range(len(board_reader.boards)):
#     board_reader.print_board(i)
#     board_reader.print_fuel_dict(i)
#     board_reader.print_cars_dict(i)
