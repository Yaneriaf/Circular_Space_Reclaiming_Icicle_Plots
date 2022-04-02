import colorsys
from math import floor
from time import sleep
from tkinter import *
from tkinter import filedialog
from input_reader import InputReader
from PIL import Image
import numpy as np

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

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)
    
class GUI:

    def __init__(self):
        # The path of the input file
        self.input_reader = None
        self.tree_nodes = []
        self.tree_height = 0
        self.selected_node = None
        self.selected_rect = None
        self.sunburst_selected = False
        self.redraw = False

        # Colors used
        self.bg_color = "#1A2227"
        self.second_color = "#22323C"
        self.node_color = "#fb0"
        self.select_color = "#a61b70"
        self.mid_x = 350
        self.mid_y = 350

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

        self.node_color = self.plot_canvas.itemcget(rect, "fill")
        self.plot_canvas.itemconfig(rect, fill = self.select_color)
        self.selected_rect = rect
        self.selected_node = node

    # Start the drawing and recursion steps for the reclaiming icicle plot
    def draw_reclaiming_driver(self, canvas, node, height, row, min_x, max_x, sunburst):
        self.gap_size = int(self.gap_size_entry.get())
        self.shrinking_factor = float(self.shrinking_factor_entry.get())
        self.max_span = int(self.max_span_entry.get())
        self.space_reclaiming_factor = float(self.space_reclaiming_factor_entry.get())
        self.hue_color = int(self.hue_color_entry.get())

        # Needed for color later
        self.number_of_nodes = len(node)
        # These two lines might not be needed, but nice to have for maybe the sunburst
        self.max_node_size = max_x
        offset = min_x + (max_x - self.max_node_size)/2

        # Drawing is based on which dimension in the smallest
        smallest_direction = min(self.mid_x, self.mid_y)
        # Outer ring starting point of the arc
        sunburst_offset = (smallest_direction / self.tree_height) * (self.tree_height-height+1)

        # Maximal width of all nodes
        self.max_width = max_x - min_x

        # Calculate the height of the root and use this for other nodes as well
        min_y = (canvas.winfo_height()/height)*(row-1)
        max_y = (canvas.winfo_height()/height)*row
        self.height = max_y - min_y

        h = self.hue_color / 360
        s = 1 - 1/self.tree_height
        v = min(0.3 + 0.7 * 1/self.tree_height, 1)
        rgb = colorsys.hsv_to_rgb(h,s,v)
        hex = rgb2hex(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        outline_rgb = colorsys.hsv_to_rgb(h,s,0.7*v)
        outline_hex = rgb2hex(int(outline_rgb[0]*255), int(outline_rgb[1]*255), int(outline_rgb[2]*255))

        # Coordinates drawing based on circular or horizontal
        if sunburst:
            coords = []
            for i in range(min_x, max_x):
                coords.append((self.mid_x + sunburst_offset * np.cos((i/20) * np.pi / 180),
                            self.mid_y + sunburst_offset * np.sin((i/20) * np.pi / 180)))
        else:
            coords = [offset,min_y,max_x,min_y, max_x,max_y,offset,max_y]

        # Draw the actual polygon
        polygon = canvas.create_polygon(coords, outline=outline_hex, 
                fill=hex, tag="root_node" + node.name)
        canvas.tag_bind("root_node" + node.name, 
                "<Button-1>", lambda event, node=node, rect=polygon:self.node_press(node, rect))

        # Store certain values for all nodes, only root is filled with correct information.
        # The other nodes are needed for later and will be adjusted then to correct values
        self.tree_nodes = []
        for n in node.traverse("levelorder"):
            self.tree_nodes.append({
            "node" : n,
            "x" : offset,
            "y" : max_y,
            "w" : self.max_node_size,
            "sticky": False,
            "span": 0,
            "fill" : hex
        })

        children = node.get_children()
        if (len(children) > 0):
            self.draw_reclaiming(1, [node], len(children), len(node), max_x-min_x, 0, canvas, sunburst)
        
    """
    The recursive method for reclaiming icicle plot, this is called from the driver

    Parameters
    ----------
    d : integer
        current depth
    P : List
        List of all parent nodes at depth d-1
    m : integer
        m > 0, number of child nodes at depth d
    A : integer
        accumulated weight of child nodes at depth d
    w : integer
        available horizontal space at depth d
    g : integer
        width taken by sticky nodes at depth d
    canvas : tkinter canvas object
        width taken by sticky nodes at depth d
    sunburst : Boolean
        Whether we need to draw a circle or not 
    """
    def draw_reclaiming(self, d, P, m, A, w, g, canvas, sunburst):
        # calculate the adaptive gap size and make sure it is not negative
        adaptive_gap_size = 0
        if m > 1:
            adaptive_gap_size = max(0, min(self.gap_size, floor((w-g-m)/(m-1))))

        if adaptive_gap_size == 0 and g > m:
            w = g
        
        # Get usable space at the current depth d
        useable_space_U = w - g - (m-1) * adaptive_gap_size

        # Get lower left coordinate point of child
        x = (self.max_width - w)/2
        if sunburst:
            y = (min(self.mid_x, self.mid_y) / self.tree_height) * (d+1)
        else:
            y = (d + 1) * self.height

        # Parameters used for the next recursive call
        new_P = []
        new_m = 0
        new_A = 0
        new_w = 0
        new_g = 0

        # Go through the current list of parents at depth d-1, level order
        for i in range(0, len(P)):
            # find node in dictionary
            p_node = next(item for item in self.tree_nodes if item["node"] == P[i]) 
            
            if sunburst:
                # inner left coordinate point
                p_0 = [p_node["x"], ((min(self.mid_x, self.mid_y) / self.tree_height) * d)]
            else:
                # Upper left coordinate point of child
                p_0 = [p_node["x"], p_node["y"]]
            
            # If the node is a child
            if p_node["sticky"]:
                children = [P[i]]
            else:
                children = P[i].get_children()
            
            for child in children:
                # find child in dictionary
                c = next(item for item in self.tree_nodes if item["node"] == child) 
                if c["sticky"]:
                    # Upper right coordinate point of child
                    p_1 = [p_0[0] + p_node["w"], p_0[1]] 
                    # shrink the sticky node (reclaim)
                    c["w"] = p_node["w"] * self.shrinking_factor 
                    x = x + c["w"]
                    c["span"] += 1
                else:
                    # Upper right coordinate point of child
                    p_1 = [p_0[0] + (len(child)/len(child.up)) * p_node["w"], p_0[1]]
                    # Get the portion of usable space for the child
                    delta = len(child)/A * useable_space_U
                    # check to be not over the maximum allowed size
                    delta_width = min(delta, self.max_node_size) 
                    offset = (delta - delta_width)/2 

                    # Calculate color in hsv and convert to rgb and then to hex
                    h = self.hue_color / 360
                    s = max(0.3, 1 - d/self.tree_height)
                    v = min(0.3 * len(child)/self.number_of_nodes + 0.7 * d/self.tree_height, 1)
                    rgb = colorsys.hsv_to_rgb(h,s,v)
                    hex = rgb2hex(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
                    outline_rgb = colorsys.hsv_to_rgb(h,s,0.7*v)
                    outline_hex = rgb2hex(int(outline_rgb[0]*255), int(outline_rgb[1]*255), 
                        int(outline_rgb[2]*255))

                    if sunburst:
                        # for drawing a circle we need to add points
                        coords = []

                        # outer ring
                        for i in range(int(x+offset), int(x+offset+delta_width)):
                            coords.append((self.mid_x + y * np.cos((i/20) * np.pi / 180),
                                        self.mid_y + y * np.sin((i/20) * np.pi / 180)))
                        
                        # inner ring
                        for i in range(int(p_1[0]), int(p_0[0]), -1):
                            coords.append((self.mid_x + p_0[1] * np.cos((i/20) * np.pi / 180),
                                        self.mid_y + p_0[1] * np.sin((i/20) * np.pi / 180)))
                    else: 
                        coords = [p_0,p_1,[x+offset+delta_width, y], [x+offset, y]]

                    
                    polygon = canvas.create_polygon(coords, outline=outline_hex, 
                        fill=hex, tag="root_node" + child.name)
                    canvas.tag_bind("root_node" + child.name, 
                        "<Button-1>", lambda event, node=child, 
                        rect=polygon:self.node_press(node, rect))
                    
                    # Save the position and width of the drawn child
                    c["x"] = x+offset
                    c["y"] = y
                    c["w"] = delta_width
                    c["fill"] = hex
                    x = x + delta + adaptive_gap_size
                
                # Points shift for the next child in level order
                p_0 = p_1 

                # Set up parameters for next recursive call
                new_C = child.get_children()
                n = len(new_C)
                c["sticky"] = n == 0
                if c["sticky"] and c["span"] < self.max_span:
                    new_P = new_P + [child]
                    new_g += c["w"]
                if not c["sticky"]:
                    new_P = new_P + [child]
                    new_m += n
                    weight_new_C = 0
                    for t in new_C:
                        weight_new_C += len(t)
                    new_A += weight_new_C
                    new_w += delta

        # This means you see updates in between
        self.root.update()
        self.root.update_idletasks()
        
        # If there are more children then continue recursive call to the next level, at depth d+1
        if new_m > 0:
           self.draw_reclaiming(d+1, new_P, new_m, new_A, 
                (new_w + self.space_reclaiming_factor * (self.max_width - new_w)), 
                (new_g * self.shrinking_factor), canvas, sunburst)

    # This function facilitates the selection of the input file and the creation of the input 
    # reader object for it
    def import_button_function(self):
        path = filedialog.askopenfile(initialdir="/", title="Select file").name
        self.input_reader = InputReader(path[:len(path)-5])
        self.file_label.config(text = path[:len(path)-5])
        self.tree_height = compute_heigth(self.input_reader.get_tree(), 1)
        self.plot_canvas.delete("all")
        self.sunburst_selected = False
        self.draw_reclaiming_driver(self.plot_canvas, self.input_reader.get_tree(),
                                    self.tree_height, 1, 0, self.plot_canvas.winfo_width(), False)
        # self.draw_reclaiming_driver(self.plot_canvas, self.input_reader.get_tree(),
        #                             self.tree_height, 1, 0, 7200, True)              

    # The event handler for pressing the change vis button
    def change_vis_button_function(self):
        if self.input_reader != None:
            if self.redraw:
                if self.sunburst_selected:
                    self.draw_reclaiming_driver(self.plot_canvas, self.input_reader.get_tree(), 
                        self.tree_height, 1, 0, 7200, True)
                else:
                    self.draw_reclaiming_driver(self.plot_canvas, self.input_reader.get_tree(),
                        self.tree_height, 1, 0, self.plot_canvas.winfo_width(), False)
                self.redraw = False
                self.change_button.config(text = "Change visualization")
            else:
                self.plot_canvas.delete("all")
                if self.sunburst_selected:
                    self.sunburst_selected = False
                    self.draw_reclaiming_driver(self.plot_canvas, self.input_reader.get_tree(),
                                        self.tree_height, 1, 0, self.plot_canvas.winfo_width(), 
                                        False)
                else:
                    self.sunburst_selected = True
                    self.draw_reclaiming_driver(self.plot_canvas, self.input_reader.get_tree(), 
                        self.tree_height, 1, 0, 7200, True)
            
        else:
            print("no file selected yet")

        self.selected_label.config(text="[Selected Node]")
        self.parent_label.config(text="[Parent Node]")
        self.children_label.config(text="[Children Nodes]")

    # The event handler for pressing the export button
    def export_button_function(self):
        self.plot_canvas.postscript(file="export.eps")
        img = Image.open("export.eps")
        img.save("export.png", "png")
        print(self.import_button.winfo_width())

    # Update parameters and redraw
    def apply_button_function(self):
        self.plot_canvas.delete("all")
        self.gap_size = int(self.gap_size_entry.get())
        self.shrinking_factor = float(self.shrinking_factor_entry.get())
        self.max_span = int(self.max_span_entry.get())
        self.space_reclaiming_factor = float(self.space_reclaiming_factor_entry.get())
        self.hue_color = int(self.hue_color_entry.get())

        if self.sunburst_selected:
            self.draw_reclaiming_driver(self.plot_canvas, self.input_reader.get_tree(),
                self.tree_height, 1, 0, 7200, True)
        else:
            self.draw_reclaiming_driver(self.plot_canvas, self.input_reader.get_tree(),
                self.tree_height, 1, 0, self.plot_canvas.winfo_width(), False)

    # The event handler for resizing the screen, redraw and clear selection 
    def resize(self, event):
        self.mid_x = (self.plot_canvas.winfo_width())/2
        self.mid_y = self.plot_canvas.winfo_height()/2
        # Instead of immediately redrawing we will create a message to click the canvas to redraw
        if self.input_reader != None:
            self.plot_canvas.delete("all")
            self.redraw = True
            self.change_button.config(text = "Redraw")
            
            self.selected_label.config(text="[Selected Node]")
            self.parent_label.config(text="[Parent Node]")
            self.children_label.config(text="[Children Nodes]")
        
    def run_gui(self):
        
        # The root frame
        self.root = Tk()
        self.root.geometry("1000x700")
        self.root.configure(background=self.bg_color)
        self.root.title("Circular Space Reclaiming Plots Visualizer")

        # This is the frame for the rest (with grid layout)
        left_frame = Frame(self.root, bg = self.bg_color, width = 250)
        left_frame.pack(side=LEFT, fill=Y)
        # left_frame.place(relheight=1, width = 250)
        # The grid layout
        left_frame.rowconfigure(0, weight=0)
        left_frame.rowconfigure(1, weight=0)
        left_frame.rowconfigure(2, weight=0)
        left_frame.rowconfigure(3, weight=0)
        left_frame.rowconfigure(4, weight=0)
        left_frame.rowconfigure(5, weight=1)
        left_frame.rowconfigure(6, weight=1)
        left_frame.columnconfigure(0, weight=1)

        # This is where the plot will be 
        self.plot_canvas = Canvas(self.root, bg="pink")
        self.plot_canvas.pack(side=RIGHT, fill=BOTH, expand=TRUE)
        self.plot_canvas.bind("<Configure>", self.resize)

        # The button/filethingy used for importing
        self.import_button = Button(left_frame, text="Import", bg=self.bg_color, fg="white", 
            activebackground=self.second_color, activeforeground="white", 
            command=self.import_button_function)
        self.import_button.grid(row=0, column=0, sticky="nsew", padx=(10,10), pady=(10,0))

        self.file_label = Label(left_frame, text="No file selected yet", 
            bg = self.bg_color, fg = "white", wraplength= 150, justify=LEFT, anchor="w")
        self.file_label.grid(row=1, column=0, sticky = "w", padx=(10,0), pady=(0,10))

        # The change vis button
        self.change_button = Button(left_frame, text="Change visualization", bg=self.bg_color, 
            fg="white", activebackground=self.second_color, activeforeground="white", 
            command=self.change_vis_button_function)
        self.change_button.grid(row=2, column=0, sticky="nsew", padx=(10,10), pady=(10,10))

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

        # The parameter frame
        parameter_frame = Frame(left_frame, bg = self.bg_color)
        parameter_frame.grid(row=5, column=0, sticky="nsew", padx=(10,10), pady=(10,10))
        for i in range(5):
            parameter_frame.rowconfigure(i, weight=1)
        for i in range(2):
            parameter_frame.columnconfigure(i, weight=1)
        
        # Parameters for changing the space reclaiming part in the parameter frame
        # gap size label
        gap_size_label = Label(parameter_frame, text="Gap size", bg = self.bg_color, 
            fg = "white", justify=LEFT, anchor="w")
        gap_size_label.grid(row=0, column=0, sticky = "w", padx=(10,10))

        self.gap_size_entry = Entry(parameter_frame, bg = self.second_color, width = 6, 
            fg = "white", highlightcolor = "white")
        self.gap_size_entry.grid(row=0, column=1, sticky = "e")
        self.gap_size_entry.insert(10, "5")

        shrinking_factor_label = Label(parameter_frame, text="Shrinking factor", bg = self.bg_color, 
            fg = "white", justify=LEFT, anchor="w")
        shrinking_factor_label.grid(row=1, column=0, sticky = "w", padx=(10,10))

        self.shrinking_factor_entry = Entry(parameter_frame, bg = self.second_color, width = 6, 
            fg = "white", highlightcolor = "white")
        self.shrinking_factor_entry.grid(row=1, column=1, sticky = "e")
        self.shrinking_factor_entry.insert(10, "0.8")

        max_span_label = Label(parameter_frame, text="Max factor", bg = self.bg_color, 
            fg = "white", justify=LEFT, anchor="w")
        max_span_label.grid(row=2, column=0, sticky = "w", padx=(10,10))

        self.max_span_entry = Entry(parameter_frame, bg = self.second_color, width = 6, 
            fg = "white", highlightcolor = "white")
        self.max_span_entry.grid(row=2, column=1, sticky = "e")
        self.max_span_entry.insert(10, "2")

        space_reclaiming_factor_label = Label(parameter_frame, text="Space recl. factor", 
            bg = self.bg_color, fg = "white", justify=LEFT, anchor="w")
        space_reclaiming_factor_label.grid(row=3, column=0, sticky = "w", padx=(10,10))

        self.space_reclaiming_factor_entry = Entry(parameter_frame, bg = self.second_color, 
            width = 6, fg = "white", highlightcolor = "white")
        self.space_reclaiming_factor_entry.grid(row=3, column=1, sticky = "e")
        self.space_reclaiming_factor_entry.insert(10, "1")

        hue_color_label = Label(parameter_frame, text="Hue color", 
            bg = self.bg_color, fg = "white", justify=LEFT, anchor="w")
        hue_color_label.grid(row=4, column=0, sticky = "w", padx=(10,10))

        self.hue_color_entry = Entry(parameter_frame, bg = self.second_color, 
            width = 6, fg = "white", highlightcolor = "white")
        self.hue_color_entry.grid(row=4, column=1, sticky = "e")
        self.hue_color_entry.insert(10, "122")

        apply_button = Button(parameter_frame, text="Apply parameters", bg=self.bg_color, 
            fg="white", activebackground=self.second_color, activeforeground="white",
            command=self.apply_button_function)
        apply_button.grid(row=5, column=0, columnspan = 2, 
            sticky="nsew")

        # The information frame
        information_frame = Frame(left_frame, bg = self.second_color)
        information_frame.grid(row=6, column=0, sticky="nsew", padx=(10,10), pady=(5,5))
        for i in range(3):
            information_frame.rowconfigure(i, weight=1)
        
        # selected node text
        self.selected_label = Label(information_frame, text="[Selected Node]", 
            bg = self.second_color, fg = "white", wraplength= 220, justify=LEFT, anchor="w")
        self.selected_label.grid(row=0, column=0, sticky = "w", padx=(10,10), pady=(5,5))

        # parent label text
        self.parent_label = Label(information_frame, text="[Parent Node]", 
            bg = self.second_color, fg = "white", wraplength= 220, justify=LEFT, anchor="w")
        self.parent_label.grid(row=1, column=0, sticky = "w", padx=(10,10), pady=(5,5))

        # List of children text
        self.children_label = Label(information_frame, text="[List of Children]", 
            bg = self.second_color, fg = "white", wraplength= 220, justify=LEFT, anchor="w")
        self.children_label.grid(row=2, column=0, sticky = "w", padx=(10,10), pady=(5,5))

        # details text (not needed rn)
        # self.detail_label = Label(information_frame, text="[Node details]", 
        #     bg = self.second_color, fg = "white", wraplength= 220, justify=LEFT, anchor="w")
        # self.detail_label.grid(row=3, column=0, sticky = "w", padx=(10,10), pady=(10,10))

        # Run the GUI
        self.root.mainloop()

