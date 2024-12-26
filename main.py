import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="Jana Halienova",
  password="mydb123"
)

print(mydb)