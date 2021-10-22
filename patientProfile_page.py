import tkinter as Tk
from tkinter import ttk, messagebox

from tkcalendar import DateEntry

from DBHelper import create_appointment, appointment_listByDoctorID, check_appointment, get_billing_info
from utilities import user_appointment


class patientProfile(object):
    # Initialization
    def __init__(self, parent, currentUser):

        """Constructor"""
        self.user = currentUser
        print(currentUser)
        self.root = parent
        self.root.title("Walk-In Clinic Management System ====  Welcome " + self.user[4]+ " "+ self.user[5])
        self.root.geometry("1135x800")
        # self.root.configure(bg='#FBE7C6')
        self.time = Tk.StringVar()
        self.reason = Tk.StringVar()
        self.dn = Tk.StringVar()
        self.frame = Tk.Frame(parent)
        self.date =Tk.StringVar()
        self.fm = Tk.StringVar()
        self.tab2 = None
        self.tab3 = None

        self.frame.grid()
        self.__profile()

    def __profile(self):
        green = "#d2ffd2"
        red = "#dd0202"
        tab_css = ttk.Style()
        # tab_css.theme_create("MyStyle", parent="alt", settings={
        #     "TNotebook.Tab": {"configure": {"padding": [50, 10],
        #                                     "background": '#BD4B4B', "font": ('URW Gothic L', '16', 'bold')}, }})
        tab_css.theme_create("PStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [50, 10], "background": green, "font": ('URW Gothic L', '16', 'bold')},
                "map": {"background": [("selected", red)],
                        "expand": [("selected", [1, 1, 1, 0])]}}})
        tab_css.theme_use("PStyle")
        tabControl = ttk.Notebook(self.root)
        tab1 = ttk.Frame(tabControl)
        self.tab2 = ttk.Frame(tabControl)
        self.tab3 = ttk.Frame(tabControl)

        # bg = '#FBE7C6'
        Tk.Label(self.root, text='Welcome to KW - CLINIC', font=("Times New Roman", 25)).grid(row=0, column=0,
                                                                                             columnspan=1)
        logout = Tk.Button(self.root, text="Logout", bg='red', fg="white", font=("Times New Roman", 15), pady=5,
                           command= lambda : ([self.root.quit()]))
        logout.config(width=15)
        logout.grid(row=0, column=0, sticky='S', pady=10, padx=(950, 0))
        tabControl.add(tab1, text='Book an Appointment')
        tabControl.add(self.tab2, text='Appointment Details')
        tabControl.add(self.tab3, text='Billing History')
        tabControl.grid()

        # =================================================================================
        # BOOK AN APPOINTMENT
        # =================================================================================
        titleLabel = Tk.Label(tab1, padx=15, pady=5, text="Book An Appointment",
                                   font=("Times New Roman",20))
        titleLabel.grid(column=0, row=0, sticky=Tk.W, padx=(100, 0), pady=(100, 50))
        # --------------------------------------------------------------------------------
        # Date
        # --------------------------------------------------------------------------------
        dateLabel = Tk.Label(tab1,  text="Appointment Date : ",
                            font=("Times New Roman", 16))
        dateLabel.grid(column=0, row=1, sticky=Tk.E, padx=(5,0), pady=(5,10))
        self.date = DateEntry(tab1, padx=10, pady=20, width=18, year=2021, month=6, day=22,
                             background='darkblue', foreground='white', borderwidth=2,  date_pattern='yyyy-mm-dd',
                             font=("Times New Roman", 16))
        self.date.grid(column=1, row=1, sticky=Tk.E, padx=5, pady=(5,10))



        fdocLabel = Tk.Label(tab1,  text="Family Doctor : ",
                            font=("Times New Roman", 16))
        fdocLabel.grid(column=2, row=1, sticky=Tk.E, padx=(15,0), pady=(5,10))
        doc = Tk.Entry(tab1, textvariable=self.fm,
                             font=("Times New Roman", 16),width=18, bd=1)
        doc.grid(column=3, row=1, sticky=Tk.E, padx=5, pady=(15,10))

        # --------------------------------------------------------------------------------
        # Time
        # --------------------------------------------------------------------------------


        options = ["9:00 AM","9:30 AM", "10:00 AM","10:30 AM","11:00 AM","11:30 AM","12:00 PM"
                   ,"12:30 PM","1:00 PM","1:30 PM","2:00 PM","2:30 PM","3:00 PM"
                   ,"4:00 PM","4:30 PM","5:00 PM","5:30 PM","6:00 PM","6:30 PM","7:00 PM","7:30 PM","8:00 PM","8:30 PM"
                   ,"9:00 PM","9:30 PM"]
        dateLabel = Tk.Label(tab1,  text="Pick a Time: ",
                                  font=("Times New Roman", 16 ))
        dateLabel.grid(column=0, row=2, sticky=Tk.E, padx=(5,0), pady=(5,10))

        time= Tk.OptionMenu(tab1, self.time, *options)
        time.config(width=16, font=('Times New Roman', 16), bg='light blue')
        time.grid(column=1, row=2, sticky=Tk.E, padx=(5, 5),  pady=(5,10))


        options2 = ['Body Checkup', 'Vaccination','Physical Injury','Minor illness','Diabetes test','cholestero test','Injections']
        rsnLabel = Tk.Label(tab1,  text="Type of Appointment: ",
                                  font=("Times New Roman", 16))
        rsnLabel.grid(column=2, row=2, sticky=Tk.W, padx=(15,0), pady=(5,10))

        rsn = Tk.OptionMenu(tab1, self.reason, *options2)
        rsn.config(width=16, font=('Times New Roman', 16), bg='light blue')
        rsn.grid(column=3, row=2, sticky=Tk.E, padx=(5, 5), pady=(5,10))

        # =================================================================================
        # Symptoms
        # =================================================================================
        dn_L = Tk.Label(tab1, text="Symptoms: ", width=16, font=("Times New Roman", 16))
        dn_L.grid(column=0, row=3, sticky=Tk.E, padx=(5,0), pady=(30,0))
        self.dn = Tk.Text(tab1, height=8, width=55, font=('Arial', 14, 'bold'))
        self.dn.grid(row=3, column=1, sticky='w', padx=(5, 5), pady=(30,0), columnspan=3)

        # =================================================================================
        # Submit
        # =================================================================================
        change = Tk.Button(tab1, text="Submit", bg='red', fg="white",
                           font=("Times New Roman", 16), command = lambda : self.submit_button_response())
        change.config(width=10)
        change.grid(column=3, row=4, sticky=Tk.E, padx=(0, 50), pady=(30, 70))

        # =================================================================================
        # Submission Handle
        # =================================================================================








        # =================================================================================
        # APPOINTMENT Details
        # # =================================================================================
        # titleLabel = Tk.Label(tab2, padx=15, pady=5, text="Appointment Details",
        #                            font=("Times New Roman",20))
        # titleLabel.grid(column=0, row=0, sticky=Tk.W, padx=(100, 0), pady=(100, 50))
        self.tab_2_screen()
        # =================================================================================
        # BILLING HISTORY
        # =================================================================================
        self.tab_3_screen()

    def submit_button_response(self):
        reason = self.reason.get()
        time_slot = self.time.get()
        date_slot = self.date.get()
        dn = self.dn.get("1.0","end-1c")
        fdoc = self.fm.get()

        print(time_slot)
        if reason and time_slot and date_slot:
            test = create_appointment(self.user[14], date_slot, time_slot, reason, dn,
                               fdoc)
            print(test)
            error = "Appointment Request Successfully Submitted"
            messagebox.showinfo("Success", error)
        else:
            error = "Error: missing or empty field"
            messagebox.showinfo("Error", error)


    def tab_2_screen(self):
        master_frame = Tk.Frame(self.tab2)
        master_frame.grid(sticky=Tk.NSEW)
        master_frame.columnconfigure(0, weight=1)
        #
        # # Create a frame for the canvas and scrollbar(s).
        frame2 = Tk.Frame(master_frame)
        frame2.grid(row=3, column=0, sticky=Tk.NW)
        #
        # # Add a canvas in that frame.
        canvas = Tk.Canvas(frame2)
        canvas.grid(row=0, column=0)
        #
        # # Create a vertical scrollbar linked to the canvas.
        vsbar = Tk.Scrollbar(frame2, orient=Tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=Tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)
        #
        # # Create a horizontal scrollbar linked to the canvas.
        hsbar = Tk.Scrollbar(frame2, orient=Tk.HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=1, column=0, sticky=Tk.EW)
        canvas.configure(xscrollcommand=hsbar.set)

        # Create a frame on the canvas to contain the content.
        # content_frame = Tk.Frame(canvas, bg="Red", bd=2)
        content_frame = Tk.Frame(canvas)
        #
        table_title = ["Date", "Time","Reason(s)", "Doctor Name", "Appointment Confirmed"]
        results = check_appointment(self.user[14])
        appointment_list = [lis for lis in results]
        if appointment_list:
            for i in range(0, len(appointment_list)):
                appointment_list[i] = user_appointment(list(appointment_list[i]))
        print(appointment_list)
        Week = appointment_list
        width_tab = [14, 10, 18,16, 24]
        ttk.Label(content_frame, text="Scheduled Appointments", font=('Arial', 20, 'bold'), justify='center').grid(
            column=0, row=0, columnspan=6, pady=10)
        refresh = Tk.Button(content_frame, text="Refresh", width=16,
                            command=lambda: ([master_frame.destroy(), self.tab_2_screen()]))
        refresh.grid(row=0, column=4,sticky='w')
        # # Create a frame on the canvas to contain the buttons.
        #
        for i in range(0, len(table_title)):
            week_0_table = Tk.Label(content_frame, text=table_title[i], width=int(width_tab[i]), fg='blue',
                                    font=('Arial', 14, 'bold'), justify='left')
            week_0_table.grid(row=1, column=i, pady=(10, 0), sticky='w')

        rows = 2
        for i in range(0, len(Week)):
            for j in range(0, len(table_title)):
                week_1_table = Tk.Label(content_frame, text=Week[i][j], width=int(width_tab[j]), fg='blue',
                                        font=('Arial', 14), justify='left')
                week_1_table.grid(row=rows, column=j, pady=(10, 0), sticky='w')
            rows += 1

        canvas.create_window((0, 0), window=content_frame, anchor=Tk.NW)
        content_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(Tk.ALL)  # Get bounding box of canvas with Buttons.
        canvas.configure(scrollregion=bbox, width=1100, height=750)


    def tab_3_screen(self):
        master_frame = Tk.Frame(self.tab3)
        master_frame.grid(sticky=Tk.NSEW)
        master_frame.columnconfigure(0, weight=1)
        #
        # # Create a frame for the canvas and scrollbar(s).
        frame2 = Tk.Frame(master_frame)
        frame2.grid(row=3, column=0, sticky=Tk.NW)
        #
        # # Add a canvas in that frame.
        canvas = Tk.Canvas(frame2)
        canvas.grid(row=0, column=0)
        #
        # # Create a vertical scrollbar linked to the canvas.
        vsbar = Tk.Scrollbar(frame2, orient=Tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=Tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)
        #
        # # Create a horizontal scrollbar linked to the canvas.
        hsbar = Tk.Scrollbar(frame2, orient=Tk.HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=1, column=0, sticky=Tk.EW)
        canvas.configure(xscrollcommand=hsbar.set)

        # Create a frame on the canvas to contain the content.
        # content_frame = Tk.Frame(canvas, bg="Red", bd=2)
        content_frame = Tk.Frame(canvas)
        #
        table_title = ["Date", "Time","Reason(s)","Charged ($CAD)"]
        results = get_billing_info(self.user[14])
        #results = []
        appointment_list = [lis for lis in results]
        if appointment_list:
            for i in range(0, len(appointment_list)):
                appointment_list[i] = user_appointment(list(appointment_list[i]))
        print(appointment_list)
        Week = appointment_list
        width_tab = [14, 10, 18, 24]
        ttk.Label(content_frame, text="Billing Details", font=('Arial', 20, 'bold'), justify='center').grid(
            column=0, row=0, columnspan=6, pady=10)
        refresh = Tk.Button(content_frame, text="Refresh", width=16,
                            command=lambda: ([master_frame.destroy(), self.tab_3_screen()]))
        refresh.grid(row=0, column=5, sticky='w')
        # # Create a frame on the canvas to contain the buttons.
        #
        for i in range(0, len(table_title)):
            week_0_table = Tk.Label(content_frame, text=table_title[i], width=int(width_tab[i]), fg='blue',
                                    font=('Arial', 14, 'bold'), justify='left')
            week_0_table.grid(row=1, column=i, pady=(10, 0), sticky='w')

        rows = 2
        for i in range(0, len(Week)):
            for j in range(0, len(table_title)):
                week_1_table = Tk.Label(content_frame, text=Week[i][j], width=int(width_tab[j]), fg='blue',
                                        font=('Arial', 14), justify='left')
                week_1_table.grid(row=rows, column=j, pady=(10, 0), sticky='w')
            rows += 1

        canvas.create_window((0, 0), window=content_frame, anchor=Tk.NW)
        content_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(Tk.ALL)  # Get bounding box of canvas with Buttons.
        canvas.configure(scrollregion=bbox, width=1100, height=750)