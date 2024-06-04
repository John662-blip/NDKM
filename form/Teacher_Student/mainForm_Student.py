from flet import *
import flet as ft
# from user import insert_user
from form.settings import *
from PIL import Image
from form.EditUser import Main as MainEd
from dung.formEnrollcourse import Main as MainAdd
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
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ElevatedButton(content=Container(
                                        content=Column(
                                            [
                                                Row(                                                  
                                                    controls=[Icon(icons.ADD_CIRCLE_ROUNDED,size=80, color="red")],
                                                    alignment=MainAxisAlignment.CENTER
                                                ),
                                                Row(
                                                    controls = [Text("Đăng Kí Môn Học",size=40, color="#000000", weight="w800")],
                                                    alignment=MainAxisAlignment.CENTER
                                                )
                                            ],
                                        alignment=MainAxisAlignment.CENTER
                                        )
                                    ),expand=True,height=200,bgcolor="#21f562",on_click=lambda e:self.clickAdd()),
                                    ElevatedButton(content=Container(
                                        content=Column(
                                            [
                                                Row(                                                  
                                                    controls=[Icon(icons.EDIT_OUTLINED,size=80, color="Green")],
                                                    alignment=MainAxisAlignment.CENTER
                                                ),
                                                Row(
                                                    controls = [Text("Chỉnh Sửa Thông Tin",size=40, weight = "w800", color="#000000")],
                                                    alignment=MainAxisAlignment.CENTER
                                                )
                                            ],
                                        alignment=MainAxisAlignment.CENTER
                                        )
                                    ),expand=True,height=200,bgcolor="#f7ff6d",on_click=lambda e : self.clickEdit()),
                                ]
                            )
                        )
                    ),
                    Container(
                        height=50
                    ),
                ]
            )
        )
        self.body = Container(
            # margin = margin.only(left=500),
            expand=True,
            border_radius=20,
            bgcolor=BG,
            content=Column(
                controls=[
                    Row(
                controls=[main_form_teacher],
                alignment=MainAxisAlignment.SPACE_EVENLY,
                )],
                alignment=MainAxisAlignment.CENTER
            ),
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
        MainEd(self.page,self.id,1).run()
        self.page.update()
    def clickAdd(self):
        self.page.clean()
        self.exit()
        MainAdd(self.page,self.id).run()
        self.page.update()
    def run(self):
        self.page.add(self.body)
    def exit(self):
        pass

# app(target=main)