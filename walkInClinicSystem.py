import tkinter as Tk  # python 3
import tkinter as tk
from tkinter import font as tkfont, messagebox  # python 3
from signup_page import newUser
from patientProfile_page import patientProfile
from doctorProfile_page import doctorProfile
from login_page import login


class MyApp(Tk.Frame):
    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        login(parent)