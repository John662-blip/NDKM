from flet import *
from form.youdate import Youdate
from connectdb import Statistics
#styler and attribute for header


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
    def __init__(self, dt: DataTable,page) -> None:
        super().__init__(**header_style, on_hover=self.toggle_search)
        self.dt: DataTable = dt
        self.page = page
        self.search_value: TextField = search_field(self.filter_dt_rows)

        self.search: Container = search_bar(self.search_value)

        self.avartar = IconButton("person")
        # Định nghĩa nút thoát
        def exit(e):
            from form.form_main import Main
            page.clean()
            Main(page).run()
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
        for data_rows in self.dt.rows:
            data_cell: any = data_rows.cells[1]
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
    "Họ","Tên", "Ngày điểm danh"
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
    def __init__(self,page):
        self.page = page
        # page.bgcolor = ""
        stats = Statistics()  # Initialize the Statistics object
        data_from_db = stats.load()
        self.table = DataTable()
        self.table.dt = {i: {'fname': row[0],'lname': row[1], 'date check': row[2]} for i, row in enumerate(data_from_db)}
        header = Header(dt=self.table,page=self.page)
        self.container=Column(
                expand=True,
                controls=[
                    header,
                    Divider(height=2,color="transparent"),
                    Column(
                        controls=[Row(controls=[Youdate(self.table)])]
                    ),
                    Column(
                        scroll=True,
                        expand=True,
                        controls=[Row(controls=[self.table])]
                    )
                ]
            )
    def run(self):
        self.page.add(self.container)
        self.page.update()
        self.table.fill_data_table()
    def exit(self):
        pass