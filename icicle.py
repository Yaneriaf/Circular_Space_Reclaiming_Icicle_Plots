# Class that constructs the icicle plot
from tkinter import *
from ete3 import Tree

class Icicle:

    def __init__(self, tree, width, height):
        self.root = Tk()
        self.bg_color = "#1A2227"
        self.root.geometry("700x700") # this might needs to change?
        self.root.configure(background=self.bg_color)
        self.root.title("Circular Space Reclaiming Plots Visualizer")
        self.canvas = Canvas(self.root, width=width,height=height)
        self.canvas.pack()

        # Set up boundaries
        self.max_width = width
        self.max_height = height
        self.tree = tree

        #Store the root already in dictionary for drawing
        self.tree_nodes = []
        self.tree_nodes.append({
            "node" : tree,
            "total_width" : width,
            "space_available" : width,
            "x" : [0, width],
            "y" : [0, 80]
        })
    
    # Will draw an internal node or a leave given a node from the tree.
    # TODO: Node height is set to a base value (80), maybe make this adaptable or change to fit long trees better
    def drawNode(self, node):
        # Get the parent of the node and find its values in the dictionary
        parent = next(item for item in self.tree_nodes if item["node"] == node.up)

        # Calculate coordinates for the node
        x1 = parent["x"][0] + parent["total_width"] - parent["space_available"]
        x2 = x1 + (len(node) / len(node.up) * parent["total_width"])
        y1 = parent["y"][1]
        y2 = parent["y"][1] + 80

        # Draw the rectangle and give it a label using Tkinter
        self.canvas.create_rectangle(x1, y1, x2, y2,
            outline="#000000", fill="#fb0")
        self.canvas.create_text((x1+1, y1), text=node.name, anchor='nw')

        # Update the space available for the parent of the node
        parent["space_available"] = parent["space_available"] - (x2 - x1)

        # Add the new node drawn to the dictionary for its children
        self.tree_nodes.append({
            "node" : node,
            "total_width" : (x2 - x1),
            "space_available" : (x2 - x1),
            "x" : [x1, x2],
            "y" : [y1, y2]
        })

    def drawIcicile(self):
        # Draws the root first
        self.canvas.create_rectangle(0, 0, self.max_width, 80,
            outline="#000000", fill="#fb0")
        self.canvas.create_text((1, 0), text=self.tree.name, anchor='nw')

        # Traverse through the tree in preorder: root -> left subtree -> right subtree
        for node in self.tree.traverse("preorder"):
            if not node.is_root():
                self.drawNode(node)
                
        self.root.mainloop()