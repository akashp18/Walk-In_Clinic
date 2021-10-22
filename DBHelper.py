"""########################################################
Author:
Student ID:
Due Date:
========================================================
File contains:

##########################################################"""

import sqlite3
from datetime import timedelta, date
import re
from datetime import datetime
DB_NAME = "Walk In_Clinic_New.db"
connection = any


def dbConnect():
    global connection
    connection = sqlite3.connect(DB_NAME)


def dbClose():
    global connection
    connection.close()


def insertPatient(f_Name, l_Name, gender, phone, email, dob, healthCard, street, city, zipCode, province, user_id):
    dbConnect()
    cursor = connection.cursor()
    str_query = "INSERT INTO TB_PATIENT (EMAIL_ADDRESS,FIRST_NAME, LAST_NAME,BIRTHDATE,HEALTHCARE_NUMBER,GENDER,PHONE,STREET,CITY,PROVINCE,ZIPCODE,user_id) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');"
    insertQuery = str_query.format(email, f_Name, l_Name, dob, healthCard, gender, phone, street, city, province,
                                   zipCode, user_id)
    cursor.execute(insertQuery)
    cursor.execute("COMMIT;")
    cursor.close()
    dbClose()


def insertUSER(userAccessID, userName, password, account_status):
    dbConnect()
    cursor = connection.cursor()
    str_query = "INSERT INTO TB_USER (USER_ACCESS_ID,USER_NAME, PASSWORD,ACCOUNT_STATUS) VALUES ('{}','{}','{}','{}');"
    insertQuery = str_query.format(userAccessID, userName, password, account_status)
    cursor.execute(insertQuery)
    cursor.execute("COMMIT;")
    last_inserted_userID = cursor.lastrowid
    cursor.close()
    dbClose()
    return last_inserted_userID


def appointment_listByDoctorID(doctor_ID):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "select APT.APPOINTMENT_ID,TP.LAST_NAME || ' ' ||  TP.FIRST_NAME AS Fullname ,cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', TP.BIRTHDATE) as int) AS AGE,APT.APPOINTMENT_TYPE,APT.APPOINTMENT_DATE,APT.APPOINTMENT_TIME from TB_APPOINTMENT APT JOIN TB_PATIENT TP ON APT.PATIENT_ID=TP.USER_ID where APT.DOCTOR_ID = {} ORDER by APT.APPOINTMENT_DATE DESC, APT.APPOINTMENT_TIME LIMIT 5".format(
        doctor_ID)
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def getPatient_info(appointment_ID):
    dbConnect()
    results = []
    is_digit = appointment_ID.isdigit()
    if is_digit:
        cursor = connection.cursor()

        selectQuery = "select FIRST_NAME, LAST_NAME, BIRTHDATE, HEALTHCARE_NUMBER, FAMILY_DOCTOR, APPOINTMENT_TYPE, SYMPTOMS  " \
                      "from TB_PATIENT TP LEFT JOIN TB_APPOINTMENT APT ON TP.USER_ID = APT.PATIENT_ID where " \
                      "APT.APPOINTMENT_ID = {}".format(appointment_ID)
        cursor.execute(selectQuery)
        results = cursor.fetchall()
        cursor.close()
        dbClose()
    return results


def getStaffInfoWithLoginDetails(userName, level):
    dbConnect()
    cursor = connection.cursor()
    if level == 3:
        selectQuery = "SELECT USER_ACCESS_ID,PASSWORD,ACCOUNT_STATUS, SF.* FROM TB_USER US LEFT JOIN TB_DOCTOR SF ON SF.DOCTOR_ID = US.USER_ID WHERE USER_NAME = '{}' limit 1;".format(
            userName)
    else:
        selectQuery = "SELECT USER_ACCESS_ID,PASSWORD,ACCOUNT_STATUS, SF.* FROM TB_USER US LEFT JOIN TB_STAFF SF ON SF.USER_ID = US.USER_ID WHERE USER_NAME = '{}' limit 1;".format(
            userName)
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def getPatientInfoWithLoginDetails(userName):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "SELECT USER_ACCESS_ID,PASSWORD,ACCOUNT_STATUS, PT.* FROM TB_USER US LEFT JOIN TB_PATIENT PT ON PT.USER_ID = US.USER_ID WHERE USER_NAME = '{}' limit 1;".format(
        userName)
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def appointment_listByDoctorID(doctor_ID):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "select APT.APPOINTMENT_ID,TP.LAST_NAME || ' ' ||  TP.FIRST_NAME AS Fullname ,cast(strftime('%Y-%m-%d', 'now') - strftime('%Y-%m-%d', TP.BIRTHDATE) as int) " \
                  "AS AGE,APT.APPOINTMENT_TYPE,APT.APPOINTMENT_DATE,APT.APPOINTMENT_TIME from TB_APPOINTMENT APT JOIN TB_PATIENT TP ON APT.PATIENT_ID=TP.USER_ID where APT.DOCTOR_ID = {} " \
                  "and APT.APPOINTMENT_DATE >= strftime('%Y-%m-%d', 'now')  ORDER by APT.APPOINTMENT_DATE ASC, APT.APPOINTMENT_TIME ".format(
        doctor_ID)
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def getpatient_appointment_history(appointment_ID):
    dbConnect()
    results = []
    print(appointment_ID)
    is_digit = appointment_ID.isdigit()
    if is_digit:
        cursor = connection.cursor()
        selectQuery = "select FIRST_NAME,LAST_NAME,BIRTHDATE,HEALTHCARE_NUMBER, APT.APPOINTMENT_ID, " \
                      "APT.APPOINTMENT_DATE,APT.APPOINTMENT_TIME,APT.APPOINTMENT_TYPE,DOCTOR_NOTE, PS.name AS " \
                      "Medicine from TB_PATIENT TP LEFT JOIN TB_APPOINTMENT APT ON TP.USER_ID=APT.PATIENT_ID LEFT " \
                      "JOIN TB_PRESCRIPTION PS ON APT.APPOINTMENT_ID=PS.APPOINTMENT_ID where APT.APPOINTMENT_ID = {" \
                      "}".format(
            appointment_ID)
        cursor.execute(selectQuery)
        results = cursor.fetchall()
        cursor.close()

    dbClose()
    return results


