"""########################################################
Author:
Student ID:
Due Date:
========================================================
File contains:
                chk_conn(conn)
##########################################################"""
import re
from DBHelper import getStaffInfoWithLoginDetails, getPatientInfoWithLoginDetails


# ==================================================
#              chk_conn Function                   #
#         Parameter: conn (String)                 #
# ==================================================
def chk_conn(conn):
    try:
        conn.cursor()
        return True
    except Exception as ex:
        return False


def checkEmailFormat(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        print("Valid Email")
        return True
    else:
        print("Invalid Email")
        return False


def checkZipCodeLength(zipCode):
    reg = r'[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ] ?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]'
    if re.fullmatch(reg, zipCode):
        print("Valid ZipCode")
        return True
    else:
        print("Invalid ZipCode")
        return False


def checkAlphabeticString(str_value):
    regex = r'[a-zA-Z ]{2,}'
    if re.fullmatch(regex, str_value):
        print("Valid String")
        return True
    else:
        print("Invalid String")
        return False


def int_Validator(input_amount):
    try:
        selected_int = int(input_amount)
        if selected_int < 0:
            print("Negative value detected.")
            return False, 0
        else:
            return True, selected_int
    except ValueError:
        print("Please enter number.")
        return False, 0


def compareIfPasswordMatch(password, confirmPassword):
    return password == confirmPassword


def gender_v(gender):
    if gender == 'Male':
        return 'M'
    elif gender == 'Female':
        return 'F'
    else:
        return 'O'


def getValid_Staff(username, password, role):
    result = getStaffInfoWithLoginDetails(username, role)
    if not result:
        return False, result
    else:
        user_cred = [lis for lis in result[0]]
        if user_cred[1] == password and user_cred[0] == role:  # need to make change for result
            return True, user_cred
        else:
            return False, []


def changeRole(role):
    access = 0
    if role == "NURSE":
        access = 2
    elif role == "DOCTOR":
        access = 3
    elif role == "ADMIN":
        access = 4
    return access


def getValid_patient(username, password):
    result = getPatientInfoWithLoginDetails(username)
    if result:
        user_cred = [lis for lis in result[0]]
        if user_cred[1] == password:
            return True, user_cred
        else:
            return False, []
    else:
        return False, []


def formatphone(phone):
    str_len = len(phone.strip())
    if str_len == 10:
        phone = phone[0:3] + '-' + phone[3:6] + '-' + phone[6:10]
    return phone

def clean_unconfirmedList(results):
    new_list = []

    for i in range(0, len(results)):
        if results[i][5] == None:
            new_list.append(list(results[i]))

    return new_list


def user_appointment(results):
    print(results)
    if results[3]==None:
        results.append("Pending")
    elif len(results) == 4:
        results.append("Confirmed")
    return results
