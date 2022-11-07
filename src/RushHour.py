from utils.BoardReader import BoardReader
from pathlib import Path
from os import path

# get absolute path of input_file
input_file = Path(path.abspath(__file__)).parent.parent / "SampleInputOutput/Sample/sample-input.txt"

board_reader = BoardReader(input_file)

for i in range(len(board_reader.boards)):
    board_reader.print_board(i)
    board_reader.print_fuel_dict(i)
    board_reader.print_cars_dict(i)