def appointment_lis():
    dbConnect()
    cursor = connection.cursor()

    selectQuery ="select APT.APPOINTMENT_ID,TP.LAST_NAME || ' ' ||  TP.FIRST_NAME AS Fullname ,TD.LAST_NAME || ' ' || TD.FIRST_NAME AS DOCTOR_NAME ,APT.APPOINTMENT_TYPE,APT.APPOINTMENT_DATE,APT.APPOINTMENT_TIME from TB_APPOINTMENT APT JOIN TB_PATIENT TP ON APT.PATIENT_ID=TP.USER_ID JOIN TB_DOCTOR TD ON APT.DOCTOR_ID=TD.DOCTOR_ID and APT.APPOINTMENT_DATE >= strftime('%Y-%m-%d', 'now') ORDER by APT.APPOINTMENT_DATE ASC"

    cursor.execute(selectQuery)
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def unconfirmed_appointment_lis():
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "Select APT.APPOINTMENT_ID,TP.LAST_NAME || ' ' ||  TP.FIRST_NAME AS Fullname ,APT.APPOINTMENT_TYPE,APT.APPOINTMENT_DATE,APT.APPOINTMENT_TIME,APT.DOCTOR_ID  from TB_APPOINTMENT APT JOIN TB_PATIENT TP ON APT.PATIENT_ID=TP.USER_ID  ORDER by APT.APPOINTMENT_DATE ASC"
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def create_appointment(patient_id, appointment_date, appointment_time, appointment_type, symptoms,
                       family_doctor):
    dbConnect()
    cursor = connection.cursor()

    appointment_date = appointment_date[5:7]+'/'+appointment_date[8:11]+'/'+appointment_date[0:4]

    str_query = "INSERT INTO TB_APPOINTMENT(PATIENT_ID,APPOINTMENT_DATE,APPOINTMENT_TIME, APPOINTMENT_TYPE, SYMPTOMS,FAMILY_DOCTOR)VALUES({},'{}','{}','{}','{}','{}');"
    insertQuery = str_query.format(patient_id, appointment_date, appointment_time, appointment_type, symptoms,
                                   family_doctor)
    print(insertQuery)
    cursor.execute(insertQuery)
    connection.commit()
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def check_appointment(patient_id):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "select TA.appointment_date,TA.APPOINTMENT_TIME,TA.APPOINTMENT_TYPE, PA.LAST_NAME || ' ' ||  PA.FIRST_NAME AS Fullname from TB_APPOINTMENT TA LEFT JOIN " \
                  "TB_DOCTOR PA on TA.DOCTOR_ID = PA.DOCTOR_ID where TA.PATIENT_ID = {} Order by cast(" \
                  "TA.appointment_date as date)," \
                  "TA.APPOINTMENT_TIME DESC".format(
        patient_id)
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def get_billing_info(patient_id):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "select  TA.appointment_date, TA.APPOINTMENT_TIME, TA.APPOINTMENT_TYPE, BIL.cost from TB_BILLING BIL " \
                  "JOIN TB_APPOINTMENT TA ON BIL.APPOINTMENT_ID = TA.APPOINTMENT_ID JOIN TB_PATIENT PA on " \
                  "TA.PATIENT_ID = PA.USER_ID where TA.PATIENT_ID = {} Order by TA.appointment_date, " \
                  "TA.APPOINTMENT_TIME".format(patient_id)
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def update_appointment(appointment_id, nurse_id, doctor_id):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "UPDATE TB_APPOINTMENT SET DOCTOR_ID = {}, NURSE_ID = {} WHERE APPOINTMENT_ID = {}".format(doctor_id,
                                                                                                             nurse_id,
                                                                                                             appointment_id)
    cursor.execute(selectQuery)
    connection.commit()
    # results = cursor.fetchall()
    cursor.close()
    dbClose()
    return


