import mysql.connector

try:
    mydb = mysql.connector.connect(
      host="13.235.17.41",
      user="sumuk",
      password="sumuk", 
      database='testdb'
    )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
print(mydb)


mycursor = mydb.cursor()


mycursor.execute("DROP TABLE customers")
mycursor.execute("SHOW TABLES")


for x in mycursor:
  print(x)