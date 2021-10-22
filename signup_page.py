# ==================================================
#                   Imports                        #
# ==================================================
import tkinter as Tk
from tkinter import messagebox
from utilities import *
from tkcalendar import DateEntry
from DBHelper import insertUSER, insertPatient


# ==================================================
#                 newUser Class                    #
# ==================================================
from tkcalendar import Calendar


class newUser(Tk.Frame):
    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.secondFrame = Tk.Toplevel()
        self.secondFrame.title(" ***  Walk-In Clinic Management System --- Account SignUp ***")
        self.secondFrame.geometry("1050x730")
        self.secondFrame.resizable(0, 0)
        # ------ Variables -----------
        self.__nUFormFontSize = 16
        self.__LoginFontSize = 18
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
        self.confirmPassword = Tk.StringVar()
        # ------ Buttons -----------
        self.newUser = None
        self.submitUser = None
        self.__newUser()

    # --------------------------------------------------------------------------------
    # Patient Profile
    # --------------------------------------------------------------------------------
    def __newUser(self):
        Title = Tk.Label(self.secondFrame, padx=0, pady=10, text=" ---- User Login Form ----",
                         font=("Times New Roman", self.__nUFormFontSize))
        Title.grid(column=0, row=0, sticky=Tk.E, padx=5, pady=5)
        # --------------------------------------------------------------------------------
        # Full Name
        # --------------------------------------------------------------------------------
        firstNameLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="First Name: ",
                                  font=("Times New Roman", self.__nUFormFontSize))
        firstNameLabel.grid(column=0, row=1, sticky=Tk.E, padx=5, pady=5)

        firstName = Tk.Entry(self.secondFrame, relief="solid", textvariable=self.fname, width=20, bd=1,
                             font=("Times New Roman", self.__nUFormFontSize))
        firstName.grid(column=1, row=1, sticky=Tk.E, padx=5, pady=5)

        lastNameLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="Last Name: ",
                                 font=("Times New Roman", self.__nUFormFontSize))
        lastNameLabel.grid(column=2, row=1, sticky=Tk.E, padx=(20, 0), pady=5)
        lastName = Tk.Entry(self.secondFrame, relief="solid", textvariable=self.lname, width=20, bd=1,
                            font=("Times New Roman", self.__nUFormFontSize))
        lastName.grid(column=3, row=1, sticky=Tk.E, padx=5, pady=5)
        # --------------------------------------------------------------------------------
        # Gender
        # --------------------------------------------------------------------------------
        genderLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="Gender: ",
                               font=("Times New Roman", self.__nUFormFontSize))
        genderLabel.grid(column=0, row=2, sticky=Tk.E, padx=5, pady=5)
        options = ['Female', 'Male', 'Other']
        gender = Tk.OptionMenu(self.secondFrame, self.genderOption, *options)
        gender.config(width=12, font=('Times New Roman', self.__nUFormFontSize), bg='light blue')
        gender.grid(column=1, row=2, sticky=Tk.E, padx=5, pady=5)
        # --------------------------------------------------------------------------------
        # Date Of Birth
        # --------------------------------------------------------------------------------
        dobLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="Date of Birth: ",
                            font=("Times New Roman", self.__nUFormFontSize))
        dobLabel.grid(column=2, row=2, sticky=Tk.E, padx=(5,0), pady=5)
        self.dob = DateEntry(self.secondFrame, padx=10, pady=20, width=18, year=2021, month=6, day=22,
                             background='darkblue', foreground='white', borderwidth=2,  date_pattern='yyyy-mm-dd',
                             font=("Times New Roman", self.__nUFormFontSize))
        self.dob.grid(column=3, row=2, sticky=Tk.E, padx=5, pady=5)


        # --------------------------------------------------------------------------------
        # Phone
        # --------------------------------------------------------------------------------
        phoneLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="Phone: ",
                              font=("Times New Roman", self.__nUFormFontSize))
        phoneLabel.grid(column=0, row=5, sticky=Tk.E, padx=5, pady=5)
        phoneNumber = Tk.Entry(self.secondFrame, relief="solid", textvariable=self.phone, width=20, bd=1,
                               font=("Times New Roman", self.__nUFormFontSize))
        phoneNumber.grid(column=1, row=5, sticky=Tk.E)

        # --------------------------------------------------------------------------------
        # HealthCare No.
        # --------------------------------------------------------------------------------
        healthcareLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="HealthCard Number: ",
                                   font=("Times New Roman", self.__nUFormFontSize))
        healthcareLabel.grid(column=0, row=6, sticky=Tk.E, padx=5, pady=5)
        hCardNumber = Tk.Entry(self.secondFrame, relief="solid", textvariable=self.healthCard, width=20, bd=1,
                               font=("Times New Roman", self.__nUFormFontSize))
        hCardNumber.grid(column=1, row=6, sticky=Tk.E)

        # --------------------------------------------------------------------------------
        # Email
        # --------------------------------------------------------------------------------
        emailLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="Email: ",
                              font=("Times New Roman", self.__nUFormFontSize))
        emailLabel.grid(column=2, row=5, sticky=Tk.E, padx=5, pady=5)
        emailNumber = Tk.Entry(self.secondFrame, relief="solid", textvariable=self.email, width=20, bd=1,
                               font=("Times New Roman", self.__nUFormFontSize))
        emailNumber.grid(column=3, row=5, sticky=Tk.E)
        # --------------------------------------------------------------------------------
        # Address Info
        # --------------------------------------------------------------------------------
        SAddLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="Street Address: ",
                             font=("Times New Roman", self.__nUFormFontSize))
        SAddLabel.grid(column=2, row=6, sticky=Tk.E, padx=5, pady=5)
        StreetAdd = Tk.Entry(self.secondFrame, relief="solid", textvariable=self.street, width=20, bd=1,
                             font=("Times New Roman", self.__nUFormFontSize))
        StreetAdd.grid(column=3, row=6, sticky=Tk.E)

        cityLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="City: ",
                             font=("Times New Roman", self.__nUFormFontSize))
        cityLabel.grid(column=0, row=7, sticky=Tk.E, padx=5, pady=5)
        city = Tk.Entry(self.secondFrame, relief="solid", textvariable=self.city, width=20, bd=1,
                        font=("Times New Roman", self.__nUFormFontSize))
        city.grid(column=1, row=7, sticky=Tk.E)

        zipCodeLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="Zip Code: ",
                                font=("Times New Roman", self.__nUFormFontSize))
        zipCodeLabel.grid(column=2, row=7, sticky=Tk.E, padx=5, pady=5)
        zipCode = Tk.Entry(self.secondFrame, relief="solid", textvariable=self.zipCode, width=8, bd=1,
                           font=("Times New Roman", self.__nUFormFontSize))
        zipCode.grid(column=3, row=7, sticky=Tk.E)

        provinceLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="Province: ",
                                 font=("Times New Roman", self.__nUFormFontSize))
        provinceLabel.grid(column=0, row=8, sticky=Tk.E, padx=(120, 0), pady=5)
        province = Tk.Entry(self.secondFrame, relief="solid", textvariable=self.province, width=20, bd=1,
                            font=("Times New Roman", self.__nUFormFontSize))
        province.grid(column=1, row=8, sticky=Tk.E)

        # --------------------------------------------------------------------------------
        # Password
        # --------------------------------------------------------------------------------
        passLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="Password: ",
                             font=("Times New Roman", self.__nUFormFontSize))
        passLabel.grid(column=2, row=8, sticky=Tk.E, padx=5, pady=5)
        newPassword = Tk.Entry(self.secondFrame, relief="solid", textvariable=self.nPassword, width=20, bd=1,
                               font=("Times New Roman", self.__nUFormFontSize))
        newPassword.grid(column=3, row=8, sticky=Tk.E)

        cpassLabel = Tk.Label(self.secondFrame, padx=10, pady=20, text="Confirm Password: ",
                              font=("Times New Roman", self.__nUFormFontSize))
        cpassLabel.grid(column=0, row=9, sticky=Tk.E, padx=5, pady=5)
        cPassword = Tk.Entry(self.secondFrame, relief="solid", textvariable=self.confirmPassword, width=20, bd=1,
                             font=("Times New Roman", self.__nUFormFontSize))
        cPassword.grid(column=1, row=9, sticky=Tk.E)

        # --------------------------------------------------------------------------------
        # Submit Button
        # --------------------------------------------------------------------------------
        self.submitUser = Tk.Button(self.secondFrame, text="Create", bg='green', fg="white",
                                    font=("Times New Roman", self.__LoginFontSize),
                                    command=lambda: self.__patientCheck())
        self.submitUser.config(width=10)
        self.submitUser.grid(column=1, row=11, sticky=Tk.E, padx=0, pady=(50, 0))
        self.cancel = Tk.Button(self.secondFrame, text="Cancel", bg='red', fg="white",
                                font=("Times New Roman", self.__LoginFontSize),
                                command=lambda: self.secondFrame.withdraw())
        self.cancel.config(width=10)
        self.cancel.grid(column=2, row=11, sticky=Tk.E, padx=(70,0), pady=(50, 0))

    # --------------------------------------------------------------------------------
    # Check Patient Info
    # --------------------------------------------------------------------------------
    def __patientCheck(self):
        error = "Errors : \n"
        first_name = self.fname.get()
        last_name = self.lname.get()
        gender = self.genderOption.get()
        phone = self.phone.get()
        email = self.email.get()
        dob = self.dob.get()
        healthCard = self.healthCard.get()
        street = self.street.get()
        city = self.city.get()
        zipCode = self.zipCode.get()
        province = self.province.get()
        nPassword = self.nPassword.get()
        confirmPassword = self.confirmPassword.get()
        self.__clearVariables()
        check_email = checkEmailFormat(email)
        check_zipcode = checkZipCodeLength(zipCode.strip())
        check_firstname = checkAlphabeticString(first_name)
        check_lastname = checkAlphabeticString(last_name)
        check_password = compareIfPasswordMatch(nPassword, confirmPassword)
        if check_password and check_email and check_lastname and check_firstname and check_zipcode:
            messagebox.showinfo("Success", "Account Created Successfully")
            id = insertUSER(1, email, nPassword, 'Active')
            gn = gender_v(gender)
            phone = formatphone(phone)
            insertPatient(first_name, last_name, gn, phone, email, dob, healthCard, street, city, zipCode, province, id)
            self.secondFrame.destroy()
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

        # check patient info

    # --------------------------------------------------------------------------------
    # Clear Variables
    # --------------------------------------------------------------------------------
    def __clearVariables(self):
        self.fname.set("")
        self.lname.set("")
        self.genderOption.set("")
        self.phone.set("")
        self.email.set("")
        self.healthCard.set("")
        self.street.set("")
        self.city.set("")
        self.zipCode.set("")
        self.province.set("")
        self.nPassword.set("")
        self.confirmPassword.set("")
