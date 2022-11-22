import csv
import os


class AnalysisOutput:
    """Class to create the output of the analysis. A CSV file is created in the end."""
    def __init__(self, file_name):
        """Create the CSV file and analysis directory if it doesnt exist"""
        if not os.path.exists("analysis"):
            os.makedirs("analysis")
        self.analysis_folder = os.path.abspath("analysis")
        self.file_name = file_name
        self.filepath = os.path.join(self.analysis_folder, self.file_name)

        with open(self.filepath, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['Puzzle Number', 'Algorithm', 'Heuristic', 'Length of the Solution', 'Length of the Search Path', 'Execution Time (in seconds)'])
    
    def add_row(self, puzzle_number: int, algorithm: str, heuristic: str, solution_length: str, search_path_length: int, execution_time: float):
        """Add a row to the CSV file"""
        with open(self.filepath, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([puzzle_number, algorithm, heuristic, solution_length, search_path_length, execution_time])