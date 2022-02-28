# Main file to run the visualization tool
from input_reader import InputReader

class Main:

    def __init__(self, path):
        self.in_reader = InputReader(path)


Main('./data/carnivora.newick')