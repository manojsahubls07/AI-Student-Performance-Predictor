import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manoj",
    database="student_prediction"
)

print("Database Connected Successfully")