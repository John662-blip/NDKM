import pyodbc
cnxn = pyodbc.connect('DRIVER={SQL Server};Server=ABC;Database=LTPT')
cursor = cnxn.cursor()
class Users:
    def __init__(self) :
        pass
    def DeleteUser(self,id):
        # SQL query for deleting the user
        sql_query = f"DELETE FROM Users WHERE id = {id}"
        try:
            # Execute the delete query
            cursor.execute(sql_query)
            # Commit the transaction
            cursor.commit()
            return True
        except:
            return False
    def DuyetUser(self,id):
        sql_query = f"""UPDATE Users 
                       SET action = 1 
                       WHERE id = {id}"""
        try:
            cursor.execute(sql_query)
            cursor.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def load(self):
        sql_query = f"""SELECT 
                        id, 
                        fname, 
                        lname, 
                        address, 
                        CASE 
                            WHEN type = 1 THEN 'Student' 
                            WHEN type = 0 THEN 'Teacher' 
                            WHEN type = 2 THEN 'Admin' 
                            ELSE 'Unknown' -- thêm trường hợp này nếu có giá trị khác ngoài 0, 1, 2
                        END as type
                    FROM 
                        Users
                    WHERE 
                        action = 0;
                    """
        cursor.execute(sql_query)
        myResult = cursor.fetchall()
        return myResult
        
class Statistics:
    def __init__(self):
        pass
    def load(self,teacher_id):
        sql_query = "SELECT Users.fname, Users.lname, FORMAT(diem_danh.date_check, 'yyyy-MM-dd HH:mm:ss') as date_check, diem_danh.course_id FROM diem_danh JOIN Users ON Users.id = diem_danh.id join Course on Course.id = diem_danh.course_id where teacher_id =" + str(teacher_id)
        cursor.execute(sql_query)
        myResult = cursor.fetchall()
        return myResult
    def loadCourse(self,teacher_id):
        sql_query = "SELECT course_name,id FROM course Where teacher_id = " + str(teacher_id)
        cursor.execute(sql_query)
        myResult = cursor.fetchall()
        return myResult
    def loadCouseForStd(self,id):
        sql_query = f"""SELECT 
                c.id, 
                c.course_name,
                c.decription,
                CASE 
                    WHEN e.student_id IS NOT NULL THEN 1
                    ELSE 0
                END AS registration_status
                FROM 
                Course c
                LEFT JOIN 
                Enrolls e ON c.id = e.course_id AND e.student_id = {str(id)}
                """
        cursor.execute(sql_query)
        myResult = cursor.fetchall()
        return myResult
    def enrollCourse(self, course_id, student_id ):
        sql_query1=f"select * from Enrolls where course_id = {course_id} and student_id = {student_id}"
        cursor.execute(sql_query1)
        myResult = cursor.fetchall()
        if (len(myResult)!=0):
            return False
        sql_query = "INSERT INTO enrolls VALUES (?, ?)"
        try:
            cursor.execute(sql_query, (course_id, student_id))
            cnxn.commit()
            return True
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")
            return False
    def load_students(self, course_id):
        sql_query = f"""
        SELECT 
            Users.fname, 
            Users.lname, 
            FORMAT(diem_danh.date_check, 'yyyy-MM-dd HH:mm:ss') as date_check, 
            Enrolls.course_id,
            CASE 
                WHEN diem_danh.id IS NOT NULL THEN 1
                ELSE 0
            END AS [check]
        FROM 
            Users
        JOIN 
            Enrolls ON Users.id = Enrolls.student_id
        LEFT JOIN 
            diem_danh ON Users.id = diem_danh.id AND diem_danh.course_id = {course_id} AND FORMAT(diem_danh.date_check, 'yyyy-MM-dd') = CONVERT(date, GETDATE())
        WHERE 
            Enrolls.course_id = {course_id}
        """
        cursor.execute(sql_query)
        myResult = cursor.fetchall()
        return myResult




