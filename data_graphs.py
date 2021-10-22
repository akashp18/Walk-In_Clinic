import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def graph1():
    connection = sqlite3.connect("Walk In_Clinic_New.db")
    sql_query = pd.read_sql_query('''SELECT APPOINTMENT_DATE  FROM TB_APPOINTMENT;''', connection)
    df = pd.DataFrame(sql_query)
    df['Year'] = pd.DatetimeIndex(df['APPOINTMENT_DATE']).year
    group_data = df.groupby(['Year']).count()
    df = pd.DataFrame(group_data)
    df['YEAR'] = df.index
    Year = df['YEAR'].values.tolist()
    Total = df['APPOINTMENT_DATE'].values.tolist()

    return Year, Total


def graph2():
    connection = sqlite3.connect("Walk In_Clinic_New.db")
    sql_query = pd.read_sql_query('''
                                    SELECT a.APPOINTMENT_DATE, b.COST  FROM TB_APPOINTMENT a 
                                    join TB_BILLING b on a.APPOINTMENT_ID = b.APPOINTMENT_ID ;
                                  ''', connection)

    df = pd.DataFrame(sql_query)
    df['Year'] = pd.DatetimeIndex(df['APPOINTMENT_DATE']).year

    group_data = df.groupby(['Year'])['COST'].sum()
    df = pd.DataFrame(group_data)
    df['YEAR'] = df.index

    w = 0.5
    Year = df['YEAR'].values.tolist()
    Amount = df['COST'].values.tolist()


    return Year, Amount


def graph3():
    connection = sqlite3.connect("Walk In_Clinic_New.db")
    sql_query = pd.read_sql_query('''
                                    SELECT APPOINTMENT_ID,APPOINTMENT_TYPE FROM TB_APPOINTMENT;
                                  ''', connection)

    df = pd.DataFrame(sql_query)
    group_data = df.groupby(['APPOINTMENT_TYPE']).count()
    df = pd.DataFrame(group_data)
    df.columns = ['Count']
    df['type'] = df.index
    type = df['type'].values.tolist()
    count = df['Count'].values.tolist()
    return type, count

