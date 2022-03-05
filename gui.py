from tkinter import *
from tkinter import filedialog
from input_reader import InputReader

def import_button_function(self):
    path = filedialog.askopenfile(initialdir="/", title="Select file").name
    print(path[:len(path)-5])
    self.input_reader = InputReader(path)

def change_vis_button_function():
    print("changed")

class GUI:

    def __init__(self):
        # The path of the input file
        self.input_reader = None

        # Colors used
        self.bg_color = "#1A2227"
        self.second_color = "#22323C"

    def run_gui(self):
        
        
        # The root frame
        root = Tk()
        root.geometry("700x700")
        root.configure(background=self.bg_color)
        root.title("Circular Space Reclaiming Plots Visualizer")

        # The grid layout
        for i in range(5):
            root.rowconfigure(i, weight=1)
        for i in range(4):
            root.columnconfigure(i, weight=1)

        # This is where the plot will be 
        plot_frame = Frame(root, bg="pink")
        plot_frame.grid(row=0, column=1, columnspan=3, rowspan=5, sticky="nsew", 
            padx=(10,10), pady=(10,10))

        # The button/filethingy used for importing
        import_button = Button(root, text="Import", bg=self.bg_color, fg="white", 
            activebackground=self.second_color, activeforeground="white", 
            command=lambda: import_button_function(self))
        import_button.grid(row=0, column=0, sticky="nsew", padx=(10,10), pady=(10,10))

        # The change vis button
        change_button = Button(root, text="Change visualization", bg=self.bg_color, 
            fg="white", activebackground=self.second_color, activeforeground="white", 
            command=change_vis_button_function)
        change_button.grid(row=1, column=0, sticky="nsew", padx=(10,10), pady=(10,10))

        # The export button
        export_button = Button(root, text="Export", bg=self.bg_color, fg="white", 
            activebackground=self.second_color, activeforeground="white")
        export_button.grid(row=2, column=0, sticky="nsew", padx=(10,10), pady=(10,10))

        # The animation speed slider (ugly)
        animation_speed = Scale(root, from_=0, to=100, orient=HORIZONTAL, bg=self.bg_color, 
            fg="white", label="Animation Speed", showvalue=0, troughcolor=self.second_color, 
            highlightcolor=self.second_color, bd=1, highlightthickness=0, 
            activebackground=self.second_color)
        animation_speed.grid(row=3, column=0, sticky="ew", padx=(10,10), pady=(10,10))

        # The information frame
        information_frame = Frame(root, bg = self.second_color)
        information_frame.grid(row=4, column=0, sticky="nsew", padx=(10,10), pady=(10,10))
        for i in range(4):
            information_frame.rowconfigure(i, weight=1)
        
        # selected node text
        selected_label = Label(information_frame, text="[Selected Node]", 
            bg = self.second_color, fg = "white")
        selected_label.grid(row=0, column=0, sticky = "w", padx=(10,10), pady=(10,10))

        # parent label text
        parent_label = Label(information_frame, text="[Parent Node]", 
            bg = self.second_color, fg = "white")
        parent_label.grid(row=1, column=0, sticky = "w", padx=(10,10), pady=(10,10))

        # List of children text
        children_label = Label(information_frame, text="[List of Children]", 
            bg = self.second_color, fg = "white")
        children_label.grid(row=2, column=0, sticky = "w", padx=(10,10), pady=(10,10))

        # details text
        detail_label = Label(information_frame, text="[Node details]", 
            bg = self.second_color, fg = "white")
        detail_label.grid(row=3, column=0, sticky = "w", padx=(10,10), pady=(10,10))

        # Run the GUI
        root.mainloop()

