
from walkInClinicSystem import MyApp
from DBHelper import *
import tkinter as Tk
if __name__ == "__main__":

    # --------------------------------------------------
    # GUI
    # --------------------------------------------------
    root = Tk.Tk()
    app = MyApp(root)
    root.mainloop()
