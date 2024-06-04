from flet import *
from form.youdate import Youdate
from connectdb import Statistics
import pandas as pd
import threading
#styler and attribute for header
import datetime
import os
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path_1 = os.path.join(desktop_path, 'attendance_data.xlsx')
header_style: dict[str, any] = {
    "height": 60,
    "bgcolor": "#7befa7",
    "border_radius":  border_radius.only(top_left=15,top_right=15),
    "padding": padding.only(left=15,right=15),
}

def search_field(function: callable)-> TextField:
    return TextField(
        border_color="transparent",
        height=20,
        text_size=14,
        content_padding=0,
        cursor_color="white",
        cursor_width=1,
        color="white",
        hint_text="Search",
        on_change=function,
    )

def search_bar(control: TextField) -> Container:
    return Container(
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
                control,
            ],
        ),
    )
#header
class Header(Container):
    def __init__(self, dt: DataTable,page,id,func,youdate) -> None:
        super().__init__(**header_style, on_hover=self.toggle_search)
        self.dt: DataTable = dt
        self.youdate = youdate
        self.id = id
        self.func = func
        self.page = page
        # self.table = DataTable()
        self.search_value: TextField = search_field(self.filter_dt_rows)

        self.search: Container = search_bar(self.search_value)

        self.avartar = IconButton("person")
        # Định nghĩa nút thoát
        def exit(e):
            from form.Teacher_Student.mainForm_Teacher import Main
            page.clean()
            Main(page,self.id).run()
            page.update()
        self.exit_button = TextButton("Back",icon="close", on_click=exit) # Thoát khi nút được nhấp

        # Căn chỉnh các phần tử bên trong header
        self.content = Row(
            alignment="spaceBetween",  # Căn các phần tử theo hướng ngang, nút thoát sẽ ở bên phải
            controls=[self.avartar, self.search, self.exit_button]  # Thêm nút thoát vào header
        )
    def toggle_search(self,e: HoverEvent) -> None:
        self.search.opacity = 1 if e.data == "true" else 0
        self.search.update()
    def filter_dt_rows(self,e):
        # print(self.search_value)
        self.func(self.youdate.selected_date)
        for data_rows in self.dt.rows:
            data_cell: any = data_rows.cells[1]
            if (data_rows.visible):
                data_rows.visible = (
                    True
                    if e.control.value.lower() in data_cell.
                    content.value.lower()
                    else False
                )
            data_rows.update()
    
def text_field() -> TextField:
    return TextField(
        border_color="transparent",
        height=20,
        text_size=13,
        content_padding=0,
        cursor_color="black",
        cursor_width=1,
        cursor_height=18,
        color = "black",
    )

def text_field_container(
        expand: bool | int, name: str, control: TextField
)-> Container:
    return Container(
        expand=expand,
        height=45,
        bgcolor="#ebebeb",
        border_radius=6,
        padding=8,
        content=Column(
            spacing=1,
            control=[
                Text(
                    value=name,
                    size=9,
                    color="black",
                    weight="bold",
                ),
                control
            ]
        )
    )

