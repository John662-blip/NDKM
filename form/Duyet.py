from flet import *
from connectdb import Users
import os
from form.service.face.Train import training
import shutil
# Cập nhật tên cột để bao gồm nút đăng kí
column_names : list[str] = [
    "id", "Họ", "Tên","Địa Chỉ", "Loại" ,"Duyệt","Không Duyệt"
]

# Định nghĩa lại kiểu dáng cho bảng dữ liệu
data_table_style: dict[str, any] = {
    "expand": True,
    "border_radius": 8,
    "border": border.all(2, "#ebebeb"),
    "horizontal_lines": border.BorderSide(1, "#ebebeb"),
    "columns": [
        DataColumn(Text(index, size=12, color="black", weight="bold"))
        for index in column_names
    ]
}

class DataTable(DataTable):
    def __init__(self) -> None:
        super().__init__(**data_table_style)

    def fill_data_table(self, data_list) -> None:
        self.rows = []

        for values in data_list:
            data = DataRow()
            data.cells = [
                DataCell(Text(value, color="black"))
                 if index not in ["Duyệt", "Không Duyệt"] else
                DataCell(value)
                for index, value in values.items()
            ]
            self.rows.append(data)
        self.update()

class Main:
    def __init__(self, page, student_id):
        self.page = page
        self.student_id = student_id
        self.canClick = True
        self.stats = Users()  # Initialize the Statistics object
        data_from_db = self.stats.load()

        # Create the data table and fill it with data
        self.table = DataTable()
        
        self.table.dt = {i: {'id': row[0],'Họ' : row[1], 'Tên' : row[2] , "Địa Chỉ" :row[3] ,"Loại":row[4]}  for i, row in enumerate(data_from_db)}

        # Create a button for each course
        for i,data in  enumerate(self.table.dt.values()):
            btnRegister = ElevatedButton(
                text="Duyệt",
                on_click=lambda e, user_id=data['id']: self.DuyetUsers(user_id),
                width=200,
                bgcolor="#EEF7FF",
                color="#141E46",
            )
            data['Duyệt'] = btnRegister

        for i,data in  enumerate(self.table.dt.values()):
            btnRegister = ElevatedButton(
                text="Xóa",
                on_click=lambda e, user_id=data['id']: self.xoaUsers(user_id),
                width=200,
                bgcolor="#EEF7FF",
                color="#141E46",
            )
            data['Không Duyệt'] = btnRegister
        # Create dialog for successful registration
        def close_dlg(e):
            self.dlg_modal.open = False
            self.page.update()
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Thông báo"),
            content=Text("Duyệt Thành Công"),
            actions=[
                TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=MainAxisAlignment.END
        )

        # Create dialog for failed registration
        def close_dlg2(e):
            self.dlg_modal2.open = False
            self.page.update()
        self.dlg_modal2 = AlertDialog(
            modal=True,
            title=Text("Thông báo"),
            content=Text("Xóa Thành Công"),
            actions=[
                TextButton("OK", on_click=close_dlg2),
            ],
            actions_alignment=MainAxisAlignment.END
        )
        def close_dlg3(e):
            self.dlg_modal3.open = False
            self.page.update()
        self.dlg_modal3 = AlertDialog(
            modal=True,
            title=Text("Thông báo"),
            content=Text("Thao Tác Thất Bại"),
            actions=[
                TextButton("OK", on_click=close_dlg3),
            ],
            actions_alignment=MainAxisAlignment.END
        )
        # Create search field
        self.search_value = TextField(
            border_color="transparent",
            height=20,
            text_size=14,
            content_padding=0,
            cursor_color="white",
            cursor_width=1,
            color="white",
            hint_text="Search",
            on_change=self.filter_dt_rows,
        )

        # Create search bar
        self.search = Container(
            width=350,
            bgcolor="white10",
            border_radius=6,
            opacity=0,
            animate_opacity=300,
            padding=8,
            content=Row(
                spacing=10,
                vertical_alignment="center",
                controls=[
                    Icon(
                        name=icons.SEARCH_ROUNDED,
                        size=17,
                        opacity=0.85,
                    ),
                    self.search_value,
                ],
            ),
        )

        # Create header
        self.header = Container(
            height=60,
            bgcolor="#7befa7",
            border_radius=border_radius.only(top_left=15,top_right=15),
            padding=padding.only(left=15,right=15),
            on_hover=self.toggle_search,
            content=Row(
                alignment="spaceBetween",
                controls=[
                    IconButton("person"),
                    self.search,
                    TextButton("Back", icon="close", on_click=self.exit),
                ],
            ),
        )

    def toggle_search(self, e: HoverEvent) -> None:
        self.search.opacity = 1 if e.data == "true" else 0
        self.search.update()
    def reload_data(self):
        data_from_db = self.stats.load()
        data_list = [
            {
                'id': row[0],
                'Họ': row[1],
                'Tên': row[2],
                'Địa Chỉ': row[3],
                'Loại': row[4],
                'Duyệt': ElevatedButton(
                    text="Duyệt",
                    on_click=lambda e, user_id=row[0]: self.DuyetUsers(user_id),
                    width=200,
                    bgcolor="#EEF7FF",
                    color="#141E46",
                ),
                'Không Duyệt': ElevatedButton(
                    text="Xóa",
                    on_click=lambda e, user_id=row[0]: self.xoaUsers(user_id),
                    width=200,
                    bgcolor="#EEF7FF",
                    color="#141E46",
                )
            }
            for row in data_from_db
        ]
        self.table.fill_data_table(data_list)
    def filter_dt_rows(self, e):
        for data_rows in self.table.rows:
            data_cell: any = data_rows.cells[2]
            data_rows.visible = (
                True
                if e.control.value.lower() in data_cell.content.value.lower()
                else False
            )
            data_rows.update()
    def xoaUsers(self,id):
        if (self.canClick):
            self.canClick = False
            folder_path = f"form/service/face/twp/{id}"
            try:
                self.stats.DeleteUser(id)
                shutil.rmtree(folder_path)
                self.page.dialog = self.dlg_modal2
                self.dlg_modal2.open = True
                self.page.update()
                self.reload_data()
                self.canClick = True
                self.search_value.value = ""
            except FileNotFoundError:
                self.canClick = True
                pass
            except Exception as e:
                print(e)
                self.page.dialog = self.dlg_modal3
                self.dlg_modal3.open = True
                self.page.update()
                self.canClick = True
    def DuyetUsers(self, id):
        if (self.canClick):
            self.canClick = False
            try:
                if (self.stats.DuyetUser(id)):
                    for filename in os.listdir(f"form/service/face/twp/{id}"):
                        source_file_path = os.path.join(f"form/service/face/twp/{id}", filename)
                        if os.path.isfile(source_file_path):
                            destination_file_path = os.path.join("form/service/face/dataSet", filename)
                            shutil.move(source_file_path, destination_file_path)
                    if not os.listdir(f"form/service/face/twp/{id}"):  # Kiểm tra xem thư mục có trống không
                        os.rmdir(f"form/service/face/twp/{id}")#xóa
                    training()
                    self.page.dialog = self.dlg_modal
                    self.dlg_modal.open = True
                    self.page.update()
                    self.reload_data()
                    self.canClick = True
                    self.search_value.value = ""
            except Exception as e:
                print(e)
                self.page.dialog = self.dlg_modal3
                self.dlg_modal3.open = True
                self.page.update()
                self.canClick = True

    def exit(self, e):
        from form.form_main import Main
        self.page.clean()
        Main(self.page).run()
        self.page.update()

    def run(self):
        # ... (phần còn lại của mã nguồn không thay đổi)

        self.container = Column(
            expand=True,
            controls=[
                self.header,
                Divider(height=2, color="transparent"),
                Row(controls=[self.table])
            ]
        )
        self.page.add(self.container)
        self.page.update()
        self.table.fill_data_table(self.table.dt.values())
        

# Usage:
# from dung.formEnrollcourse import Register

# application = None

# def main(page: Page):
#     global application
#     application = Register(page, 1)
#     application.run()

# app(target=main, view=WEB_BROWSER)
