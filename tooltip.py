import tkinter as tk
import tkinter.ttk as ttk

# This class is only used for the tooltip
'''
    This class is based on the Tkinter tooltip class and Pmw
    Tkinter tooltip class only works for buttons, and the Pmw module is not supported in the later Python versions.
    Aknowledgements from Alberto Vassena, https://stackoverflow.com/questions/40538204/how-i-can-make-a-tooltip-appear-over-a-canvas-area-bounded-by-a-box
'''
class CanvasTooltip:
    def __init__(self, canvas, object,
                 *,
                 bg='#FFFFEA',
                 pad=(5, 3, 5, 3),
                 text='canvas info',
                 waittime=400,
                 wraplength=250):
        self.waittime = waittime  # in miliseconds, originally 500
        self.wraplength = wraplength  # in pixels, originally 180
        self.canvas = canvas
        self.text = text
        self.canvas.tag_bind(object, "<Enter>", self.onEnter)
        self.canvas.tag_bind(object, "<Leave>", self.onLeave)
        self.canvas.tag_bind(object, "<ButtonPress>", self.onLeave)
        self.bg = bg
        self.pad = pad
        self.id = None
        self.tw = None

    def onEnter(self, event=None):
        self.schedule()

    def onLeave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.canvas.after(self.waittime, self.show)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.canvas.after_cancel(id_)

    def show(self, event=None):
        def tip_pos_calculator(canvas, label,
                               *,
                               tip_delta=(10, 5), pad=(5, 3, 5, 3)):

            c = canvas

            s_width, s_height = c.winfo_screenwidth(), c.winfo_screenheight()

            width, height = (pad[0] + label.winfo_reqwidth() + pad[2],
                             pad[1] + label.winfo_reqheight() + pad[3])

            mouse_x, mouse_y = c.winfo_pointerxy()

            x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
            x2, y2 = x1 + width, y1 + height

            x_delta = x2 - s_width
            if x_delta < 0:
                x_delta = 0
            y_delta = y2 - s_height
            if y_delta < 0:
                y_delta = 0

            offscreen = (x_delta, y_delta) != (0, 0)

            if offscreen:

                if x_delta:
                    x1 = mouse_x - tip_delta[0] - width

                if y_delta:
                    y1 = mouse_y - tip_delta[1] - height

            offscreen_again = y1 < 0  # out on the top

            if offscreen_again:
                # No further checks will be done.
                y1 = 0

            return x1, y1

        bg = self.bg
        pad = self.pad
        canvas = self.canvas

        # creates a toplevel window
        self.tw = tk.Toplevel(canvas.master)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)

        win = tk.Frame(self.tw,
                       background=bg,
                       borderwidth=0)
        label = ttk.Label(win,
                          text=self.text,
                          justify=tk.LEFT,
                          background=bg,
                          relief=tk.SOLID,
                          borderwidth=0,
                          wraplength=self.wraplength)

        label.grid(padx=(pad[0], pad[2]),
                   pady=(pad[1], pad[3]),
                   sticky=tk.NSEW)
        win.grid()

        x, y = tip_pos_calculator(canvas, label)

        self.tw.wm_geometry("+%d+%d" % (x, y))

    def hide(self):
        if self.tw:
            self.tw.destroy()
        self.tw = None