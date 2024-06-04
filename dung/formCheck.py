from flet import *
import threading
import base64
import time
from form.settings import *
from connectdb import Statistics,cursor
from form.user import DiemDanh
from dung.mytoast import Toast
import cv2
cascadePath = PATH_XML
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
column_names : list[str] = [
    "Họ","Tên", "Ngày điểm danh", "Id_Môn", "Trạng Thái"
]

data_table_style: dict[str,any] = {
    "expand": True,
    "border_radius": 8,
    "border": border.all(2,"#ebebeb"),
    "horizontal_lines": border.BorderSide(1,"#ebebeb"),
    "columns": [
        DataColumn(Text(index, size=12, color="black", weight="bold"))
        for index in column_names
    ]
}
class DataTable(DataTable):
    def __init__(self) -> None:
        super().__init__(**data_table_style)

    def fill_data_table(self) -> None:
        self.rows = []

        for values in self.dt.values():
            data = DataRow()
            data.cells = [
                DataCell(
                    Text(value, color="black")
                ) for value in values.values()
            ]
            self.rows.append(data)
        self.update()
class Main:
    def __init__(self,page,teacher_id):
        self.teacher_id = teacher_id
        from form.form_main import Main as Main1
        self.Main1 = Main1
        self.CanCheck = False
        self.start =False
        self.recognizer = cv2.face.LBPHFaceRecognizer.create()
        self.recognizer.read(PATH_TRAINER)
        self.page=page
        self.cap = cv2.VideoCapture(0)
        #datatableCourse
        stats = Statistics()  # Initialize the Statistics object
        data_from_db = stats.loadCourse(self.teacher_id)
        self.table = DataTable()
        self.table.dt = {i: {'name': row[0],'id' : row[1]}  for i, row in enumerate(data_from_db)}

        #datatableStudent
        self.table2 = DataTable()
        self.image_Box = Image(
            width= 500,
            height= 400,
            src_base64="///Z",
            expand=False,
        ) 
        def close_dlg(e):
            self.dlg_modal.open = False
            page.update()
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Thông báo"),
            content=Text("Điểm Danh Thành Công"),
            actions=[
                TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=MainAxisAlignment.END
            )
        def close_dlg2(e):
            self.dlg_modal2.open = False
            page.update()
        self.dlg_modal2 = AlertDialog(
            modal=True,
            title=Text("Thông báo"),
            content=Text("Vui lòng chọn môn học"),
            actions=[
                TextButton("OK", on_click=close_dlg2),
            ],
            actions_alignment=MainAxisAlignment.END
            )
        def close_dlg3(e):
            self.dlg_modal3.open = False
            page.update()
        self.dlg_modal3 = AlertDialog(
            modal=True,
            title=Text("Thông báo"),
            content=Text("Học sinh không thuộc lớp này."),
            actions=[
                TextButton("OK", on_click=close_dlg3),
            ],
            actions_alignment=MainAxisAlignment.END
            )
        def close_dlg4(e):
            self.dlg_modal4.open = False
            page.update()
        self.dlg_modal4 = AlertDialog(
            modal=True,
            title=Text("Thông báo"),
            content=Text("Học sinh đã điểm danh rồi."),
            actions=[
                TextButton("OK", on_click=close_dlg4),
            ],
            actions_alignment=MainAxisAlignment.END
            )
        self.update_image_thread = threading.Thread(target=self.update_image)
        self.update_image_thread.daemon = True
        self.update_image_thread.start()
        self.course_data = [(row['name'], row['id']) for row in self.table.dt.values()]
        self.cbxSelectCourse = Dropdown(
            filled= True,
            label="Môn Học",
            hint_text="Chọn",
            options=[dropdown.Option(text=name,key=id) for name,id in self.course_data],
            width=200,
            bgcolor="#5AB2FF",
            color="#EEF7FF",
            on_change=lambda e:self.ThayDoi()
        )
        self.btn = ElevatedButton(content=Text("Điểm danh"),height=30,bgcolor="#0E46A3",color="#EEF7FF",on_click=lambda e:self.clickSubmit())
        self.btn1 = ElevatedButton(content=Text("Điểm danh"),height=30,bgcolor="#0E46A3",color="#EEF7FF")
        self.first_page = Container(
            expand=True,
            border_radius=20,
            bgcolor=BG,
            content=Column(
                # alignment=MainAxisAlignment.CENTER,
                controls=[
                    Container(
                        expand=True,
                        alignment=alignment.Alignment(0,1),
                        content=Column(
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            # horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Container(
                                    # alignment=alignment.Alignment(0,1),
                                    content=Row(
                                        alignment=MainAxisAlignment.SPACE_AROUND,
                                        controls=[
                                            ElevatedButton(content=Text("Quay lại",color='white'),height=30,bgcolor="black",on_click=lambda e:self.clickBack()),
                                            Container(width= 300+400+150),
                                            Container(
                                                    content = self.cbxSelectCourse
                                                ),
                                        ],
                                    ),
                                ),
                                Container(
                                    margin=Margin(0,10,0,0),
                                    content=  Row(
                                        alignment=MainAxisAlignment.SPACE_EVENLY,
                                        controls=[
                                            
                                            Container(
                                                # expand=True,
                                                # alignment=alignment.Alignment(0,0),
                                                
                                                content=Container(
                                                    border_radius=185,
                                                    content=self.image_Box
                                                ) 
                                            ),
                                            Container(
                                                content=
                                                Column(
                                                    height=250,
                                                    width=600,
                                                    scroll=True,
                                                    expand=True,
                                                    controls=[Row(controls=[self.table2])]
                                                )
                                            ),
                                        ]
                                    )
                                ),
                               
                                Container(
                                    margin = Margin(0,0,0,0),
                                    alignment=alignment.Alignment(0,0),
                                    content = self.btn
                                ),
                            ]
                        )
                    ),    
                ]
            )
        )
    def load_students(self):
            """Load danh sách học sinh đã đăng ký môn học."""
            # Truy vấn cơ sở dữ liệu để lấy danh sách học sinh
            stats = Statistics()  # Initialize the Statistics object
            data_from_db = stats.load_students(self.course_id)

            # Cập nhật self.table2.dt
            self.table2.dt = {i: {'fname': row[0], 'lname': row[1], 'date check': row[2], 'course_id': row[3], "Trạng Thái" : "Đã Điểm Danh" if (row[4]==1) else " Chưa Điểm Danh" } for i, row in enumerate(data_from_db)}

            # Cập nhật datatable
            self.table2.fill_data_table()
    def callDB(self):
        self.update_image_thread = threading.Thread(target=self.update_image)
        self.update_image_thread.daemon = True
        self.update_image_thread.start()
    def Recognize(self,img):
        check = False
        ima = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        equalized_image = cv2.equalizeHist(ima)

        # Áp dụng bộ lọc Gaussian để làm mờ ảnh
        col = cv2.GaussianBlur(equalized_image, (5, 5), 0)    
        faces = faceCascade.detectMultiScale(
            col,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            id,confidence = self.recognizer.predict(col[y:y+h,x:x+w])
            if (confidence<conF):
                confidence = "  {0}".format(round(100-confidence))
                check = True
                cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
                if (self.CanCheck):
                    try:
                        try:
                            tmp = DiemDanh(cursor,id,self.course_id)
                            if(tmp == 0):
                                self.load_students()
                                self.toast.changeDest( f"ID : {id} đã điểm danh thành công")
                                self.toast.show()
                        except Exception as e:
                           print(e)
                           pass
                        # self.page.clean()
                        # self.exit()
                        # self.Main1(self.page).run()
                        # self.page.update()
                    except:
                        pass
            else:
                id = "unknow"
                confidence = " {0}".format(round(100-confidence))
                cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
            cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(255,255,0),1)
        return img,check

    def update_image(self):
        while  self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret == True:
                frame = cv2.flip(frame,1)
                image,check = self.Recognize(frame)
                _, buffer = cv2.imencode('.jpg', image)
                b64_string = base64.b64encode(buffer).decode('utf-8')
                if (self.image_Box):
                    self.image_Box.src_base64 = b64_string
                self.page.update()
                
            else:
                break
            time.sleep(1/500)
    def clickBack(self):
        from form.Teacher_Student.mainForm_Teacher import Main as Form_Main
        self.page.clean()
        self.exit()
        Form_Main(self.page,self.teacher_id).run()
        self.page.update()
    def clickSubmit(self):
        if(self.cbxSelectCourse.value is None):
            self.page.dialog = self.dlg_modal2
            self.dlg_modal2.open = True
            self.page.update()
            return
        # Lấy course_id từ giá trị được chọn trong cbxSelectCourse
        self.course_id = self.cbxSelectCourse.value
        if not self.start:
            self.CanCheck = True
            self.start = True
            self.btn.content = Text("Đang Tìm Khuôn Mặt...")
            self.load_students()
    def ThayDoi(self):
        self.start = False
        self.CanCheck = False
        self.course_id = self.cbxSelectCourse.value
        self.btn.content = Text("Điểm Danh")
        self.load_students()  # Load danh sách học sinh khi thay đổi môn học
    def run(self):
        self.toast = Toast(
            self.page,
            icon=icons.INFO,
            msg_title="Thông báo",
            msg_desc="This is a toast message.",
            trigger=self.btn1,
            bgcolor=colors.GREEN,
            auto_close=1.5
        )
        main_stack = Stack(expand=True, controls=[])
        main_stack.controls.append(self.first_page)
        main_stack.controls.append(self.toast.struct())
        self.page.add(main_stack)
    def exit(self):
        if self.cap.isOpened():
            self.cap.release()
