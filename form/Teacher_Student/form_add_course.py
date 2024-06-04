from flet import *
import flet as ft
from form.user import insert_user
from form.Teacher_Student.course import insert_course,checkName
from connectdb import cursor as connect_db
from form.settings import *

class Main:
    def __init__(self, page, id):
        self.page = page
        self.id = id

        def exit(e):
            from form.Teacher_Student.mainForm_Teacher import Main as Main1
            self.page.clean()
            self.exit()
            Main1(self.page,self.id).run()
            self.page.update()

        def close_dlg(e):
            self.dlg_modal.open = False
            self.page.update()

        def close_dlg1(e):
            self.dlg_modal1.open = False
            self.page.update()

        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Thông báo"),
            content=ft.Text("Thêm Khóa Học Thành công"),
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=exit
        )

        self.dlg_modal1 = ft.AlertDialog(
            modal=True,
            title=ft.Text("Lỗi"),
            content=ft.Text("Có lỗi xảy ra"),
            actions=[
                ft.TextButton("OK", on_click=close_dlg1),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        def close_dlg2(e):
            self.dlg_modal2.open = False
            self.page.update()
        self.dlg_modal2 = ft.AlertDialog(
            modal=True,
            title=ft.Text("Lỗi"),
            content=ft.Text("Tên khóa học đã tồn tại"),
            actions=[
                ft.TextButton("OK", on_click=close_dlg2),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def on_login_clicked(e):
            try:
                if (len(course_name_field.value)==0 or len(description_field.value)==0):
                    self.page.dialog = self.dlg_modal1
                    self.dlg_modal1.open = True
                    self.page.update()
                    return
                if (checkName(connect_db,course_name_field.value)):
                    self.page.dialog = self.dlg_modal2
                    self.dlg_modal2.open = True
                    self.page.update()
                    return
                insert_course(connect_db, course_name_field.value, description_field.value, id_field.value)
                self.page.dialog = self.dlg_modal
                self.dlg_modal.open = True
                self.page.update()
            except Exception as e:
                error_message = f"Có lỗi xảy ra: {str(e)}"
                self.dlg_modal1.content = ft.Text(error_message)
                self.page.dialog = self.dlg_modal1
                self.dlg_modal1.open = True
                self.page.update()

        # Define textBox
        course_name_field = TextField(text_style=TextStyle(color="#000000"), width=500, border_radius=15,
                                      border_color=colors.BLACK, focused_border_color=colors.ORANGE_700)
        description_field = TextField(text_style=TextStyle(color="#000000"), width=500, border_radius=15,
                                      border_color=colors.BLACK, focused_border_color=colors.ORANGE_700)
        id_field = TextField(text_style=TextStyle(color="#000000"), width=500, border_radius=15,
                             border_color=colors.BLACK, focused_border_color=colors.ORANGE_700,value= self.id,read_only=True)

        # Design Button login
        login_button = ElevatedButton(
            "ADD",
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

        # Design Button Cancel
        cancel_button = ElevatedButton(
            "Cancel",
            width=300,
            height=60,
            style=ButtonStyle(
                color="#ffffff",
                bgcolor=colors.RED_700,
                shape={
                    MaterialState.FOCUSED: RoundedRectangleBorder(radius=5),
                    MaterialState.HOVERED: RoundedRectangleBorder(radius=5),
                },
                padding=20,
            ),on_click= lambda e : self.clickBack()
        )
        register_course_page = Container(
            width=600,
            bgcolor="#ffffff",
            border_radius=10,
            content=Column(
                width=320,
                controls=[
                    Column(
                        controls=[
                            Container(
                                padding=padding.only(bottom=20),
                                content=Row(
                                    controls=[
                                        Container(
                                            margin=margin.only(left=60, right=10, top=10),
                                            content=Text("THÊM KHÓA HỌC", size=30, color="#000000", weight="w800")
                                        )
                                    ]
                                )
                            ),

                            Container(
                                width=500,
                                margin=margin.only(left=20, right=20, top=10),
                                content=Column(
                                    controls=[
                                        Text("Tên Khóa Học", size=20, color="#000000", weight="w500"),
                                        course_name_field
                                    ]
                                )
                            ),
                            Container(
                                width=500,
                                margin=margin.only(left=20, right=20, top=10),
                                content=Column(
                                    controls=[
                                        Text("Mô Tả", size=20, color="#000000", weight="w500"),
                                        description_field
                                    ]
                                )
                            ),
                            Container(
                                width=500,
                                margin=margin.only(left=20, right=20, top=10),
                                content=Column(
                                    controls=[
                                        Text("ID Teacher", size=20, color="#000000", weight="w500"),
                                        id_field
                                    ]
                                )
                            ),
                            Container(
                                margin=margin.only(left=70, right=20, top=10),
                                padding=padding.only(bottom=20),
                                content=Row(
                                    controls=[
                                        Container(content=login_button,
                                                  margin=margin.only(right=30), width=200
                                                  ),

                                        Container(content=cancel_button, width=200)
                                    ]
                                )
                            ),

                        ]
                    )
                ]
            ),
        )
        self.body = Container(
            expand=True,
            content=Column(
                controls=[
                    Row(
                controls=[register_course_page],
                alignment=MainAxisAlignment.SPACE_EVENLY,
                )],
                alignment=MainAxisAlignment.CENTER
                )
        )
    def clickBack(self):
        from form.Teacher_Student.mainForm_Teacher import Main as Main1
        self.page.clean()
        self.exit()
        Main1(self.page,self.id).run()
        self.page.update()
    def run(self):
        self.page.add(self.body)

    def exit(self):
        pass

# app(target=main)
