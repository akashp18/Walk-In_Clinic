import tkinter as Tk
from tkinter import ttk, messagebox

from matplotlib import pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkcalendar import DateEntry

from DBHelper import getPatientInfo, deletePatient, getStaffInfo, getDoctorInfo, deleteStaff, deleteDoctor, insertUSER, \
    insertDoctor, insertStaff
from data_graphs import graph1, graph2, graph3
from utilities import checkEmailFormat, checkZipCodeLength, checkAlphabeticString, compareIfPasswordMatch, changeRole, \
    gender_v, formatphone


class adminProfile(object):
    # Initialization
    def __init__(self, parent, currentUser):
        """Constructor"""
        self.user = currentUser
        self.root = parent
        self.root.title("Walk-In Clinic Management System ====  Welcome " + self.user[1])
        self.root.geometry("1145x700")
        # self.root.configure(bg='#FBE7C6')
        self.frame = Tk.Frame(parent)
        self.userID = Tk.StringVar()
        self.OptionRole = Tk.StringVar()
        self.__nUFormFontSize = 16
        self.__LoginFontSize = 16
        self.fname = Tk.StringVar()
        self.lname = Tk.StringVar()
        self.genderOption = Tk.StringVar()
        self.phone = Tk.StringVar()
        self.email = Tk.StringVar()
        self.dob = None
        self.healthCard = Tk.StringVar()
        self.street = Tk.StringVar()
        self.city = Tk.StringVar()
        self.zipCode = Tk.StringVar()
        self.province = Tk.StringVar()
        self.nPassword = Tk.StringVar()
        self.OptionSpecial = Tk.StringVar()
        self.confirmPassword = Tk.StringVar()
        self.var = Tk.IntVar()
        self.var2 = Tk.IntVar()
        self.var3 = Tk.IntVar()
        self.adminFrame = None

        self.patient_id = Tk.StringVar()
        self.option1 = None
        self.option2 = None
        self.graphWindow = None

        self.frame.grid()
        self.__profile()

    def __profile(self):
        green = "#d2ffd2"
        red = "#dd0202"
        tab_css = ttk.Style()
        # tab_css.theme_create("MyStyle", parent="alt", settings={
        #     "TNotebook.Tab": {"configure": {"padding": [50, 10],
        #                                     "background": '#BD4B4B', "font": ('URW Gothic L', '16', 'bold')}, }})
        tab_css.theme_create("MyStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [68, 10], "background": green, "font": ('URW Gothic L', '16', 'bold')},
                "map": {"background": [("selected", red)],
                        "expand": [("selected", [1, 1, 1, 0])]}}})
        tab_css.theme_use("MyStyle")
        tabControl = ttk.Notebook(self.root)
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        tab4 = ttk.Frame(tabControl)
        # bg = '#FBE7C6'
        Tk.Label(self.root, text='Welcome to KW - CLINIC', font=("Times New Roman", 25)).grid(row=0, column=0,
                                                                                              columnspan=1)
        logout = Tk.Button(self.root, text="Logout", bg='red', fg="white", font=("Times New Roman", 15), pady=5,
                           command=lambda: self.root.quit())
        logout.config(width=15)
        logout.grid(row=0, column=0, sticky='S', pady=10, padx=(950, 0))
        tabControl.add(tab1, text='Edit Patient')
        tabControl.add(tab2, text='Add Staff')
        tabControl.add(tab3, text='Remove/View Staff')
        tabControl.add(tab4, text='Data Trend Report')
        tabControl.grid()

        # =================================================================================
        # Edit Patients
        # =================================================================================
        common_bg = '#' + ''.join([hex(x)[2:].zfill(2) for x in (181, 26, 18)])  # RGB in dec
        common_fg = '#ffffff'  # pure white

        actionLabel = Tk.Label(tab1, padx=15, pady=15, text="Action:", font=("Times New Roman", 16))
        actionLabel.grid(column=0, row=1, sticky=Tk.W, padx=(100, 0), pady=(100, 0))
        var = Tk.IntVar()
        self.option1 = Tk.Radiobutton(tab1, text="Search Patient", variable=self.var, value=1,
                                      font=("Times New Roman", 16), fg=common_fg, bg=common_bg,
                                      activebackground=common_bg, activeforeground=common_fg, selectcolor=common_bg)
        self.option1.grid(column=1, row=1, sticky=Tk.W, padx=(100, 0), pady=(100, 0))
        #
        self.option2 = Tk.Radiobutton(tab1, text="Remove Patient", variable=self.var, value=2, highlightcolor='green',
                                      font=("Times New Roman", 16), fg=common_fg, bg=common_bg,
                                      activebackground=common_bg, activeforeground=common_fg, selectcolor=common_bg)
        self.option2.grid(column=2, row=1, sticky=Tk.W, padx=(100, 0), pady=(100, 0))

        userIdLabel = Tk.Label(tab1, padx=15, pady=10, text="Patient User ID:  ",
                               font=("Times New Roman", 16))
        userIdLabel.grid(column=0, row=3, sticky=Tk.W, padx=(100, 0), pady=(30, 0))

        userId = Tk.Entry(tab1, relief="solid", textvariable=self.userID,
                          font=("Times New Roman", 16))
        userId.grid(column=1, row=3, sticky=Tk.E, padx=(0, 0), pady=(30, 0))

        change = Tk.Button(tab1, text="Commit", bg='red', fg="white",
                           font=("Times New Roman", 16), command=self.search_patient)
        change.config(width=10)
        change.grid(column=2, row=3, sticky=Tk.E, padx=(0, 0), pady=(30, 0))

        #
        # option3 = Tk.Radiobutton(tab1, text="Edit Patient", variable=var, value=3, highlightcolor = 'green',font=("Times New Roman", 16), fg=common_fg, bg=common_bg,
        #                    activebackground=common_bg, activeforeground=common_fg, selectcolor=common_bg)
        # option3.grid(column=3, row=1, sticky=Tk.W, padx=(100, 0), pady=(100, 0))

        # =================================================================================
        # Edit Staff
        # =================================================================================

        roleLabel = Tk.Label(tab2, text="Add Staff Account",
                             font=("Times New Roman", 20))
        roleLabel.grid(column=0, row=0, sticky=Tk.W, padx=(80, 0), pady=(60,0))



        roleLabel = Tk.Label(tab2, text="Role: ",
                             font=("Times New Roman", self.__LoginFontSize))
        roleLabel.grid(column=0, row=2, sticky=Tk.E, padx=(5, 0), pady=(30, 5))

        options = ['ADMIN', 'DOCTOR', 'NURSE']
        role = Tk.OptionMenu(tab2, self.OptionRole, *options)
        role.config(width=16, font=('Times New Roman', 16), bg='light blue')
        role.grid(column=1, row=2, sticky=Tk.E, padx=(5, 0), pady=(30, 5))

        # --------------------------------------------------------------------------------
        # Full Name
        # --------------------------------------------------------------------------------
        firstNameLabel = Tk.Label(tab2, text="First Name: ",
                                  font=("Times New Roman", self.__nUFormFontSize))
        firstNameLabel.grid(column=0, row=3, sticky=Tk.E, padx=5, pady=5)

        firstName = Tk.Entry(tab2, relief="solid", textvariable=self.fname, width=20, bd=1,
                             font=("Times New Roman", self.__nUFormFontSize))
        firstName.grid(column=1, row=3, sticky=Tk.E, padx=5, pady=5)

        lastNameLabel = Tk.Label(tab2, text="Last Name: ",
                                 font=("Times New Roman", self.__nUFormFontSize))
        lastNameLabel.grid(column=2, row=3, sticky=Tk.E, padx=(20, 0), pady=5)
        lastName = Tk.Entry(tab2, relief="solid", textvariable=self.lname, width=20, bd=1,
                            font=("Times New Roman", self.__nUFormFontSize))
        lastName.grid(column=3, row=3, sticky=Tk.E, padx=5, pady=5)
        # --------------------------------------------------------------------------------
        # Gender
        # --------------------------------------------------------------------------------
        genderLabel = Tk.Label(tab2, text="Gender: ",
                               font=("Times New Roman", self.__nUFormFontSize))
        genderLabel.grid(column=0, row=4, sticky=Tk.E, padx=5, pady=5)
        options = ['Female', 'Male', 'Other']
        gender = Tk.OptionMenu(tab2, self.genderOption, *options)
        gender.config(width=12, font=('Times New Roman', self.__nUFormFontSize), bg='light blue')
        gender.grid(column=1, row=4, sticky=Tk.E, padx=5, pady=5)
        # --------------------------------------------------------------------------------
        # Date Of Birth
        # --------------------------------------------------------------------------------
        dobLabel = Tk.Label(tab2, text="Date of Birth: ",
                            font=("Times New Roman", self.__nUFormFontSize))
        dobLabel.grid(column=2, row=4, sticky=Tk.E, padx=(5, 0), pady=5)
        self.dob = DateEntry(tab2, padx=10, pady=20, width=18, year=2021, month=6, day=22,
                             background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                             font=("Times New Roman", self.__nUFormFontSize))
        self.dob.grid(column=3, row=4, sticky=Tk.E, padx=5, pady=5)

        # --------------------------------------------------------------------------------
        # Phone
        # --------------------------------------------------------------------------------
        phoneLabel = Tk.Label(tab2, text="Phone: ",
                              font=("Times New Roman", self.__nUFormFontSize))
        phoneLabel.grid(column=0, row=5, sticky=Tk.E, padx=5, pady=5)
        phoneNumber = Tk.Entry(tab2, relief="solid", textvariable=self.phone, width=20, bd=1,
                               font=("Times New Roman", self.__nUFormFontSize))
        phoneNumber.grid(column=1, row=5, sticky=Tk.E)

        # --------------------------------------------------------------------------------
        # Email
        # --------------------------------------------------------------------------------
        emailLabel = Tk.Label(tab2, text="Email: ",
                              font=("Times New Roman", self.__nUFormFontSize))
        emailLabel.grid(column=2, row=5, sticky=Tk.E, padx=5, pady=5)
        emailNumber = Tk.Entry(tab2, relief="solid", textvariable=self.email, width=20, bd=1,
                               font=("Times New Roman", self.__nUFormFontSize))
        emailNumber.grid(column=3, row=5, sticky=Tk.E)

        # --------------------------------------------------------------------------------
        # Password
        # --------------------------------------------------------------------------------
        spLabel = Tk.Label(tab2, text="Speciality: ",
                           font=("Times New Roman", self.__nUFormFontSize))
        spLabel.grid(column=0, row=6, sticky=Tk.E, padx=5, pady=5)
        sp = Tk.Entry(tab2, relief="solid", textvariable=self.OptionSpecial, width=20, bd=1,
                      font=("Times New Roman", self.__nUFormFontSize))
        sp.grid(column=1, row=6, sticky=Tk.E)
        # --------------------------------------------------------------------------------
        # Address Info
        # --------------------------------------------------------------------------------
        SAddLabel = Tk.Label(tab2, text="Street Address: ",
                             font=("Times New Roman", self.__nUFormFontSize))
        SAddLabel.grid(column=0, row=7, sticky=Tk.E, padx=5, pady=5)
        StreetAdd = Tk.Entry(tab2, relief="solid", textvariable=self.street, width=20, bd=1,
                             font=("Times New Roman", self.__nUFormFontSize))
        StreetAdd.grid(column=1, row=7, sticky=Tk.E)

        cityLabel = Tk.Label(tab2, text="City: ",
                             font=("Times New Roman", self.__nUFormFontSize))
        cityLabel.grid(column=2, row=7, sticky=Tk.E, padx=5, pady=5)
        city = Tk.Entry(tab2, relief="solid", textvariable=self.city, width=20, bd=1,
                        font=("Times New Roman", self.__nUFormFontSize))
        city.grid(column=3, row=7, sticky=Tk.E)

        zipCodeLabel = Tk.Label(tab2, text="Zip Code: ",
                                font=("Times New Roman", self.__nUFormFontSize))
        zipCodeLabel.grid(column=0, row=8, sticky=Tk.E, padx=5, pady=5)
        zipCode = Tk.Entry(tab2, relief="solid", textvariable=self.zipCode, width=8, bd=1,
                           font=("Times New Roman", self.__nUFormFontSize))
        zipCode.grid(column=1, row=8, sticky=Tk.E)

        provinceLabel = Tk.Label(tab2, text="Province: ",
                                 font=("Times New Roman", self.__nUFormFontSize))
        provinceLabel.grid(column=2, row=8, sticky=Tk.E, padx=(120, 0), pady=5)
        province = Tk.Entry(tab2, relief="solid", textvariable=self.province, width=20, bd=1,
                            font=("Times New Roman", self.__nUFormFontSize))
        province.grid(column=3, row=8, sticky=Tk.E)

        # --------------------------------------------------------------------------------
        # Password
        # --------------------------------------------------------------------------------
        passLabel = Tk.Label(tab2, text="Password: ",
                             font=("Times New Roman", self.__nUFormFontSize))
        passLabel.grid(column=0, row=9, sticky=Tk.E, padx=5, pady=5)
        newPassword = Tk.Entry(tab2, relief="solid", textvariable=self.nPassword, width=20, bd=1,
                               font=("Times New Roman", self.__nUFormFontSize))
        newPassword.grid(column=1, row=9, sticky=Tk.E)

        cpassLabel = Tk.Label(tab2, text="Confirm Password: ",
                              font=("Times New Roman", self.__nUFormFontSize))
        cpassLabel.grid(column=2, row=9, sticky=Tk.E, padx=5, pady=5)
        cPassword = Tk.Entry(tab2, relief="solid", textvariable=self.confirmPassword, width=20, bd=1,
                             font=("Times New Roman", self.__nUFormFontSize))
        cPassword.grid(column=3, row=9, sticky=Tk.E)

        change = Tk.Button(tab2, text="ADD", bg='red', fg="white",
                           font=("Times New Roman", 16), command=self.addUser)
        change.config(width=10)
        change.grid(column=3, row=10, sticky=Tk.E, padx=(0, 0), pady=(50, 20))
        # =================================================================================
        # Edit Staff
        # =================================================================================

        common_bg = '#' + ''.join([hex(x)[2:].zfill(2) for x in (181, 26, 18)])  # RGB in dec
        common_fg = '#ffffff'  # pure white

        actionLabel = Tk.Label(tab3, padx=15, pady=15, text="Action:", font=("Times New Roman", 16))
        actionLabel.grid(column=0, row=1, sticky=Tk.W, padx=(100, 0), pady=(100, 0))

        option1 = Tk.Radiobutton(tab3, text="Search Staff", variable=self.var2, value=1, font=("Times New Roman", 16),
                                 fg=common_fg, bg=common_bg,
                                 activebackground=common_bg, activeforeground=common_fg, selectcolor=common_bg)
        option1.grid(column=1, row=1, sticky=Tk.W, padx=(100, 0), pady=(100, 0))
        #
        option2 = Tk.Radiobutton(tab3, text="Remove Staff", variable=self.var2, value=2, highlightcolor='green',
                                 font=("Times New Roman", 16), fg=common_fg, bg=common_bg,
                                 activebackground=common_bg, activeforeground=common_fg, selectcolor=common_bg)
        option2.grid(column=2, row=1, sticky=Tk.W, padx=(100, 0), pady=(100, 0))

        userIdLabel = Tk.Label(tab3, padx=14, pady=10, text="Staff User ID: ",
                               font=("Times New Roman", 16))
        userIdLabel.grid(column=0, row=3, sticky=Tk.W, padx=(100, 0), pady=(30, 0))

        userId = Tk.Entry(tab3, relief="solid", textvariable=self.userID,
                          font=("Times New Roman", 16))
        userId.grid(column=1, row=3, sticky=Tk.E, padx=(20, 0), pady=(30, 0))

        change = Tk.Button(tab3, text="Commit", bg='red', fg="white",
                           font=("Times New Roman", 16), command=self.search_staff)
        change.config(width=10)
        change.grid(column=2, row=3, sticky=Tk.E, padx=(0, 0), pady=(30, 0))
        # =================================================================================
        # Data Trend Report
        # =================================================================================
        common_bg = '#252627' # RGB in dec
        common_fg = '#F2EFE9'  # pure white

        actionLabel = Tk.Label(tab4, padx=15, pady=15, text="Select Data Analysis:", font=("Times New Roman", 22))
        actionLabel.grid(column=0, row=0, sticky=Tk.W, padx=(100, 0), pady=(100, 0))

        self.option1 = Tk.Radiobutton(tab4, text="Appointments by Appointment Type Data", variable=self.var3, value=1,
                                      font=("Times New Roman", 20))
        self.option1.grid(column=0, row=1, sticky=Tk.W, padx=(300, 0), pady=(50, 0))
        #
        self.option2 = Tk.Radiobutton(tab4, text="Revenue Per Year Data", variable=self.var3, value=2, highlightcolor='green',
                                      font=("Times New Roman", 20))
        self.option2.grid(column=0, row=2, sticky=Tk.W, padx=(300, 0), pady=(50, 0))

        self.option3 = Tk.Radiobutton(tab4, text="Appointments By Year Data", variable=self.var3, value=3, highlightcolor='green',
                                      font=("Times New Roman", 20))
        self.option3.grid(column=0, row=3, sticky=Tk.W, padx=(300, 0), pady=(50, 0))



        change = Tk.Button(tab4, text="Create", bg='red', fg="white",
                           font=("Times New Roman", 16), command=self.graph_data)
        change.config(width=10)
        change.grid(column=0, row=4, sticky=Tk.E, padx=(0, 0), pady=(30, 0))


    def search_patient(self):

        search_list = ["Email:  ", "Firstname:  ", "Lastname:  ", "Birthday:  ", "HealthCard No:  ", "Gender:  ",
                       "Phone number:  ", "Street Name: ",
                       'City:  ', 'Province:  ', 'ZipCode:  ', 'User_ID:  ']

        user_id = self.userID.get()
        option = self.var.get()

        if option == 0:
            error = "Options are not selected"
            messagebox.showinfo("Error", error)
        elif option == 1:

            user_info = getPatientInfo(user_id)
            if user_info:
                self.adminFrame = Tk.Toplevel()
                for i in range(0, len(user_info[0])):
                    spLabel = Tk.Label(self.adminFrame, text=search_list[i],
                                       font=("Times New Roman", self.__nUFormFontSize))
                    spLabel.grid(column=0, row=i, sticky=Tk.E, padx=5, pady=5)
                    spLabel = Tk.Label(self.adminFrame, text=user_info[0][i],
                                       font=("Times New Roman", self.__nUFormFontSize))
                    spLabel.grid(column=1, row=i, sticky=Tk.E, padx=5, pady=5)

            if not user_info:
                error = "User Not Found"
                messagebox.showinfo("Error", error)

        elif option == 2:
            deletePatient(user_id)
            error = "User is Deleted"
            messagebox.showinfo("Success", error)

    def search_staff(self):

        search_list_0 = ["Doctor_ID:  ", "Firstname:  ", "Lastname:  ", "Birthday:  ", "Gender:  ", "Email:  ",
                         "Phone number:  ", "Street Name: ",
                         'City:  ', 'Province:  ', 'ZipCode:  ', 'Speciality:  ']
        search_list_1 = ["Firstname:  ", "Lastname:  ", "Birthday:  ", "Gender:  ", "Email:  ",
                         "Phone number:  ", "Street Name: ",
                         'City:  ', 'Province:  ', 'ZipCode:  ', 'User_ID:  ']

        user_id = self.userID.get()
        option = self.var2.get()
        isDoctor = 2
        user_info = getStaffInfo(user_id)
        if not user_info:
            user_info = getDoctorInfo(user_id)
            if user_info:
                isDoctor = 1
            else:
                isDoctor = 2
        elif user_info:
                isDoctor = 0
        if option == 0:
            error = "Options are not selected"
            messagebox.showinfo("Error", error)
        elif option == 1:

            if user_info:
                self.adminFrame = Tk.Toplevel()
                if isDoctor == 1:
                    search_list = search_list_0
                else:
                    search_list = search_list_1
                print(user_info[0])
                print(search_list)
                for i in range(0, len(user_info[0])):
                    spLabel = Tk.Label(self.adminFrame, text=search_list[i],
                                       font=("Times New Roman", self.__nUFormFontSize))
                    spLabel.grid(column=0, row=i, sticky=Tk.E, padx=5, pady=5)
                    spLabel = Tk.Label(self.adminFrame, text=user_info[0][i],
                                       font=("Times New Roman", self.__nUFormFontSize))
                    spLabel.grid(column=1, row=i, sticky=Tk.E, padx=5, pady=5)

            if not user_info:
                error = "User Not Found"
                messagebox.showinfo("Error", error)

        elif option == 2 and user_id != 1000:
            if isDoctor == 1:
                deleteDoctor(user_id)
                error = "Doctor account is Deleted"
                messagebox.showinfo("Success", error)
            elif isDoctor == 0:
                deleteStaff(user_id)
                error = "Staff account is Deleted"
                messagebox.showinfo("Success", error)
            else:
                error = "Invalid Staff ID"
                messagebox.showinfo("Error", error)
        else:
            error = "Invalid Staff ID"
            messagebox.showinfo("Error", error)

    def addUser(self):
        error =''
        fname =self.fname.get()
        lname= self.lname.get()
        role = self.OptionRole.get()
        gender = self.genderOption.get()
        dob = self.dob.get()
        phone = self.phone.get()
        email = self.email.get()
        special = self.OptionSpecial.get()
        street = self.street.get()
        city = self.city.get()
        zipcode = self.zipCode.get()
        province = self.province.get()
        npass = self.nPassword.get()
        cpass = self.confirmPassword.get()
        check_email = checkEmailFormat(email)
        check_zipcode = checkZipCodeLength(zipcode.strip())
        check_firstname = checkAlphabeticString(fname)
        check_lastname = checkAlphabeticString(lname)
        check_password = compareIfPasswordMatch(npass, cpass)
        if check_password and check_email and check_zipcode and check_firstname and check_lastname:
            change_role = changeRole(role)
            id = insertUSER(change_role, email, npass,'Active')
            gn = gender_v(gender)
            phone = formatphone(phone)
            if change_role == 3:
                insertDoctor(id, fname, lname, dob, gn, email, phone, street, city, province, zipcode, special)
            elif change_role == 2:
                insertStaff(id, fname, lname, dob, gn, email, phone, street, city, province, zipcode)
            messagebox.showinfo("Success", "Account id: {} created Successfully ".format(id))
        else:
            if not check_firstname:
                error = error + "First name contain invalid characters\n"
            if not check_lastname:
                error = error + "Last name contain invalid characters\n"
            if not check_zipcode:
                error = error + "Invalid ZipCode\n"
            if not check_email:
                error = error + "Invalid Email address\n"

            if not check_password:
                error = error + "Password and Confirm password does not matches\n"
            messagebox.showinfo("Error", error)

    def graph_1(self):
        Year, Total = graph1()
        w = 0.5
        window = Tk.Toplevel()
        fig = Figure(figsize=(7, 7),
                     dpi=100)
        plot1 = fig.add_subplot(111)
        plot1.bar(Year, Total, w, label="Appointment by year", color=['black', 'red', 'green', 'blue', 'cyan'])
        plot1.set_xlabel("Year")
        plot1.set_ylabel("Number of Appointments")
        plot1.set_title("Appointments by year")
        plot1.set_xticks(Year)
        canvas = FigureCanvasTkAgg(fig,
                                   master=window)
        canvas.draw()
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                       window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
    def graph_2(self):
        Year, Amount = graph2()
        w = 0.5
        window = Tk.Toplevel()
        fig = Figure(figsize=(7, 7),
                     dpi=100)
        plot1 = fig.add_subplot(111)
        plot1.bar(Year, Amount, w, label="Revenue per Year", color=['blue', 'cyan','black', 'red', 'green'])
        plot1.set_xlabel("Year")
        plot1.set_ylabel("Revenue(in $)")
        plot1.set_title("Revenue per year")
        plot1.set_xticks(Year)
        canvas = FigureCanvasTkAgg(fig,
                                   master=window)
        canvas.draw()
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                       window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()

    def graph_3(self):
        type_, count = graph3()
        window = Tk.Toplevel()
        fig = Figure(figsize=(7, 7),
                     dpi=100)
        plot1 = fig.add_subplot(111)
        plot1.pie(count, labels=type_, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})
        plot1.set_ylabel("Revenue(in $)")
        plot1.set_title("Appointments by appointment_type(Till now)")
        canvas = FigureCanvasTkAgg(fig,
                                   master=window)
        canvas.draw()
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                       window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()


    def graph_data(self):
        graph = self.var3.get()
        if graph == 1:
            self.graph_1()
        elif graph ==2:
            self.graph_2()
        elif graph == 3:
            self.graph_3()