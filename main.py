# Main file to run the visualization tool
from icicle import Icicle
from input_reader import InputReader
from gui import GUI

class Main:

    def __init__(self, path):
        self.in_reader = InputReader(path)
        self.icicle = Icicle(self.in_reader.get_tree(), 700,700)
        self.icicle.drawIcicile()


# p = Main('./data/carnivora.newick')
gui = GUI()
gui.run_gui()
#p.in_reader.read_child()
