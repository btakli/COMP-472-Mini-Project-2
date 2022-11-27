from os import path
from pathlib import Path

from utils.AnalysisOutput import AnalysisOutput
from utils.BoardReader import BoardReader
from utils.OutputGeneration import OutputGeneration
from utils.SearchAlgorithms import GBFS, A, UniformCostSearch


def main():
    # get absolute path of input_file
    input_file = Path(path.abspath(__file__)).parent / "input.txt"
    
    analysisoutput = AnalysisOutput("analysis.csv")

    board_reader = BoardReader(input_file)

    boardslist = board_reader.boards
    carslist = board_reader.cars_board



    heuristics_list = [1,2,3,4]
    # default value for lambda_val. Can modify for h3
    lambda_val = 2
    # 0.5 is the default value, but you can change it to see how it affects the results. Basically weight of h1 and h2 in the h4 heuristic
    h4_weight_factor = 0.6 



    print("~~~Running all search algorithms. *NOTE: Only the output for UCS is shown in the console for illustrative purposes.~~~")
    # for each board in the input file
    for i in range(len(boardslist)):
        board_reader.print_board(i)
        board_reader.print_cars_dict(i)
        ucs = UniformCostSearch(boardslist[i], carslist[i], board_reader.exit)
        win_node = ucs.search()
        if win_node is not None:
            print(f"Win Node: {win_node}")
            print(f"Total cost: {ucs.goal.cost}")
            print(f"Solution (path): {ucs.solution_path}")
        else:
            print("No solution found.")

        print(f"Execution time: {ucs.get_exec_time()}")
        print(f"Length of the search path: {ucs.search_path_length}")
        
        # Output Files Generation for UC Search
        output_generator = OutputGeneration(ucs, board_reader, i, True)
        output_generator.search_files()
        output_generator.solution_files()

        # Analysis Output for UC Search
        if win_node is not None:
            analysisoutput.add_row(i+1, "UCS", "N/A", ucs.goal.cost, ucs.search_path_length, ucs.get_exec_time())
        else:
            analysisoutput.add_row(i+1, "UCS", "N/A", "No Solution", ucs.search_path_length, ucs.get_exec_time())

        
        # Search Algorithm GBFS using Heuristics
        for heuristic in heuristics_list:
            gbfs = GBFS(boardslist[i], carslist[i], board_reader.exit, heuristic, lambda_value=lambda_val, weighted_avg_factor=h4_weight_factor)
            win_node = gbfs.search()
            output_generator = OutputGeneration(gbfs, board_reader, i, True)
            output_generator.search_files()
            output_generator.solution_files()

            # Analysis Output for GBFS
            if win_node is not None:
                analysisoutput.add_row(i+1, "GBFS", f"h{heuristic}", gbfs.goal.cost, gbfs.search_path_length, gbfs.get_exec_time())
            else:
                analysisoutput.add_row(i+1, "GBFS", f"h{heuristic}", "No Solution", gbfs.search_path_length, gbfs.get_exec_time())

         # Search Algorithm A/A* using Heuristics
        for heuristic in heuristics_list:
            a = A(boardslist[i], carslist[i], board_reader.exit, heuristic, lambda_value=lambda_val, weighted_avg_factor=h4_weight_factor)
            win_node = a.search()
            output_generator = OutputGeneration(a, board_reader, i, True)
            output_generator.search_files()
            output_generator.solution_files()

            # Analysis Output for A*
            if win_node is not None:
                analysisoutput.add_row(i+1, "A/A*", f"h{heuristic}", a.goal.cost, a.search_path_length, a.get_exec_time())
            else:
                analysisoutput.add_row(i+1, "A/A*", f"h{heuristic}", "No Solution", a.search_path_length, a.get_exec_time())

# main
if __name__ == "__main__":
    main()
