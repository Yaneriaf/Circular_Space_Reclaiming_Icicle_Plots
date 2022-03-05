from tkinter import *
from tkinter import filedialog
from input_reader import InputReader

# This function facilitates the selection of the input file and the creation of the input 
# reader object for it
def import_button_function(self):
    path = filedialog.askopenfile(initialdir="/", title="Select file").name
    self.input_reader = InputReader(path[:len(path)-5])
    self.file_label.config(text = path[:len(path)-5])

def change_vis_button_function(self):
    if self.input_reader != None:
        print(self.input_reader.trees[0].ascii_art())
    else:
        print("no file selected yet")

def export_button_function(self):
    print(self.import_button.winfo_width())

class GUI:

    def __init__(self):
        # The path of the input file
        self.input_reader = None

        # Colors used
        self.bg_color = "#1A2227"
        self.second_color = "#22323C"

    def run_gui(self):
        
        # The root frame
        self.root = Tk()
        self.root.geometry("700x700")
        self.root.configure(background=self.bg_color)
        self.root.title("Circular Space Reclaiming Plots Visualizer")

        # This is where the plot will be 
        plot_frame = Frame(self.root, bg="pink")
        plot_frame.pack(side=RIGHT, fill=BOTH, expand=TRUE)

        # This is the frame for the rest (with grid layout)
        left_frame = Frame(self.root, bg = self.bg_color)
        left_frame.place(relheight=1, width = 250)
        # The grid layout
        for i in range(6):
            left_frame.rowconfigure(i, weight=1)
        left_frame.columnconfigure(0, weight=1)

        # The button/filethingy used for importing
        import_button = Button(left_frame, text="Import", bg=self.bg_color, fg="white", 
            activebackground=self.second_color, activeforeground="white", 
            command=lambda:import_button_function(self))
        import_button.grid(row=0, column=0, sticky="nsew", padx=(10,10), pady=(10,0))

        self.file_label = Label(left_frame, text="No file selected yet", 
            bg = self.bg_color, fg = "white", wraplength= 230)
        self.file_label.grid(row=1, column=0, sticky = "w", padx=(10,0), pady=(0,10))

        # The change vis button
        change_button = Button(left_frame, text="Change visualization", bg=self.bg_color, 
            fg="white", activebackground=self.second_color, activeforeground="white", 
            command=lambda:change_vis_button_function(self))
        change_button.grid(row=2, column=0, sticky="nsew", padx=(10,10), pady=(10,10))

        # The export button
        export_button = Button(left_frame, text="Export", bg=self.bg_color, fg="white", 
            activebackground=self.second_color, activeforeground="white",
            command=lambda:export_button_function(self))
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
        self.root.mainloop()

