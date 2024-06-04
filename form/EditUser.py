from flet import *
import flet as ft
from form.user import update_user
from connectdb import cursor as connect_db


class Main:
    def __init__(self,page,id,type):
        self.page = page
        self.type = type
        self.id = id
        self.fname =""
        self.lname = ""
        self.sdt = ""
        self.address = ""
        try:
            sql_query = f"select fname,lname,sdt,address from Users where id = {id}"
            connect_db.execute(sql_query)
            myResult = connect_db.fetchall()
            self.fname = myResult[0].fname
            self.lname = myResult[0].lname
            self.sdt = myResult[0].sdt
            self.address = myResult[0].address
        except:
            pass
        def exit(e):
            if (self.type == 0):
                from form.Teacher_Student.mainForm_Teacher import Main as Mai1
                self.page.clean()
                self.exit()
                Mai1(self.page,self.id).run()
                self.page.update()
            else :
                from form.Teacher_Student.mainForm_Student import Main as Mai2
                self.page.clean()
                self.exit()
                Mai2(self.page,self.id).run()
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
            content=ft.Text("Cập Nhập User Thành công"),
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
    
        def on_edit_clicked(e):
            try:
                update_user(connect_db, id_field.value, first_name_field.value, last_name_field.value, phone_field.value, address_field.value)
                page.dialog = self.dlg_modal
                self.dlg_modal.open = True
                page.update()
            except Exception as e:
                page.dialog = self.dlg_modal1
                self.dlg_modal1.open = True
                page.update()
                print(e)
        #Button Cancel
        def on_cancel_clicked(e):
            if (self.type == 0):
                from form.Teacher_Student.mainForm_Teacher import Main as Mai1
                self.page.clean()
                self.exit()
                Mai1(self.page,self.id).run()
                self.page.update()
            else :
                from form.Teacher_Student.mainForm_Student import Main as Mai2
                self.page.clean()
                self.exit()
                Mai2(self.page,self.id).run()
                self.page.update()


        # Define textBox
        id_field = TextField(text_style=TextStyle(color="#000000"), border_radius=15, border_color=colors.BLACK, focused_border_color=colors.ORANGE_700,value=self.id,read_only=True)
        first_name_field = TextField(text_style=TextStyle(color="#000000"), width=200, border_radius=15, border_color=colors.BLACK, focused_border_color=colors.ORANGE_700,value=self.fname)
        last_name_field = TextField(text_style=TextStyle(color="#000000"), width=200, border_radius=15, border_color=colors.BLACK, focused_border_color=colors.ORANGE_700,value=self.lname)
        phone_field = TextField(text_style=TextStyle(color="#000000"), border_radius=15, border_color=colors.BLACK, focused_border_color=colors.ORANGE_700,value=self.sdt)
        address_field = TextField(text_style=TextStyle(color="#000000"), border_radius=15, border_color=colors.BLACK, focused_border_color=colors.ORANGE_700,value=self.address)


        #Design Button login
        edit_button = ElevatedButton(
                "Edit",
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
                on_click=on_edit_clicked
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
                        content=Text("CẬP NHẬP THÔNG TIN", size=30, color="#000000", weight="w800")
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
                        margin=margin.only(left=20, right=20, top=15),
                        content=Column(
                            controls=[
                                Text("Address", size=20, color="#000000", weight="w500"),
                                address_field
                            ]
                        )
                    ),
                    Container(
                        margin = margin.only(left=70, right=20, top=10),
                        padding = padding.only(bottom=20),
                        content = Row(
                            controls=[
                                Container(content=edit_button,
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
            # width=1000,
            # height=800,
            content=Row(
                controls=[
                    Column(
                        controls=[
                            register_page
                        ],
                       # alignment= MainAxisAlignment.END
                    ),
                    
                ]
            ,
                alignment=MainAxisAlignment.SPACE_EVENLY,

            ) 
        )
    def run(self):
        self.page.add(self.body)
    def exit(self):
        pass
