from flet import *
from connectdb import Statistics

# Cập nhật tên cột để bao gồm nút đăng kí
column_names : list[str] = [
    "id", "Tên Môn", "Mô tả","Trạng Thái", "Đăng kí"
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

    def fill_data_table(self) -> None:
        self.rows = []

        for values in self.dt.values():
            data = DataRow()
            data.cells = [
                DataCell(Text(value, color="black"))
                if index != "Đăng kí" else
                DataCell(values["Đăng kí"])
                for index, value in values.items()
            ]
            self.rows.append(data)
        self.update()

class Main:
    def __init__(self, page, student_id):
        self.page = page
        self.student_id = student_id
        self.stats = Statistics()  # Initialize the Statistics object
        data_from_db = self.stats.loadCouseForStd(self.student_id)

        # Create the data table and fill it with data
        self.table = DataTable()
        self.table.dt = {i: {'id': row[0],'Tên Môn' : row[1], 'Mô Tả' : row[2] , "Trạng Thái" : "Đã Đăng Kí" if (row[3]==1) else " Chưa Đăng Kí"}  for i, row in enumerate(data_from_db)}

        # Create a button for each course
        for i,course in  enumerate(self.table.dt.values()):
            btnRegister = ElevatedButton(
                text="Đăng kí",
                on_click=lambda e, course_id=course['id']: self.register_course(course_id),
                width=200,
                bgcolor="#EEF7FF",
                color="#141E46",
            )
            course['Đăng kí'] = btnRegister

        # Create dialog for successful registration
        def close_dlg(e):
            self.dlg_modal.open = False
            self.page.update()
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Thông báo"),
            content=Text("Đăng kí Thành Công"),
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
            content=Text("Đăng kí thất bại. Bạn đã đăng kí môn này rồi!"),
            actions=[
                TextButton("OK", on_click=close_dlg2),
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

    def filter_dt_rows(self, e):
        for data_rows in self.table.rows:
            data_cell: any = data_rows.cells[1]
            data_rows.visible = (
                True
                if e.control.value.lower() in data_cell.content.value.lower()
                else False
            )
            data_rows.update()

    def register_course(self, course_id):
        # Here you can add the code to register the student to the selected course
        # For example:
        if self.stats.enrollCourse(course_id, self.student_id):
            self.page.dialog = self.dlg_modal
            self.dlg_modal.open = True
            self.page.update()
            found_index = next((index for index, course in enumerate(self.table.dt.values()) if course['id'] == course_id), None)
            self.table.dt[found_index]["Trạng Thái"] = "Đã Đăng Kí"
            self.table.fill_data_table()
        else:
            self.page.dialog = self.dlg_modal2
            self.dlg_modal2.open = True
            self.page.update()

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
        self.table.fill_data_table()

# Usage:
# from dung.formEnrollcourse import Register

# application = None

# def main(page: Page):
#     global application
#     application = Register(page, 1)
#     application.run()

# app(target=main, view=WEB_BROWSER)
