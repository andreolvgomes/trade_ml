#https://github.com/mkleehammer/pyodbc
#https://github.com/mkleehammer/pyodbc/wiki
#https://www.mql5.com/pt/articles/2895

import pyodbc

cnn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-LIF7QU6\SQLEXPRESS;DATABASE=test;UID=sa;PWD=2020')
cursor = cnn.cursor()

cursor.execute('select * from DemoTest')
row = cursor.fetchone()
id = row[0]
str = row[1]

