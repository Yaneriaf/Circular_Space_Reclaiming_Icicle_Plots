# Class that reads the given input and allows other classes to access
import io
import newick as nw

with io.open('data/carnivora.newick', encoding='utf8') as file:
    trees = nw.load(file)

def read_child():
    
    