def add_bill(appointment_id, patient_id, nurse_id, cost):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "INSERT INTO TB_BILLING(APPOINTMENT_ID,PATIENT_ID,NURSE_ID,COST) VALUES({},{},{},{})".format(
        appointment_id, patient_id, nurse_id, cost)
    cursor.execute(selectQuery)
    connection.commit()
    # results = cursor.fetchall()
    cursor.close()
    dbClose()
    return


# problem
def add_prescriton_per_appointment(name, num_pills, Frequency, special_instruction, expr_date, filled,
                                   appointment_id):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "INSERT INTO TB_PRESCRIPTION(NAME,NUMBER_OF_PILLS,FREQUENCY,SPECIAL_INSTRUCTION," \
                  "EXPIRATION_DATE,DATE_FILLED,APPOINTMENT_ID)VALUES('{}',{},'{}','{}',{},{},{})".format(name,
                                                                                                         num_pills,
                                                                                                         Frequency,
                                                                                                         special_instruction,
                                                                                                         expr_date,
                                                                                                         filled,
                                                                                                         appointment_id)
    cursor.execute(selectQuery)
    connection.commit()
    # results = cursor.fetchall()
    cursor.close()
    dbClose()
    return


def update_doctorNote(appointment_id, doctor_notes):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "UPDATE TB_APPOINTMENT SET DOCTOR_NOTE ='{}'  where appointment_ID = {}".format(doctor_notes,
                                                                                                  appointment_id)
    cursor.execute(selectQuery)
    connection.commit()
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def getPatientInfo(user_id):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "SELECT * FROM TB_PATIENT WHERE USER_ID = '{}' limit 1;".format(user_id)
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def deletePatient(user_id):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "DELETE FROM TB_PATIENT WHERE USER_ID = '{}';".format(user_id)
    cursor.execute(selectQuery)
    connection.commit()
    selectQuery = "DELETE FROM TB_USER WHERE USER_ID = '{}';".format(user_id)
    cursor.execute(selectQuery)
    connection.commit()
    cursor.fetchall()
    cursor.close()
    dbClose()
    return


def getStaffInfo(user_id):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "SELECT * FROM TB_STAFF WHERE USER_ID = '{}' limit 1;".format(user_id)
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def getDoctorInfo(user_id):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "SELECT * FROM TB_DOCTOR WHERE DOCTOR_ID = '{}' limit 1;".format(user_id)
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    cursor.close()
    dbClose()
    return results


def deleteDoctor(user_id):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "DELETE FROM TB_DOCTOR WHERE DOCTOR_ID = '{}';".format(user_id)
    cursor.execute(selectQuery)
    connection.commit()
    selectQuery = "DELETE FROM TB_USER WHERE USER_ID = '{}';".format(user_id)
    cursor.execute(selectQuery)
    connection.commit()
    cursor.fetchall()
    cursor.close()
    dbClose()
    return


def deleteStaff(user_id):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "DELETE FROM TB_STAFF WHERE USER_ID = '{}';".format(user_id)
    cursor.execute(selectQuery)
    connection.commit()
    selectQuery = "DELETE FROM TB_USER WHERE USER_ID = '{}';".format(user_id)
    cursor.execute(selectQuery)
    connection.commit()
    cursor.fetchall()
    cursor.close()
    dbClose()
    return


def insertDoctor(pid, fname, lname, dob, gender, email, phone, street, city, province, zipcode, spec):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "INSERT INTO TB_DOCTOR(DOCTOR_ID,FIRST_NAME,LAST_NAME,BIRTHDATE," \
                  "GENDER,EMAIL_ADDRESS,PHONE,STREET,CITY,PROVINCE,ZIPCODE," \
                  "SPECIALITY)VALUES({},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}');".format(pid, fname, lname, dob,
                                                                                                 gender, email, phone,
                                                                                                 street, city, province,
                                                                                                 zipcode, spec)
    cursor.execute(selectQuery)
    connection.commit()

    cursor.fetchall()
    cursor.close()
    dbClose()


def insertStaff(pid, fname, lname, dob, gender, email, phone, street, city, province, zipcode):
    dbConnect()
    cursor = connection.cursor()
    selectQuery = "INSERT INTO TB_STAFF(FIRST_NAME,LAST_NAME,BIRTHDATE," \
                  "GENDER,EMAIL_ADDRESS,PHONE,STREET,CITY,PROVINCE,ZIPCODE," \
                  "USER_ID)VALUES('{}','{}',{},'{}','{}','{}','{}','{}','{}','{}',{});".format(fname, lname, dob,
                                                                                                 gender, email, phone,
                                                                                                 street, city, province,
                                                                                                 zipcode, pid)
    cursor.execute(selectQuery)
    connection.commit()

    cursor.fetchall()
    cursor.close()
    dbClose()

