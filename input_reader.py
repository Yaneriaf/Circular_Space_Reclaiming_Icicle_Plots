# Class that reads the given input and allows other classes to access
# from asyncio.windows_events import NULL
import io
import newick as nw
from ete3 import Tree
import numpy as np   # numerical library

class InputReader:

    def __init__(self, path):
        with io.open(path, 'r', encoding='utf-8') as file:
            self.tree = Tree(file.read(), format=1)
            file.close()
            
    def get_tree(self):
        return self.tree
