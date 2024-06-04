from flet import *
import flet as ft
from form.user import insert_user,TinhSoAdmin
from connectdb import cursor as connect_db
import os
import shutil
import cv2
from form.settings import *
from form.service.face.Train import training
path = PATH_DATASET
recognizer = cv2.face.LBPHFaceRecognizer.create()
face_detector = cv2.CascadeClassifier(PATH_XML)
class Main:
        #image
    def __init__(self,page,id):
        self.page  = page
        self.id = id
        self.type = 0
        def exit(e):
            from form.form_main import Main as Mai1
            self.page.clean()
            self.exit()
            Mai1(self.page).run()
            self.page.update() 
            
        def close_dlg(e):
            self.dlg_modal.open = False
            page.update()
        def close_dlg1(e):
            self.dlg_modal1.open = False
            page.update()
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Thông báo"),
            content=ft.Text("Thêm Thành công"),
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss= exit)
        self.dlg_modal1 = ft.AlertDialog(
            modal=True,
            title=ft.Text("Lỗi"),
            content=ft.Text("Có lỗi xãy ra?"),
            actions=[
                ft.TextButton("OK", on_click=close_dlg1),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
           )
        
        #Button Login
        def on_login_clicked(e):
            try:
                if (int(self.type) ==2):
                    sl = TinhSoAdmin(connect_db)
                    if (sl==0):
                        insert_user(connect_db, id_field.value, first_name_field.value, last_name_field.value, phone_field.value, address_field.value, 2,1)
                        for filename in os.listdir(f"form/service/face/twp/{id_field.value}"):
                            source_file_path = os.path.join(f"form/service/face/twp/{id_field.value}", filename)
                            if os.path.isfile(source_file_path):
                                destination_file_path = os.path.join("form/service/face/dataSet", filename)
                                shutil.move(source_file_path, destination_file_path)
                        if not os.listdir(f"form/service/face/twp/{id_field.value}"):  # Kiểm tra xem thư mục có trống không
                            os.rmdir(f"form/service/face/twp/{id_field.value}")#xóa
                        training()
                    else:
                        insert_user(connect_db, id_field.value, first_name_field.value, last_name_field.value, phone_field.value, address_field.value, 2,0)
                else:
                    insert_user(connect_db, id_field.value, first_name_field.value, last_name_field.value, phone_field.value, address_field.value, self.type,0)
                page.dialog = self.dlg_modal
                self.dlg_modal.open = True
                page.update()
            except Exception as e:
                error_message = f"Có lỗi xảy ra: {str(e)}"
                self.dlg_modal1.content = ft.Text(error_message)
                self.page.dialog = self.dlg_modal1
                self.dlg_modal1.open = True
            finally:
                self.page.update()
        #Button Cancel
        def on_cancel_clicked(e):
            from form.form_main import Main as Mai1
            self.page.clean()
            self.exit()
            Mai1(self.page).run()
            self.page.update() 


        def radio_changed(e):
            self.type = e.control.value  # Update the type based on the radio button's value
            self.page.update()


        # Define textBox
        id_field = TextField(text_style=TextStyle(color="#000000"), border_radius=15, border_color=colors.BLACK, focused_border_color=colors.ORANGE_700,value=self.id,read_only=True)
        first_name_field = TextField(text_style=TextStyle(color="#000000"), width=200, border_radius=15, border_color=colors.BLACK, focused_border_color=colors.ORANGE_700)
        last_name_field = TextField(text_style=TextStyle(color="#000000"), width=200, border_radius=15, border_color=colors.BLACK, focused_border_color=colors.ORANGE_700)
        phone_field = TextField(text_style=TextStyle(color="#000000"), border_radius=15, border_color=colors.BLACK, focused_border_color=colors.ORANGE_700)
        address_field = TextField(text_style=TextStyle(color="#000000"), border_radius=15, border_color=colors.BLACK, focused_border_color=colors.ORANGE_700)



        # Setup the initial value for self.type
        self.type = 0     # Default to Teacher, for example

        radio_group = ft.RadioGroup(
            value=self.type,  # Use self.type to set the initial value
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Radio(label="", value=0),  # Value for Teacher
                                ft.Text("Teacher", weight="bold", color="#000000")
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Radio(label="", value=1),  # Value for Student
                                ft.Text("Student", weight="bold", color="#000000")
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        margin=margin.only(left=50)  # Adjusted for clarity
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Radio(label="", value=2),  # Value for Admin
                                ft.Text("Admin", weight="bold", color="#000000")
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        margin=margin.only(left=50)  # Adjusted for clarity
                    ),
                ]
            ),
            on_change=radio_changed
        )


        #Design Button login
        login_button = ElevatedButton(
                "Register",
                width=200,
                height=70,
                style=ButtonStyle(
                    color="#ffffff",
                    bgcolor=colors.ORANGE_700,
                    shape={
                        MaterialState.FOCUSED: RoundedRectangleBorder(radius=5),
                        MaterialState.HOVERED: RoundedRectangleBorder(radius=5),
                    },
                    padding=20,
                ),
                on_click=on_login_clicked
                
        )
        

        #Design Button Cancel
        cancel_button = ElevatedButton(
            "Cancel",
            width=200,
            height=70,
            style=ButtonStyle(
                color="#ffffff",
                bgcolor=colors.RED_700,  # Changed color to differentiate
                shape={
                    MaterialState.FOCUSED: RoundedRectangleBorder(radius=5),
                    MaterialState.HOVERED: RoundedRectangleBorder(radius=5),
                },
                padding=20,
            ),
            on_click=on_cancel_clicked
        )


        register_page = Container(
            width= 600,
            bgcolor="#ffffff",
            border_radius=10,
            content=Column(
                width=320,
                controls=[
                   Column(
                       controls=[
                    Container(
                        margin=margin.only(left=10, right=10, top=10),
                        content=Text("ĐĂNG KÍ THÔNG TIN", size=30, color="#000000", weight="w800")
                    ),
                    Container(
                        width=200,
                        margin=margin.only(left=20, right=20, top=10),
                        content=Column(
                            controls=[
                                Text("ID", size=20, color="#000000", weight="w500"),
                                id_field
                            ]
                        )
                    ),
                    Container(
        
                        margin=margin.only(left=20, right=20, top=10),
                        content=Row(
                            controls=[
                                Container(
                                    content=Column(
                                        controls=[
                                            Text("First Name", size=20, color="#000000", weight="w500",width=300),
                                        first_name_field
                                        ]
                                    ),
                                ),
                                Container(
                                    content=Column(
                                        controls=[
                                            Text("Last Name", size=20, color="#000000", weight="w500",width=300),
                                            last_name_field
                                        ]
                                    )
                                )
                            ]
                        )
                    ),
                    Container(
                        width=500,
                        margin=margin.only(left=20, right=20, top=10),
                        content=Column(
                            controls=[
                                Text("Phone", size=20, color="#000000", weight="w500"),
                                phone_field
                            ]
                        )
                    ),
                    Container(
                        width=500,
                        margin=margin.only(left=20, right=20, top=10),
                        content=Column(
                            controls=[
                                Text("Address", size=20, color="#000000", weight="w500"),
                                address_field
                            ]
                        )
                    ),
                    Container(
                        margin = margin.only(left = 20, right = 20, top = 10),
                        content = Column(
                            controls = [
                               Text("Select Teacher Or Student", size = 20, color="#000000", weight = "w500"),
                               radio_group
                            ]
                        )
                    ),
                    Container(
                        margin = margin.only(left=70, right=20, top=20),
                        padding = padding.only(bottom=20),
                        content = Row(
                            controls=[
                                Container(content=login_button,
                                        margin=margin.only(right=30), width= 200
                                ),
                                
                                Container(content=cancel_button, width = 200)
                            ]
                        )
                    ),
                   

                       ]
                   )
                ]
            ),
        )
        self.body = Container(
            # margin = margin.only(left=500),
            content=Row(
                controls=[register_page],
                alignment=MainAxisAlignment.SPACE_EVENLY,
            )
        )
    def run(self):
        self.page.add(self.body)
    def exit(self):
        pass

# app(target=main)