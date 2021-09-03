import mysql.connector

mydb = mysql.connector.connect(
        host='localhost', 
        user='root',
        password='root')

mycursor = mydb.cursor()


db2 = mysql.connector.connect(
        host='localhost', 
        user='root',
        password='root',
        database='testdb')
    
cursor2 = db2.cursor()




def showdbs():
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        print(x)


def create_test_db():
    mycursor.execute("CREATE DATABASE testdb")



def create_auth_table():
    cursor2.execute("CREATE TABLE auth (id VARCHAR(255), username VARCHAR(255), password VARCHAR(255), email VARCHAR(255));")


def showtables():
    cursor2.execute("SHOW TABLES")
    for x in cursor2:
          print(x)
    




try:
    create_test_db()
except:
    print("Creation Error")
try:
    showdbs()
except:

    print("Show Error")
try:
    create_auth_table()
except:
    
    print("Creation Table Error")
try:
    showtables()
except:
   print("cant show") 
