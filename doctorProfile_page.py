import tkinter as Tk
from tkinter import ttk, END, VERTICAL, NS, RIGHT, Y, LEFT, BOTH, messagebox

from tkcalendar import DateEntry
from tkintertable import TableCanvas, TableModel

# import tkintertable
from DBHelper import appointment_listByDoctorID, getPatient_info, getpatient_appointment_history, \
    add_prescriton_per_appointment, update_doctorNote

ROWS_DISP = 20  # Number of rows to display.
COLS_DISP = 7  # Number of columns to display.


class doctorProfile(object):
    # Initialization
    def __init__(self, parent, currentUser):
        """Constructor"""
        self.user = currentUser
        self.root = parent
        self.root.title("Walk-In Clinic Management System ====  Welcome " + self.user[4] + " " + self.user[5])
        self.root.geometry("1148x900")
        self.canvas = None
        self.prescriptionList = []
        self.appointment_id = Tk.StringVar()
        self.appointment_sid = Tk.StringVar()
        self.masterFrame = None
        self.precptFrame = None
        self.nameM =  Tk.StringVar()
        self.numPills = Tk.StringVar()
        self.freq = Tk.StringVar()
        self.spc = Tk.StringVar()
        self.exp =None
        self.filled = None
        self.apid0 = Tk.StringVar()
        self.dn = None
        # self.root.configure(bg='#FBE7C6')
        self.frame = Tk.Frame(parent)
        self.frame.grid()
        self.__profile()

    def __profile(self):
        green = "#d2ffd2"
        red = "#dd0202"
        tab_css = ttk.Style()
        # tab_css.theme_create("MyStyle", parent="alt", settings={
        #     "TNotebook.Tab": {"configure": {"padding": [50, 10],
        #                                     "background": '#BD4B4B', "font": ('URW Gothic L', '16', 'bold')}, }})
        tab_css.theme_create("NewStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [65, 10], "background": green, "font": ('URW Gothic L', '16', 'bold')},
                "map": {"background": [("selected", red)],
                        "expand": [("selected", [1, 1, 1, 0])]}}})
        tab_css.theme_use("NewStyle")
        tabControl = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(tabControl)
        self.tab2 = ttk.Frame(tabControl)
        self.tab3 = ttk.Frame(tabControl)

        Tk.Label(self.root, text='Welcome to KW - CLINIC', font=("Times New Roman", 25)).grid(row=0, column=0,
                                                                                              columnspan=1)
        logout = Tk.Button(self.root, text="Logout", bg='red', fg="white", font=("Times New Roman", 15), pady=5,
                           command=lambda: ([self.root.quit()]))
        logout.config(width=15)
        logout.grid(row=0, column=0, sticky='S', pady=10, padx=(950, 0))
        tabControl.add(self.tab1, text='Appointment Calender')
        tabControl.add(self.tab2, text='Patient Notes (Today App)')
        #tabControl.add(self.tab3, text='Search Patient History')
        tabControl.grid()

        # =================================================================================
        # 5-Days Appointment Calender
        # =================================================================================
        self.tab_1_screen()
        # =================================================================================
        # Patient Notes (Today App)
        # =================================================================================
        self.tab_2_screen()

        # =================================================================================
        # Search Patient History
        # =================================================================================
        self.tab_3_screen()

    # =================================================================================
    # Tab 1 Screen
    # =================================================================================

    def tab_1_screen(self):
        master_frame = Tk.Frame(self.tab1)
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
        table_title = ["Appointment ID", "Full Name", "Age", "Reason(s)", "Date", "Time"]
        results = appointment_listByDoctorID(self.user[3])
        appointment_list = [lis for lis in results]
        Week = appointment_list

        width_tab = [12, 18, 10, 24, 10, 10]
        ttk.Label(content_frame, text="5-Days Appointment Schedule", font=('Arial', 20, 'bold'), justify='center').grid(
            column=0, row=0, columnspan=6, pady=10)
        refresh = Tk.Button(content_frame, text="Refresh", width=16,
                            command=lambda: ([master_frame.destroy(), self.tab_1_screen()]))
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

    # =================================================================================
    # Tab 2 Screen
    # =================================================================================
    def tab_2_screen(self):
        appointment_id = Tk.Label(self.tab2, text="Appointment ID: ", width=16, font=('Arial', 14, 'bold'))
        appointment_id.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        apid = Tk.Entry(self.tab2, text="Get", width=30, font=('Arial', 14, 'bold'), textvariable=self.appointment_id)
        apid.grid(row=0, column=0, sticky='w', padx=(200, 0), pady=(15, 0))
        get = Tk.Button(self.tab2, text="Get", width=10, font=('Arial', 12, 'bold'), command=self.tab_2_screen_02)
        get.grid(row=0, column=0, sticky='w', padx=(530, 0), pady=(15, 0))

    def tab_2_screen_02(self):
        appoint_id = self.appointment_id.get()
        results = getPatient_info(appoint_id)
        if results:
            user_info = [lis for lis in results[0]]
        else:
            user_info=[]
        self.master_frame = Tk.Frame(self.tab2)
        self.master_frame.grid(sticky=Tk.NSEW)
        self.master_frame.columnconfigure(0, weight=1)
        #
        # # Create a frame for the canvas and scrollbar(s).
        frame2 = Tk.Frame(self.master_frame)
        frame2.grid(row=4, column=0, sticky=Tk.NW)
        #
        # # Add a canvas in that frame.
        canvas = Tk.Canvas(frame2)
        canvas.grid(row=4, column=0)

        # # Create a vertical scrollbar linked to the canvas.
        vsbar = Tk.Scrollbar(frame2, orient=Tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=4, column=1, sticky=Tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)
        #
        # # Create a horizontal scrollbar linked to the canvas.
        hsbar = Tk.Scrollbar(frame2, orient=Tk.HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=5, column=0, sticky=Tk.EW)
        canvas.configure(xscrollcommand=hsbar.set)


        content_frame = Tk.Frame(canvas)
        #

        # =================================================================================
        # Appointment ID
        # =================================================================================
        appointment_id_L = Tk.Label(content_frame, text="Appointment ID: ", width=16, font=('Arial', 14, 'bold'))
        appointment_id_L.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        appointment_id = Tk.Label(content_frame, text=appoint_id, width=16, font=('Arial', 14, 'bold'),fg='#f00')
        appointment_id.grid(row=0, column=1, sticky='w', padx=(10, 0), pady=(15, 0))
        if user_info:
            # =================================================================================
            # Name
            # =================================================================================

            firstN_L = Tk.Label(content_frame, text="First Name: ", width=16, font=('Arial', 14, 'bold'))
            firstN_L.grid(row=1, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
            firstN = Tk.Label(content_frame, text=user_info[0], width=16, font=('Arial', 14, 'bold'),fg='#f00')
            firstN.grid(row=1, column=1, sticky='w', padx=(10, 0), pady=(15, 0))

            lastN_L = Tk.Label(content_frame, text="Last Name: ", width=16, font=('Arial', 14, 'bold'))
            lastN_L.grid(row=1, column=2, sticky='w', padx=(10, 0), pady=(15, 0))
            lastN = Tk.Label(content_frame, text=user_info[1], width=16, font=('Arial', 14, 'bold'),fg='#f00')
            lastN.grid(row=1, column=3, sticky='w', padx=(10, 0), pady=(15, 0))
            # =================================================================================
            # DOB and Family Doctor
            # =================================================================================
            dob_L = Tk.Label(content_frame, text="Date of Birth: ", width=16, font=('Arial', 14, 'bold'))
            dob_L.grid(row=2, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
            dob = Tk.Label(content_frame, text=user_info[2], width=16, font=('Arial', 14, 'bold'),fg='#f00')
            dob.grid(row=2, column=1, sticky='w', padx=(10, 0), pady=(15, 0))

            fd_L = Tk.Label(content_frame, text="Family Doctor: ", width=16, font=('Arial', 14, 'bold'))
            fd_L.grid(row=2, column=2, sticky='w', padx=(10, 0), pady=(15, 0))
            fd = Tk.Label(content_frame, text=user_info[4], width=16, font=('Arial', 14, 'bold'),fg='#f00')
            fd.grid(row=2, column=3, sticky='w', padx=(10, 0), pady=(15, 0))

            # =================================================================================
            # HealthCard and Reason
            # =================================================================================
            hc_L = Tk.Label(content_frame, text="HealthCard No: ", width=16, font=('Arial', 14, 'bold'))
            hc_L.grid(row=3, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
            hc = Tk.Label(content_frame, text=user_info[3], width=16, font=('Arial', 14, 'bold'),fg='#f00')
            hc.grid(row=3, column=1, sticky='w', padx=(10, 0), pady=(15, 0))

            rsn_L = Tk.Label(content_frame, text="Appointment For: ", width=16, font=('Arial', 14, 'bold'))
            rsn_L.grid(row=3, column=2, sticky='w', padx=(10, 0), pady=(15, 0))
            rsn = Tk.Label(content_frame, text=user_info[5], width=16, font=('Arial', 14, 'bold'),fg='#f00')
            rsn.grid(row=3, column=3, sticky='w', padx=(10, 0), pady=(15, 0))
            # =================================================================================
            # Description
            # =================================================================================
            sy_L = Tk.Label(content_frame, text="Symptoms: ", width=16, font=('Arial', 14, 'bold'))
            sy_L.grid(row=4, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
            sy = Tk.Label(content_frame, text=user_info[6], width=16, font=('Arial', 14, 'bold'),fg='#f00')
            sy.grid(row=4, column=1, sticky='w', padx=(10, 0), pady=(15, 0))
            # =================================================================================
            # DoctorNotes
            # =================================================================================
            dn_L = Tk.Label(content_frame, text="Doctor Notes: ", width=16, font=('Arial', 14, 'bold'))
            dn_L.grid(row=5, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
            self.dn= Tk.Text(content_frame, height= 15, width=60, font=('Arial', 14, 'bold'))
            self.dn.grid(row=5, column=1, sticky='w', padx=(10, 0), pady=(15, 0), columnspan=3)
            # =================================================================================
            # Prescription
            # =================================================================================
            precription = Tk.Button(content_frame, text="Add Prescriptions", width=25, font=('Arial', 12, 'bold'), command= lambda : self.prescription())
            precription.grid(row=6, column=3, sticky='w', padx=(0, 0), pady=(15, 0),columnspan = 3)


        save = Tk.Button(content_frame, text="Save", width=10, font=('Arial', 12, 'bold'),command=lambda:[(self.save_tab2())])
        save.grid(row=7, column=4, sticky='w', padx=(0, 0), pady=(35, 0),columnspan = 3)
        canvas.create_window((0, 0), window=content_frame, anchor=Tk.NW)
        content_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(Tk.ALL)  # Get bounding box of canvas with Buttons.
        canvas.configure(scrollregion=bbox, width=1100, height=750)

    # =================================================================================
    # Tab 3 Screen
    # =================================================================================
    def tab_3_screen(self):
        appointment_id = Tk.Label(self.tab3, text="Appointment ID: ", width=16, font=('Arial', 14, 'bold'))
        appointment_id.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        apid = Tk.Entry(self.tab3, text="Get", width=30, font=('Arial', 14, 'bold'), textvariable=self.appointment_sid)
        apid.grid(row=0, column=0, sticky='w', padx=(200, 0), pady=(15, 0))
        get = Tk.Button(self.tab3, text="Get", width=10, font=('Arial', 12, 'bold'), command=self.tab_3_screen_02)
        get.grid(row=0, column=0, sticky='w', padx=(530, 0), pady=(15, 0))

    def tab_3_screen_02(self):
        appoint_id = self.appointment_sid.get()
        #results = getpatient_appointment_history(appoint_id)
        results = []
        if results:
            #user_info = [lis for lis in results[0]]
            user_info = []
        else:
            user_info = []
        self.master_frame = Tk.Frame(self.tab3)
        self.master_frame.grid(sticky=Tk.NSEW)
        self.master_frame.columnconfigure(0, weight=1)
        #
        # # Create a frame for the canvas and scrollbar(s).
        frame2 = Tk.Frame(self.master_frame)
        frame2.grid(row=4, column=0, sticky=Tk.NW)
        #
        # # Add a canvas in that frame.
        canvas = Tk.Canvas(frame2)
        canvas.grid(row=4, column=0)

        # # Create a vertical scrollbar linked to the canvas.
        vsbar = Tk.Scrollbar(frame2, orient=Tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=4, column=1, sticky=Tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)
        #
        # # Create a horizontal scrollbar linked to the canvas.
        hsbar = Tk.Scrollbar(frame2, orient=Tk.HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=5, column=0, sticky=Tk.EW)
        canvas.configure(xscrollcommand=hsbar.set)
        content_frame = Tk.Frame(canvas)
        #if user_info:
        # =================================================================================
        # Name
        # =================================================================================
        firstN_L = Tk.Label(content_frame, text="First Name: ", width=16, font=('Arial', 14, 'bold'))
        firstN_L.grid(row=1, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        firstN = Tk.Label(content_frame,  width=16, font=('Arial', 14, 'bold'), fg='#f00')
        firstN.grid(row=1, column=1, sticky='w', padx=(10, 0), pady=(15, 0))

        lastN_L = Tk.Label(content_frame, text="Last Name: ", width=16, font=('Arial', 14, 'bold'))
        lastN_L.grid(row=1, column=2, sticky='w', padx=(10, 0), pady=(15, 0))
        lastN = Tk.Label(content_frame, width=16, font=('Arial', 14, 'bold'), fg='#f00')
        lastN.grid(row=1, column=3, sticky='w', padx=(10, 0), pady=(15, 0))
            # =================================================================================
            # DOB
            # =================================================================================
        dob_L = Tk.Label(content_frame, text="Date of Birth: ", width=16, font=('Arial', 14, 'bold'))
        dob_L.grid(row=2, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        dob = Tk.Label(content_frame, width=16, font=('Arial', 14, 'bold'), fg='#f00')
        dob.grid(row=2, column=1, sticky='w', padx=(10, 0), pady=(15, 0))

            # =================================================================================
            # HealthCard
            # =================================================================================
        hc_L = Tk.Label(content_frame, text="HealthCard No: ", width=16, font=('Arial', 14, 'bold'))
        hc_L.grid(row=2, column=2, sticky='w', padx=(10, 0), pady=(15, 0))
        hc = Tk.Label(content_frame,  width=16, font=('Arial', 14, 'bold'), fg='#f00')
        hc.grid(row=2, column=3, sticky='w', padx=(10, 0), pady=(15, 0))

        apptHistory_L = Tk.Label(content_frame, text="Appointment(s) History: ", width=20, font=('Arial', 14, 'bold'))
        apptHistory_L.grid(row=3, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        apptHistory = Tk.Label(content_frame,  width=16, font=('Arial', 14, 'bold'), fg='#f00')
        apptHistory.grid(row=3, column=1, sticky='w', padx=(10, 0), pady=(15, 0))

        save = Tk.Button(content_frame, text="Save", width=10, font=('Arial', 12, 'bold'),command=lambda:[(self.save_tab2())])
        save.grid(row=7, column=4, sticky='w', padx=(0, 0), pady=(35, 0), columnspan=3)
        canvas.create_window((0, 0), window=content_frame, anchor=Tk.NW)
        content_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(Tk.ALL)  # Get bounding box of canvas with Buttons.
        canvas.configure(scrollregion=bbox, width=1100, height=750)

    # =================================================================================
    # SAVE tab 3 content
    # =================================================================================
    def save_tab2(self):
        doctor_notes = self.dn.get("1.0","end-1c")
        appointment_id= self.appointment_id.get()
        update_doctorNote(appointment_id, doctor_notes)
        self.master_frame.destroy()
        self.tab_2_screen()


    # =================================================================================
    # refresh tab 3 content
    # =================================================================================
    def save_tab3(self):
        self.master_frame.destroy()
        self.tab_3_screen()

    # =================================================================================
    # Add prescription
    # =================================================================================

    def prescription(self):
        self.precptFrame = Tk.Toplevel()
        name = Tk.Label(self.precptFrame, text="Name: ", width=16, font=('Arial', 14, 'bold'))
        name.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        apid = Tk.Entry(self.precptFrame, text="Get", width=30, font=('Arial', 14, 'bold'), textvariable=self.nameM)
        apid.grid(row=0, column=1, sticky='w', padx=(0, 0), pady=(15, 0))

        numP = Tk.Label(self.precptFrame, text="Number of pills: ", width=16, font=('Arial', 14, 'bold'))
        numP.grid(row=1, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        apid = Tk.Entry(self.precptFrame, text="Get", width=30, font=('Arial', 14, 'bold'), textvariable=self.numPills)
        apid.grid(row=1, column=1, sticky='w', padx=(0, 0), pady=(15, 0))

        numP = Tk.Label(self.precptFrame, text="Frequency: ", width=16, font=('Arial', 14, 'bold'))
        numP.grid(row=2, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        apid = Tk.Entry(self.precptFrame, text="Get", width=30, font=('Arial', 14, 'bold'), textvariable=self.freq)
        apid.grid(row=2, column=1, sticky='w', padx=(0, 0), pady=(15, 0))

        numP = Tk.Label(self.precptFrame, text="Special Instructions: ", width=16, font=('Arial', 14, 'bold'))
        numP.grid(row=3, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        apid = Tk.Entry(self.precptFrame, text="Get", width=30, font=('Arial', 14, 'bold'), textvariable=self.spc)
        apid.grid(row=3, column=1, sticky='w', padx=(0, 0), pady=(15, 0))


        dobLabel = Tk.Label(self.precptFrame, padx=10, pady=20, text="Expiration Date: ",
                            font=('Arial', 14, 'bold'))
        dobLabel.grid(row=4, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        self.exp = DateEntry(self.precptFrame, padx=10, pady=20, width=18, year=2021, month=6, day=22,
                             background='darkblue', foreground='white', borderwidth=2,  date_pattern='yyyy-mm-dd',
                             font=('Arial', 14, 'bold'))
        self.exp.grid(row=4, column=1, sticky='w', padx=(0, 0), pady=(15, 0))


        dobLabel = Tk.Label(self.precptFrame, padx=10, pady=20, text="Date Filled: ",
                            font=('Arial', 14, 'bold'))
        dobLabel.grid(row=5, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        self.filled = DateEntry(self.precptFrame, padx=10, pady=20, width=18, year=2021, month=6, day=22,
                             background='darkblue', foreground='white', borderwidth=2,  date_pattern='yyyy-mm-dd',
                             font=('Arial', 14, 'bold'))
        self.filled.grid(row=5, column=1, sticky='w', padx=(0, 0), pady=(15, 0))

        numP = Tk.Label(self.precptFrame, text="Appointment ID: ", width=16, font=('Arial', 14, 'bold'))
        numP.grid(row=6, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        apid = Tk.Entry(self.precptFrame, text="Get", width=30, font=('Arial', 14, 'bold'), textvariable=self.apid0)
        apid.grid(row=6, column=1, sticky='w', padx=(0, 0), pady=(15, 0))

        save = Tk.Button(self.precptFrame, text="Save", width=10, font=('Arial', 14, 'bold'), command= lambda:self.add_pre())
        save.grid(row=7, column=1, sticky='w', padx=(0, 0), pady=(35, 0))

    def add_pre(self):
        name = self.nameM.get()
        num_pills = self.numPills.get()
        Frequency = self.freq.get()
        special_instruction = self.spc.get()
        expr_date = self.exp.get()
        filled = self.filled.get()
        appointment_id = self.apid0.get()
        print(expr_date)
        add_prescriton_per_appointment(name, num_pills, Frequency, special_instruction, expr_date, filled,
                                       appointment_id)
        messagebox.showinfo("Success", "Prescription Added")
        self.precptFrame.withdraw()
