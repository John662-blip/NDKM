# import sys
# import os

# Add the parent directory to sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from connectdb import connect_db

# Establish a database connection
from flet import *

def TinhSoAdmin(db_cursor):
    sql_query =f"Select * from Users where type = 2"
    db_cursor.execute(sql_query)
    myResult = db_cursor.fetchall()
    return len(myResult)
def insert_user(db_cursor, id, fname, lname, phone, address, type,action):
    sql = """INSERT INTO Users(id, fname, lname, sdt, address, type,action)
             VALUES (?, ?, ?, ?, ?, ?,?)"""
    db_cursor.execute(sql, (id, fname, lname, phone, address, type,action))
    db_cursor.connection.commit()

def DiemDanh(db_cursor, id, course_id):
    # kiểm tra điểm danh chưa
    sql_query = f"""SELECT * FROM diem_danh WHERE id = {id} AND course_id = {course_id} AND CONVERT(date, date_check) = CONVERT(date, getdate())"""
    db_cursor.execute(sql_query)
    myResult = db_cursor.fetchall()
    if len(myResult) > 0:
        return 1
    # kiểm tra xem có học lớp này không
    sql_query2 = f"""SELECT * FROM Enrolls WHERE student_id = {id} AND course_id = {course_id}"""
    db_cursor.execute(sql_query2)
    myResult2 = db_cursor.fetchall()
    if len(myResult2) == 0:
        return 2
    else:
        sql = """INSERT INTO diem_danh(id, course_id)
                VALUES (?, ?)"""
        db_cursor.execute(sql, (id, course_id))
        db_cursor.connection.commit()
        return 0

def TimKiemUser(db_cursor,id):
    sql_query =f"Select * from Users where id = {int(id)}"
    db_cursor.execute(sql_query)
    myResult = db_cursor.fetchall()
    if len(myResult)>0:
        type = myResult[0][5]
        return type
    return None

def update_user(db_cursor, id, fname, lname, phone, address):
    sql = """UPDATE Users SET fname=?, lname = ?, sdt = ?, address = ? WHERE id = ? """
             
    db_cursor.execute(sql, (fname, lname, phone, address, id))
    db_cursor.connection.commit()
