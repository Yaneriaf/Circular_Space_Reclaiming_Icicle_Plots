# Class that reads the given input and allows other classes to access
import io
import newick as nw

class InputReader:

    def __init__(self, path):
        with io.open(path, encoding='utf8') as file:
            self.trees = nw.load(file)[0]
            print(self.trees.ascii_art())

    def read_child():
        pass
