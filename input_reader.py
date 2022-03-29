# Class that reads the given input and allows other classes to access
# from asyncio.windows_events import NULL
import io
import newick as nw
from ete3 import Tree
import numpy as np   # numerical library

class InputReader:

    def __init__(self, path):
        with io.open(path, encoding='utf8') as file:
            self.newick_tree = nw.load(file)

        f = open(path, "r")
        self.tree = Tree(f.read(), format=1)
        print(self.tree)

    def read_child(self, node):
        return node.descendants
            
    def get_tree(self):
        return self.tree
