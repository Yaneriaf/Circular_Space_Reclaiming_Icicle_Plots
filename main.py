# Main file to run the visualization tool
from input_reader import InputReader
from gui import GUI

class Main:

    def __init__(self, path):
        self.in_reader = InputReader(path)


# p = Main('./data/carnivora.newick')
gui = GUI()
gui.run_gui()
# p.in_reader.read_child()