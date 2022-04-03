import tkinter as tk

class Zoom(tk.Frame):
    def __init__(self, root, canvas):
        tk.Frame.__init__(self, root)
        self.canvas = canvas
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,1000,1000))

        # Binds events of the mouse to functions
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.drag_move)
        #linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        #windows scroll
        self.canvas.bind("<MouseWheel>",self.zoomer)

    #move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
    def drag_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    #windows zoom
    def zoomer(self,event):
        true_x = self.canvas.canvasx(event.x)
        true_y = self.canvas.canvasy(event.y)
        if (event.delta > 0):
            self.canvas.scale("all", true_x, true_y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", true_x, true_y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    #linux zoom
    def zoomerP(self,event):
        true_x = self.canvas.canvasx(event.x)
        true_y = self.canvas.canvasy(event.y)
        self.canvas.scale("all", true_x, true_y, 1.1, 1.1)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    def zoomerM(self,event):
        true_x = self.canvas.canvasx(event.x)
        true_y = self.canvas.canvasy(event.y)
        self.canvas.scale("all", true_x, true_y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))