from flet import *
import flet as ft
from form.settings import *
from form.formtwpFaceDetect import Main as Main1
from form.form1 import Main as Main2
class Main:
    def __init__(self,page):
        self.page  = page
        main_form_teacher = Container(
            expand=True,
            alignment=alignment.center,
            content=Column(
                controls=[
                    Container(
                        content=Container( 
                                content=Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ElevatedButton(content=Container(
                                        content=Column(
                                            [
                                                Row(                                                  
                                                    controls=[Icon(icons.GROUP_ADD_ROUNDED,size=80, color="red")],
                                                    alignment=MainAxisAlignment.CENTER
                                                ),
                                                Row(
                                                    controls = [Text("Đăng Kí Khuôn Mặt",size=40, color="#000000", weight="w800")],
                                                    alignment=MainAxisAlignment.CENTER
                                                )
                                            ],
                                        alignment=MainAxisAlignment.CENTER
                                        )
                                    ),expand=True,height=200,bgcolor="#21f562",on_click=lambda e : self.click_Dk()),
                                    ElevatedButton(content=Container(
                                        content=Column(
                                            [
                                                Row(                                                  
                                                    controls=[Icon(icons.LOGIN,size=80, color="Green")],
                                                    alignment=MainAxisAlignment.CENTER
                                                ),
                                                Row(
                                                    controls = [Text("Đăng Nhập",size=40, weight = "w800", color="#000000")],
                                                    alignment=MainAxisAlignment.CENTER
                                                )
                                            ],
                                        alignment=MainAxisAlignment.CENTER
                                        )
                                    ),expand=True,height=200,bgcolor="#f7ff6d",on_click=lambda e : self.click_DN()),
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
    def click_Dk(self):
        self.page.clean()
        self.exit()
        Main1(self.page).run()
        self.page.update()
    def click_DN(self):
        self.page.clean()
        self.exit()
        Main2(self.page).run()
        self.page.update()
    def run(self):
        self.page.add(self.body)
    def exit(self):
        pass

# app(target=main)