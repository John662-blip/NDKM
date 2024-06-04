# import sys
# import os

# Add the parent directory to sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from connectdb import connect_db

# Establish a database connection


# Insert Course 
def insert_course(db_cursor, course_name, decription, teacher_id):
    sql = """INSERT INTO Course(course_name, decription, teacher_id)
             VALUES (?, ?, ?)"""
    db_cursor.execute(sql, (course_name, decription, teacher_id))
    db_cursor.connection.commit()

def checkName(db_cursor, course_name):
    sql = f"""Select * from Course where course_name like N'{course_name}'"""
    db_cursor.execute(sql)
    myResult = db_cursor.fetchall()
    if (len(myResult)!=0) :
        return True
    return False
#Update Course 
def update_course(db_cursor, id,  course_name, description, teacher_id):
    sql = """UPDATE Course SET course_name=?, description = ?, teacher_id = ?  WHERE id = ? """
             
    db_cursor.execute(sql, (course_name, description, teacher_id, id))
    db_cursor.connection.commit()

#Delete Course
def delete_course(db_cursor, id):
    sql = """DELETE FROM Course WHERE id = ?"""
    db_cursor.execute(sql, (id,))
    db_cursor.connection.commit()
