from tkinter import *
from tkinter import filedialog
from input_reader import InputReader

# compute the height of a tree (naive method)
def compute_heigth(node, current):
    children = node.get_children()
    depths = []
    
    if len(children) == 0:
        return current
    else: 
        for i in children: 
            depths.append(compute_heigth(i, current+1))
        return max(depths)
    
class GUI:

    def __init__(self):
        # The path of the input file
        self.input_reader = None
        self.tree_nodes = []
        self.tree_height = 0
        self.selected_node = None
        self.selected_rect = None

        # Colors used
        self.bg_color = "#1A2227"
        self.second_color = "#22323C"
        self.node_color = "#fb0"
        self.select_color = "#a61b70"

    # presses a node and updates the information
    def node_press(self, node, rect):
        self.selected_label.config(text = "Selected = " + node.name)
        if (node.up == None):
            self.parent_label.config(text = "Parent = None")
        else:
            self.parent_label.config(text = "Parent = " + node.up.name)

        if (len(node.children) == 0):
            self.children_label.config(text = "Children = \nNone") 
        else:
            children_string = ""
            for i in node.children:
                children_string += "    "  + i.name + "\n"
            self.children_label.config(text = "Children = \n" + children_string) 

        # Keep track of what is selected
        if self.selected_rect != None:
            self.plot_canvas.itemconfig(self.selected_rect, fill =self.node_color)

        self.plot_canvas.itemconfig(rect, fill = self.select_color)
        self.selected_rect = rect
        self.selected_node = node

    # Draws the tree using a recursive call 
    def draw_tree(self, canvas, node, height, row, min_x, max_x):
        children = node.get_children()
        # compute our drawing bounds
        min_y = (canvas.winfo_height()/height)*(row-1)
        max_y = (canvas.winfo_height()/height)*row

        # Draw the current node
        if node.up == None:
            rectangle = canvas.create_rectangle(min_x, min_y, max_x, max_y, outline="#000000", 
                fill=self.node_color, tag="root_node" + node.name)
            canvas.tag_bind("root_node" + node.name, 
                "<Button-1>", lambda event, node=node, rect=rectangle:self.node_press(node, rect))
        else: 
            rectangle = canvas.create_rectangle(min_x, min_y, max_x, max_y, outline="#000000", 
                fill=self.node_color, tag=node.up.name + node.name)
            canvas.tag_bind(node.up.name + node.name, 
                "<Button-1>", lambda event, node=node, rect=rectangle:self.node_press(node, rect))

        # This means you see updates in between
        self.root.update()
        self.root.update_idletasks()

        # If there are children, draw those
        width = max_x - min_x
        if (len(children) > 0):
            portion = width/len(children)
            for i in range(len(children)):
                self.draw_tree(canvas, children[i], height, row+1, 
                    min_x+(portion*i), min_x+(portion*(i+1)))

    # This function facilitates the selection of the input file and the creation of the input 
    # reader object for it
    def import_button_function(self):
        path = filedialog.askopenfile(initialdir="/", title="Select file").name
        self.input_reader = InputReader(path[:len(path)-5])
        self.file_label.config(text = path[:len(path)-5])
        self.tree_height = compute_heigth(self.input_reader.get_tree(), 1)
        self.plot_canvas.delete("all")
        self.draw_tree(self.plot_canvas, self.input_reader.get_tree(), 
            self.tree_height, 1, 250, self.plot_canvas.winfo_width())

    # The event handler for pressing the change vis button
    def change_vis_button_function(self):
        if self.input_reader != None:
            print(self.input_reader.trees[0].ascii_art())
        else:
            print("no file selected yet")

    # The event handler for pressing the export button
    def export_button_function(self):
        print(self.import_button.winfo_width())

    # The event handler for resizing the screen, redraw and clear selection 
    def resize(self, event):
        if self.input_reader != None:
            self.plot_canvas.delete("all")
            self.draw_tree(self.plot_canvas, self.input_reader.get_tree(), 
                self.tree_height, 1, 250, self.plot_canvas.winfo_width())
            self.selected_label.config(text="[Selected Node]")
            self.parent_label.config(text="[Parent Node]")
            self.children_label.config(text="[Children Nodes]")
        
    def run_gui(self):
        
        # The root frame
        self.root = Tk()
        self.root.geometry("700x700")
        self.root.configure(background=self.bg_color)
        self.root.title("Circular Space Reclaiming Plots Visualizer")

        # This is where the plot will be 
        self.plot_canvas = Canvas(self.root, bg="pink")
        self.plot_canvas.pack(side=RIGHT, fill=BOTH, expand=TRUE)
        self.plot_canvas.bind("<Configure>", self.resize)

        # This is the frame for the rest (with grid layout)
        left_frame = Frame(self.root, bg = self.bg_color)
        left_frame.place(relheight=1, width = 250)
        # The grid layout
        left_frame.rowconfigure(0, weight=0)
        left_frame.rowconfigure(1, weight=0)
        left_frame.rowconfigure(2, weight=0)
        left_frame.rowconfigure(3, weight=0)
        left_frame.rowconfigure(4, weight=0)
        left_frame.rowconfigure(5, weight=1)
        left_frame.columnconfigure(0, weight=1)

        # The button/filethingy used for importing
        self.import_button = Button(left_frame, text="Import", bg=self.bg_color, fg="white", 
            activebackground=self.second_color, activeforeground="white", 
            command=self.import_button_function)
        self.import_button.grid(row=0, column=0, sticky="nsew", padx=(10,10), pady=(10,0))

        self.file_label = Label(left_frame, text="No file selected yet", 
            bg = self.bg_color, fg = "white", wraplength= 230, justify=LEFT, anchor="w")
        self.file_label.grid(row=1, column=0, sticky = "w", padx=(10,0), pady=(0,10))

        # The change vis button
        change_button = Button(left_frame, text="Change visualization", bg=self.bg_color, 
            fg="white", activebackground=self.second_color, activeforeground="white", 
            command=self.change_vis_button_function)
        change_button.grid(row=2, column=0, sticky="nsew", padx=(10,10), pady=(10,10))

        # The export button
        export_button = Button(left_frame, text="Export", bg=self.bg_color, fg="white", 
            activebackground=self.second_color, activeforeground="white",
            command=self.export_button_function)
        export_button.grid(row=3, column=0, sticky="nsew", padx=(10,10), pady=(10,10))

        # The animation speed slider (ugly)
        animation_speed = Scale(left_frame, from_=0, to=100, orient=HORIZONTAL, bg=self.bg_color, 
            fg="white", label="Animation Speed", showvalue=0, troughcolor=self.second_color, 
            highlightcolor=self.second_color, bd=1, highlightthickness=0, 
            activebackground=self.second_color)
        animation_speed.grid(row=4, column=0, sticky="ew", padx=(10,10), pady=(10,10))

        # The information frame
        information_frame = Frame(left_frame, bg = self.second_color)
        information_frame.grid(row=5, column=0, sticky="nsew", padx=(10,10), pady=(10,10))
        for i in range(3):
            information_frame.rowconfigure(i, weight=1)
        
        # selected node text
        self.selected_label = Label(information_frame, text="[Selected Node]", 
            bg = self.second_color, fg = "white", wraplength= 220, justify=LEFT, anchor="w")
        self.selected_label.grid(row=0, column=0, sticky = "w", padx=(10,10), pady=(10,10))

        # parent label text
        self.parent_label = Label(information_frame, text="[Parent Node]", 
            bg = self.second_color, fg = "white", wraplength= 220, justify=LEFT, anchor="w")
        self.parent_label.grid(row=1, column=0, sticky = "w", padx=(10,10), pady=(10,10))

        # List of children text
        self.children_label = Label(information_frame, text="[List of Children]", 
            bg = self.second_color, fg = "white", wraplength= 220, justify=LEFT, anchor="w")
        self.children_label.grid(row=2, column=0, sticky = "w", padx=(10,10), pady=(10,10))

        # details text (not needed rn)
        # self.detail_label = Label(information_frame, text="[Node details]", 
        #     bg = self.second_color, fg = "white", wraplength= 220, justify=LEFT, anchor="w")
        # self.detail_label.grid(row=3, column=0, sticky = "w", padx=(10,10), pady=(10,10))

        # Run the GUI
        self.root.mainloop()

