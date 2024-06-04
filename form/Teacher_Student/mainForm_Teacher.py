from flet import *
import flet as ft
from form.settings import *
from form.EditUser import Main as MainEd
from dung.formStatistic import Main as MainTK
from form.Teacher_Student.form_add_course import Main as MainAdd
from dung.formCheck import Main as MainDD
class Main:
    def __init__(self,page,id):
        self.page  = page
        self.id = id

        main_form_teacher = Container(
            expand=True,
            # alignment=alignment.center,
            content=Column(
                expand=True,
                controls=[
                    Container(
                                margin = Margin(20,0,50,0),
                                content= ElevatedButton(content=Text("Quay lại",color='white'),height=30,bgcolor="black",on_click=lambda e:self.clickBack())
                                ),
                    Container(
                        content=Container( 
                                content=Row(
                                # alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ElevatedButton(content=Container(
                                        content=Column(
                                            [
                                                Row(                                                  
                                                    controls=[Icon(icons.EDIT,size=80, color="red")],
                                                    alignment=MainAxisAlignment.CENTER
                                                ),
                                                Row(
                                                    controls = [Text("Chỉnh Sửa Thông Tin",size=40, color="#000000", weight="w800")],
                                                    alignment=MainAxisAlignment.CENTER
                                                )
                                            ],
                                        alignment=MainAxisAlignment.CENTER
                                        )
                                    ),expand=True,height=200,bgcolor="#21f562",on_click=lambda e:self.clickEdit()),
                                    ElevatedButton(content=Container(
                                        content=Column(
                                            [
                                                Row(                                                  
                                                    controls=[Icon(icons.ADD_OUTLINED,size=80, color="Green")],
                                                    alignment=MainAxisAlignment.CENTER
                                                ),
                                                Row(
                                                    controls = [Text("Tạo Khóa Học",size=40, weight = "w800", color="#000000")],
                                                    alignment=MainAxisAlignment.CENTER
                                                )
                                            ],
                                        alignment=MainAxisAlignment.CENTER
                                        )
                                    ),expand=True,height=200,bgcolor="#f7ff6d",on_click=lambda e: self.ClickAdd()),
                                ]
                            )
                        )
                    ),
                    Container(
                        height=50
                    ),
                    Container(
                        content=Container( 
                                content=Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ElevatedButton(content=Container(
                                        content=Column(
                                            [
                                                Row(                                                  
                                                    controls=[Icon(icons.CAMERA_ALT_OUTLINED,size=80, color="Orange")],
                                                    alignment=MainAxisAlignment.CENTER
                                                ),
                                                Row(
                                                    controls = [Text("Điểm Danh",size=40, weight="w800", color="#000000")],
                                                    alignment=MainAxisAlignment.CENTER
                                                )
                                            ],
                                        alignment=MainAxisAlignment.CENTER
                                        )
                                    ),expand=True,height=200,bgcolor="#00FFFF",on_click=lambda e:self.ClickDD()),
                                    ElevatedButton(content=Container(
                                        content=Column(
                                            [
                                                Row(                                                  
                                                    controls=[Icon(icons.AUTO_GRAPH_ROUNDED,size=80, color="#ffffff")],
                                                    alignment=MainAxisAlignment.CENTER
                                                ),
                                                Row(
                                                    controls  = [Text("Thống Kê Từng Lớp",size=40, weight="w800", color="#000000")],
                                                    alignment=MainAxisAlignment.CENTER
                                                )
                                            ],
                                        alignment=MainAxisAlignment.CENTER
                                        )
                                    ),expand=True,height=200,bgcolor="Orange",on_click=lambda e:self.ClickTK()),
                                ]
                            )
                        )
                    ),
                ]
            )
        )
        self.body = Container(
            # margin = margin.only(left=500),
            bgcolor=BG,
            expand=True,
            border_radius=20,
            content=Column(
                controls=[
                    Row(
                    controls=[main_form_teacher],
                    alignment=MainAxisAlignment.SPACE_EVENLY,
                )]
                ,alignment=MainAxisAlignment.CENTER
            )
        )
    def clickBack(self):
        from form.form_main import Main as Form_Main
        self.page.clean()
        self.exit()
        Form_Main(self.page).run()
        self.page.update()
    def clickEdit(self):
        self.page.clean()
        self.exit()
        MainEd(self.page,self.id,0).run()
        self.page.update()
    def ClickTK(self):
        self.page.clean()
        self.exit()
        MainTK(self.page,self.id).run()
        self.page.update()
    def ClickDD(self):
        self.page.clean()
        self.exit()
        MainDD(self.page,self.id).run()
        self.page.update()
    def ClickAdd(self):
        self.page.clean()
        self.exit()
        MainAdd(self.page,self.id).run()
        self.page.update()
    def run(self):
        self.page.add(self.body)
    def exit(self):
        pass

# app(target=main)