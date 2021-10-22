import tkinter as Tk
from tkinter import ttk, messagebox

from DBHelper import appointment_lis, unconfirmed_appointment_lis, update_appointment, add_bill
from utilities import clean_unconfirmedList


class nurseProfile(object):
    # Initialization
    def __init__(self, parent, currentUser):
        """Constructor"""
        self.user = currentUser
        self.root = parent
        self.root.title("Walk-In Clinic Management System ====  Welcome " + self.user[3]+ " "+ self.user[4])
        self.root.geometry("1100x700")
        # self.root.configure(bg='#FBE7C6')
        self.tab1=None
        self.tab2 = None
        self.tab3 = None
        self.patientID = Tk.StringVar()
        self.doc_id = Tk.StringVar()
        self.appointment_id = Tk.StringVar()
        self.billAmount = Tk.StringVar()
        self.bill_id = Tk.StringVar()
        self.frame = Tk.Frame(parent)
        self.frame.grid()
        self.__profile()

    def __profile(self):
        green = "#d2ffd2"
        red = "#dd0202"
        tab_css = ttk.Style()
        tab_css.theme_create("MyStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [65, 10], "background": green, "font": ('URW Gothic L', '16', 'bold')},
                "map": {"background": [("selected", red)],
                        "expand": [("selected", [1, 1, 1, 0])]}}})
        tab_css.theme_use("MyStyle")
        tabControl = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(tabControl)
        self.tab2 = ttk.Frame(tabControl)
        self.tab3 = ttk.Frame(tabControl)

        # bg = '#FBE7C6'
        Tk.Label(self.root, text='Welcome to KW - CLINIC', font=("Times New Roman", 25)).grid(row=0, column=0,
                                                                                             columnspan=1)
        logout = Tk.Button(self.root, text="Logout", bg='red', fg="white", font=("Times New Roman", 15), pady=5,
                           command= lambda :self.root.quit())
        logout.config(width=15)
        logout.grid(row=0, column=0, sticky='S', pady=10, padx=(870, 0))
        tabControl.add(self.tab1, text='Appointment Calender')
        tabControl.add(self.tab2, text='Unconfirmed Appointments')
        tabControl.add(self.tab3, text='Billing Patient')
        tabControl.grid()


        # =================================================================================
        # Appointment Calender
        # =================================================================================
        self.tab_1_screen()

        # =================================================================================
        # Unconfirmed Appointments
        # =================================================================================
        self.tab_2_screen_0()

        # =================================================================================
        # Billing Patient
        # =================================================================================

        self.tab_3_screen_0()

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
        table_title = ["Appointment ID", "Patient Name", "Doctor Name", "Reason(s)", "Date", "Time"]
        results = appointment_lis()
        #print(results)
        appointment_list = [lis for lis in results]
        Week = appointment_list

        width_tab = [12, 18, 10, 24, 10, 10]
        ttk.Label(content_frame, text="Appointment Schedule", font=('Arial', 20, 'bold'), justify='center').grid(
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
        #
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

    def tab_2_screen_0(self):
        appointment_id = Tk.Label(self.tab2, text="Appointment ID: ", width=16, font=('Arial', 14, 'bold'))
        appointment_id.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=(15, 0))
        apid = Tk.Entry(self.tab2, text="Get", width=30, font=('Arial', 14, 'bold'), textvariable=self.appointment_id)
        apid.grid(row=0, column=0, sticky='w', padx=(200, 0), pady=(15, 0))

        doctor_id = Tk.Label(self.tab2, text="Doctor ID: ", width=16, font=('Arial', 14, 'bold'))
        doctor_id.grid(row=0, column=0, sticky='w', padx=(410, 0), pady=(15, 0))
        doid = Tk.Entry(self.tab2, text="Get", width=30, font=('Arial', 14, 'bold'), textvariable=self.doc_id)
        doid.grid(row=0, column=0, sticky='w', padx=(600, 0), pady=(15, 0))

        confirm = Tk.Button(self.tab2, text="Confirm", width=10, font=('Arial', 12, 'bold'), command = self.confirm_appoinment)
        confirm.grid(row=0, column=0, sticky='w', padx=(900, 0), pady=(15, 0))
        self.tab_2_screen()

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
        table_title = ["Appointment ID", "Patient Name","Reason(s)", "Date", "Time"]
        result= unconfirmed_appointment_lis()
        print(result)
        results = clean_unconfirmedList(result)
        appointment_list = [lis for lis in results]
        Week = appointment_list

        width_tab = [12, 18, 24, 10, 10]
        ttk.Label(content_frame, text="Unconfirmed Appointments", font=('Arial', 20, 'bold'), justify='center').grid(
            column=0, row=0, columnspan=6, pady=10)
        refresh = Tk.Button(content_frame, text="Refresh", width=16,
                            command=lambda: ([master_frame.destroy(), self.tab_2_screen_0()]))
        refresh.grid(row=0, column=5, sticky='w')
        # # Create a frame on the canvas to contain the buttons.
        #
        for i in range(0, len(table_title)):
            week_0_table = Tk.Label(content_frame, text=table_title[i], width=int(width_tab[i]), fg='blue',
                                    font=('Arial', 14, 'bold'), justify='left')
            week_0_table.grid(row=1, column=i, pady=(10, 0), sticky='w')
        #
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

    def confirm_appoinment(self):
        appointment = self.appointment_id.get()
        doctor = self.doc_id.get()
        if appointment and doctor:
            print(doctor)
            print(appointment)
            print(self.user[13])
            update_appointment(appointment, self.user[13], doctor)
            messagebox.showinfo("Success", "Appointment confirmed, Refresh to see changes")
        else:
            error = "Invalid IDs"
            messagebox.showinfo("Error", error)

    def tab_3_screen_0(self):
        ttk.Label(self.tab3, text="Billing Portal", font=('Arial', 20, 'bold'), justify='center').grid(
            column=0, row=0, columnspan=6, pady=(50,0))

        appointment_id = Tk.Label(self.tab3, text="Appointment ID: ", width=16, font=('Arial', 14, 'bold'),justify='center')
        appointment_id.grid(row=1, column=0, sticky='w', padx=(200, 0), pady=(25, 0))
        apid = Tk.Entry(self.tab3, text="Get", width=25, font=('Arial', 14, 'bold'), textvariable=self.bill_id)
        apid.grid(row=1, column=1, sticky='w', padx=(0, 0), pady=(25, 0))


        billing_id = Tk.Label(self.tab3, text="Patient ID: ", width=16, font=('Arial', 14, 'bold'),justify='center')
        billing_id.grid(row=2, column=0, sticky='w', padx=(200, 0), pady=(25, 0))
        doid = Tk.Entry(self.tab3, text="Get", width=25, font=('Arial', 14, 'bold'), textvariable=self.patientID)
        doid.grid(row=2, column=1, sticky='w', padx=(0,0), pady=(25, 0))

        billing_id  = Tk.Label(self.tab3, text="Billing Amount($): ", width=16, font=('Arial', 14, 'bold'), justify='center')
        billing_id.grid(row=3, column=0, sticky='w', padx=(200, 0), pady=(25, 0))
        toid = Tk.Entry(self.tab3, text="Get", width=25, font=('Arial', 14, 'bold'), textvariable=self.billAmount)
        toid.grid(row=3, column=1, sticky='w', padx=(0,0), pady=(25, 0))

        confirm = Tk.Button(self.tab3, text="Charge Account", width=25, font=('Arial', 12, 'bold'), command = self.setBilling)
        confirm.grid(row=4, column=1, sticky='w', padx=(5, 0), pady=(45, 0))

    def setBilling(self):
        app_id = self.bill_id.get()
        pp_id = self.patientID.get()
        amount = self.billAmount.get()
        if app_id and pp_id and amount:
            add_bill(app_id, pp_id, self.user[13], amount)
            messagebox.showinfo("Success", "Payment Successful")
        else:
            error = "Invalid Entry"
            messagebox.showinfo("Error", error)
