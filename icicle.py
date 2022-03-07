# Class that constructs the icicle plot
from tkinter import *
from ete3 import Tree, TreeStyle

class Icicle:

    def __init__(self, tree, width, height):
        self.root = Tk()
        self.bg_color = "#1A2227"
        self.root.geometry("700x700")
        self.root.configure(background=self.bg_color)
        self.root.title("Circular Space Reclaiming Plots Visualizer")
        self.canvas = Canvas(self.root, width=width,height=height)
        self.canvas.pack()

        self.max_width = width
        self.max_height = height
        self.tree = tree
        self.tree_nodes = []
        self.tree_nodes.append({
            "node" : tree,
            "total_width" : width,
            "space_available" : width,
            "x" : [0, width],
            "y" : [0, 80]
        })
    
    def drawNode(self, node):
        x1 = self.max_width - self.space_available
        x2 = x1 + (len(node) / len(node.up) * self.max_width)
        y1 = 80
        y2 = 160
        self.canvas.create_rectangle(x1, y1, x2, y2,
            outline="#000000", fill="#fb0")
        self.canvas.create_text((x1+1, 80), text=node.name, anchor='nw')
        self.space_available = self.space_available - (x2 - x1)
        print(self.space_available)

    def drawIcicile(self):
        level = 1
        self.canvas.create_rectangle(0, 0, self.max_width, 80,
            outline="#000000", fill="#fb0")
        self.canvas.create_text((1, 0), text=self.tree.name, anchor='nw')
        self.space_available = self.max_width
        new_level = False

        for node in self.tree.traverse("preorder"):
            print(f"current node: {node.name}")
            if new_level:
                next_level = 1
                node_traverse = node.up
                new_level = False
                while (not node_traverse.is_root()):
                    node_traverse = node_traverse.up
                    next_level += 1
                print(next_level)

            if not node.is_root():
                self.drawNode(node)
                if not node.is_leaf():
                    level += 1
                else:
                    new_level = True
                
        self.root.mainloop()
        #boxWidth, space_available