column_names : list[str] = [
    "Họ","Tên", "Ngày điểm danh", "Id_Môn"
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
        self.page = page
        # page.bgcolor = ""
        #data1
        def close_dlg(e):
            self.dlg_modal.open = False
            self.page.update()

        def close_dlg1(e):
            self.dlg_modal1.open = False
            self.page.update()

        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Thông báo"),
            content=Text("Lưu file tại attendance_data.xlsx trên màn hình chính"),
            actions=[
                TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=MainAxisAlignment.END,
            # on_dismiss=exit
        )

        self.dlg_modal1 = AlertDialog(
            modal=True,
            title=Text("Lỗi"),
            content=Text("Có lỗi xảy ra"),
            actions=[
                TextButton("OK", on_click=close_dlg1),
            ],
            actions_alignment=MainAxisAlignment.END
        )
        stats = Statistics()  # Initialize the Statistics object
        data_from_db = stats.load(self.teacher_id)
        self.table = DataTable()
        self.table.dt = {i: {'fname': row[0],'lname': row[1], 'date check': row[2], 'course_id': row[3]} for i, row in enumerate(data_from_db)}
        #data2
        data_from_db2 = stats.loadCourse(self.teacher_id)
        self.table2 = DataTable()
        self.table2.dt = {i: {'name': row[0],'id' : row[1]}  for i, row in enumerate(data_from_db2)}
        #cobobox
        self.course_data = [(row['name'], row['id']) for row in self.table2.dt.values()]
        self.cbxSelectCourse = Dropdown(
            filled= True,
            label="Môn Học",
            hint_text="Chọn",
            options=[dropdown.Option(text=name,key=id) for name,id in self.course_data],
            width=200,
            bgcolor="#EEF7FF",
            color="#141E46",
            on_change= self.changeValue
        )
        if (len(self.course_data)!=0):
            default_value = self.course_data[0]  # Chọn mặc định là phần tử đầu tiên trong danh sách
            self.cbxSelectCourse.value = default_value[1]

        self.youdate = Youdate(self.filter_table,self.clearSearch)
        self.header = Header(dt=self.table,page=self.page,id=self.teacher_id,func=self.filter_table,youdate=self.youdate)
        self.print_button = ElevatedButton(
            "Print",
            width=400,
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
            on_click=self.on_print_clicked
        )
        
        self.container = Column(
            expand=True,
            controls=[
                self.header,
                Divider(height=2, color="transparent"),
                Row(controls=[
                    self.youdate,
                    Container(width=700),
                    Container(margin=Margin(20, 10, 0, 0), content=self.cbxSelectCourse),
                ]),
                Column(scroll=True, expand=True, controls=[Row(controls=[self.table])]),
                Container(
                   margin = margin.only(left=70, right=20, top=10),
                        padding = padding.only(bottom=20),
                        content = Row(
                            controls=[
                                Container(content=self.print_button,
                                        margin=margin.only(right=30), width= 200
                                ),
                                
                            ]
                        )
                ),
            ]
        )
    def on_print_clicked(self, event):
        def export_data():
            try:
                # Collect data from DataTable
                data = []
                for row in self.table.rows:
                    if row.visible:  # Only include visible rows in the export
                        row_data = [cell.content.value for cell in row.cells]
                        data.append(row_data)

                # Create a DataFrame
                df = pd.DataFrame(data, columns=column_names)

                file_path = file_path_1

                # Write DataFrame to an Excel file
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)

                # Update the UI on the main thread after successful export
                self.page.dialog = self.dlg_modal
                self.dlg_modal.open = True
                self.page.update()
            except Exception as e:
                # Update the UI on the main thread in case of an error
                self.page.dialog = self.dlg_modal1
                self.dlg_modal1.open = True
                self.page.update()

        # Start the export_data function in a new thread
        export_thread = threading.Thread(target=export_data)
        export_thread.start()

       

    def clearSearch(self):
        self.header.search_value.value = ""
    def changeValue(self,e):
        self.header.search_value.value = ""
        self.filter_table(self.youdate.selected_date)
    def filter_table(self, date):
        if date is None:
            for row in self.table.rows:
                # Assuming the date is in the second column and course is in the third column
                row_course = str(row.cells[3].content.value)  # Chuyển đổi giá trị course_id thành chuỗi
                selected_course = str(self.cbxSelectCourse.value)  # Chuyển đổi giá trị từ ComboBox thành chuỗi
                # Check both the date and the course
                row.visible = (row_course == selected_course)
            self.table.update()
            return
        for row in self.table.rows:
            # Assuming the date is in the second column and course is in the third column
            row_date = row.cells[2].content.value.split(' ')[0]  # Chỉ lấy phần ngày
            row_course = str(row.cells[3].content.value)  # Chuyển đổi giá trị course_id thành chuỗi
            selected_course = str(self.cbxSelectCourse.value)  # Chuyển đổi giá trị từ ComboBox thành chuỗi
            # Check both the date and the course
            dateobj = datetime.datetime.strptime(row_date, "%Y-%m-%d").date()
            row.visible = (dateobj == date) and (row_course == selected_course)
        self.table.update()
    def run(self):
        self.page.add(self.container)
        self.page.update()
        self.table.fill_data_table()
        self.filter_table(self.youdate.selected_date)
    def exit(self):
        pass