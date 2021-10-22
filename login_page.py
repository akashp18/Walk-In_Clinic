import tkinter as Tk  # python 3
import tkinter as tk
from tkinter import font as tkfont, messagebox  # python 3
from signup_page import newUser
from patientProfile_page import patientProfile
from doctorProfile_page import doctorProfile
from nurseProfile_page import nurseProfile
from adminProfile_page import adminProfile
from utilities import getValid_Staff, getValid_patient
from utilities import changeRole


class login(Tk.Frame):
    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.root = parent
        self.root.title("*** Walk-In Clinic Management System ***")
        self.root.geometry("650x700")
        self.root.resizable(0, 0)
        self.__welcome()
        # -------- Variables -----------
        self.__LoginFontSize = 18
        self.patientEmail = Tk.StringVar()
        self.patientPassword = Tk.StringVar()
        self.OptionRole = Tk.StringVar()
        self.staffEmail = Tk.StringVar()
        self.staffPassword = Tk.StringVar()
        self.patientLogin = None
        # -------- Labels -----------

        self.emailLabel = None
        self.roleLabel = None
        self.passwordLabel = None
        self.loginLabel = None
        self.passLabel = None
        # ----------Text---------------
        self.email = None
        self.role = None
        self.password = None
        self.patientEmail = None
        self.patientPass = None
        # -------- Buttons -----------
        self.submit = None
        self.login = None

        # --------------------------------------------------------------------------------
        # Welcome Screen
        # --------------------------------------------------------------------------------

    def __welcome(self):
        # Welcome Screen Layout
        patient = Tk.Button(self.root, bg='green', fg="white", text="Patient", font=("Times New Roman", 20),
                            command=lambda: [self.__PatientLogin()])
        patient.config(width=20)
        patient.grid(column=0, row=0, sticky=Tk.W, padx=(0, 0))
        staff = Tk.Button(self.root, text="Staff", bg='black', fg="white", font=("Times New Roman", 20),
                          command=lambda: [self.__StaffSignIn()])
        staff.config(width=22)
        staff.grid(column=1, row=0, sticky=Tk.W, padx=0)
        self.title = Tk.Label(self.root, padx=15, pady=5, text="Welcome to KW-CLINIC",
                              font=("Times New Roman", 30))
        self.title.grid(column=0, row=1, sticky=Tk.W, padx=(110, 0), pady=(250, 0), columnspan=2)

        # --------------------------------------------------------------------------------
        # Staff SignIn Screen
        # --------------------------------------------------------------------------------

    def __StaffSignIn(self):
        if self.title is not None:
            self.title.grid_remove()
            self.title = None
        if self.loginLabel is not None:
            self.__clear_Patient_Login()
        if self.emailLabel is not None:
            self.__clear_Staff_Login()

        options = ['ADMIN', 'DOCTOR', 'NURSE']
        self.emailLabel = Tk.Label(self.root, padx=15, pady=5, text="Login: ",
                                   font=("Times New Roman", self.__LoginFontSize))
        self.emailLabel.grid(column=0, row=1, sticky=Tk.W, padx=(100, 0), pady=(100, 0))

        self.email = Tk.Entry(self.root, relief="solid", textvariable=self.staffEmail, font=("Times New Roman", 20))
        self.email.grid(column=1, row=1, sticky=Tk.E, padx=(0, 160), pady=(100, 0))

        self.roleLabel = Tk.Label(self.root, padx=15, pady=10, text="Role: ",
                                  font=("Times New Roman", self.__LoginFontSize))
        self.roleLabel.grid(column=0, row=2, sticky=Tk.W, padx=(100, 0), pady=5)

        self.role = Tk.OptionMenu(self.root, self.OptionRole, *options)
        self.role.config(width=16, font=('Times New Roman', self.__LoginFontSize), bg='light blue')
        self.role.grid(column=1, row=2, sticky=Tk.E, padx=(0, 160), pady=5)

        self.passwordLabel = Tk.Label(self.root, padx=15, pady=10, text="Password: ",
                                      font=("Times New Roman", self.__LoginFontSize))
        self.passwordLabel.grid(column=0, row=3, sticky=Tk.W, padx=(100, 0), pady=5)

        self.password = Tk.Entry(self.root, relief="solid", textvariable=self.staffPassword,
                                 font=("Times New Roman", self.__LoginFontSize),show ="*")
        self.password.grid(column=1, row=3, sticky=Tk.E, padx=(0, 160), pady=5)

        self.submit = Tk.Button(self.root, text="Login", bg='red', fg="white",
                                font=("Times New Roman", self.__LoginFontSize), command=self.__staffCheck)
        self.submit.config(width=10)
        self.submit.grid(column=1, row=4, sticky=Tk.E, padx=(0, 160), pady=(100, 0))

        # --------------------------------------------------------------------------------
        # Patient SignIn Screen
        # --------------------------------------------------------------------------------

    def __PatientLogin(self):
        if self.title is not None:
            self.title.grid_remove()
            self.title = None
        if self.loginLabel is not None:
            self.__clear_Patient_Login()
        if self.emailLabel is not None:
            self.__clear_Staff_Login()

        self.loginLabel = Tk.Label(self.root, padx=15, pady=15, text="Login: ",
                                   font=("Times New Roman", self.__LoginFontSize))
        self.loginLabel.grid(column=0, row=1, sticky=Tk.W, padx=(100, 0), pady=(100, 0))

        self.patientEmail = Tk.Entry(self.root, relief="solid", textvariable=self.patientEmail, width=25, bd=1,
                                     font=("Times New Roman", self.__LoginFontSize))
        self.patientEmail.grid(column=1, row=1, sticky=Tk.E, padx=(0, 180), pady=(100, 0))

        self.passLabel = Tk.Label(self.root, padx=15, text="Password: ",
                                  font=("Times New Roman", self.__LoginFontSize))
        self.passLabel.grid(column=0, row=2, sticky=Tk.W, padx=(100, 0), pady=5)

        self.patientPass = Tk.Entry(self.root, relief="solid", textvariable=self.patientPassword, width=25, bd=1,
                                    font=("Times New Roman", self.__LoginFontSize), show ="*")
        self.patientPass.grid(column=1, row=2, sticky=Tk.E, padx=(0, 180), pady=(25, 0))

        self.newUser = Tk.Button(self.root, text="New User?", bg='green', fg="white",
                                 font=("Times New Roman", self.__LoginFontSize), command=lambda: newUser(self))
        self.newUser.config(width=10)
        self.newUser.grid(column=1, row=3, sticky=Tk.W, padx=5, pady=(100, 0))

        self.login = Tk.Button(self.root, text="Login", bg='red', fg="white",
                               font=("Times New Roman", self.__LoginFontSize), command=self.__patientCheck)
        self.login.config(width=10)
        self.login.grid(column=1, row=3, sticky=Tk.E, padx=(0, 180), pady=(100, 0))

        # --------------------------------------------------------------------------------
        # Patient Profile Check
        # --------------------------------------------------------------------------------

    def __patientCheck(self):
        patientLogin = self.patientEmail.get()
        p_pass = self.patientPassword.get()
        valid_user, user_cred = getValid_patient(patientLogin, p_pass)
        print(user_cred)
        if valid_user:
            self.secondFrame = Tk.Toplevel()
            patientProfile(self.secondFrame, user_cred)

        else:
            error = "Invalid Login or/and Password"
            messagebox.showinfo("Error", error)

        # --------------------------------------------------------------------------------
        # Staff Profile Check
        # --------------------------------------------------------------------------------

    def __staffCheck(self):
        login = self.staffEmail.get()
        role = self.OptionRole.get()
        p_pass = self.staffPassword.get()
        if role == '' or login == '' or p_pass == '':
            error = "Please fill all the fields to login"
            messagebox.showinfo("Error", error)
        else:
            role_access = changeRole(role)
            check_staff, staff_info = getValid_Staff(login, p_pass, role_access)
            print(staff_info)
            if check_staff:
                self.secondFrame = Tk.Toplevel()
                if staff_info[0] == 2:
                    nurseProfile(self.secondFrame, staff_info)
                elif staff_info[0] == 3:
                    doctorProfile(self.secondFrame, staff_info)
                elif staff_info[0] == 4:
                    adminProfile(self.secondFrame, staff_info)
            else:
                error = "Invalid Login Credentials or Role or Password"
                messagebox.showinfo("Error", error)

        # --------------------------------------------------------------------------------
        # Clear Patient Screen
        # --------------------------------------------------------------------------------

    def __clear_Patient_Login(self):
        self.loginLabel.grid_remove()
        self.passLabel.grid_remove()
        self.patientEmail.grid_remove()
        self.patientPass.grid_remove()
        self.newUser.grid_remove()
        self.login.grid_remove()

        # --------------------------------------------------------------------------------
        # Clear Staff Screen
        # --------------------------------------------------------------------------------

    def __clear_Staff_Login(self):
        self.emailLabel.grid_remove()
        self.email.grid_remove()
        self.roleLabel.grid_remove()
        self.role.grid_remove()
        self.passwordLabel.grid_remove()
        self.password.grid_remove()
        self.submit.grid_remove()

        # --------------------------------------------------------------------------------
        # Secondary frames are closed
        # --------------------------------------------------------------------------------

    def __onCloseOtherFrame(self, otherFrame):
        otherFrame.destroy()
        self.__show()

    def hide(self):
        self.root.withdraw()

    def __show(self):
        self.topLevel.update()
        self.topLevel.deiconify()
