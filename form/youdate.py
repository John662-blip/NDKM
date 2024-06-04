from flet import *
from form.date_picker import DatePicker
from form.selection_type import SelectionType
from datetime import datetime

class Youdate(UserControl):
    def __init__(self, filter_table_func,func_clear):
        super().__init__()
        self.filter_table_func = filter_table_func
        self.func_clear = func_clear
        self.datepicker = None
        self.holidays = [datetime(2023,4,25),datetime(2023,5,1)]
        self.locales = ["vi_VN"]
        self.selected_locale = None
        self.selected_date = None
        self.you_select_date = Text(size=30,weight="bold")

        self.locales_opts = []

        for l in self.locales:
            self.locales_opts.append(
               dropdown.Option(l) 
            )
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Select date here"),
            actions=[
                TextButton("Cancel",
                           on_click=self.cancel_dlg),
                TextButton("Confirm",
                           on_click=self.confirm_dlg), 
            ],
            actions_padding=5,
            content_padding=0
            ) 
        self.tf = TextField(
            label="select here",
            dense=True,
            width=260,height=50
        )
        self.cal_icon = TextButton(
            icon=icons.CALENDAR_MONTH,
            on_click=self.open_dlg_modal,
            height=40,
            width=40,
            right=0,
            style=ButtonStyle(
                padding=Padding(4,0,0,0),
                shape={
                    MaterialState.DEFAULT:RoundedRectangleBorder(radius=1)
                }
            )
        )
        self.st = Stack([
            self.tf,
            self.cal_icon
        ])
        self.from_to_text = Text(visible=False)

    def build(self):
        return Column([
            Text("Chọn ngày:",size=20,weight="bold"),
            self.st,
            self.from_to_text,
            self.you_select_date
        ])
    def confirm_dlg(self,e):
        selected_date = self.datepicker.selected_data[0] if len(self.datepicker.selected_data) > 0 else None

        # Only get the date part of the selected date
        self.selected_date = selected_date.date() if selected_date else None

        selected_data_str = self.selected_date.strftime("%Y-%m-%d") if self.selected_date else None  # Trả về ngày theo định dạng 'YYYY/MM/DD'
        self.tf.value = selected_data_str

        # Filter the table based on the selected date
        self.filter_table_func(self.selected_date)  # Call the filter_table function of Main
        self.func_clear()
        self.dlg_modal.open =False
        self.update()
        self.page.update()
    def cancel_dlg(self,e):
        self.dlg_modal.open =False
        self.page.update()
    
    def open_dlg_modal(self,e):
        self.datepicker = DatePicker(
            hour_minute=True,
            selected_date=None,
            selection_type=int(0),
            #for sartuday and sunday
            holidays= self.holidays,
            #show 3 mont in date picker
            show_three_months=True,
            locale=self.selected_locale
            
        )
        self.page.dialog = self.dlg_modal
        self.dlg_modal.content = self.datepicker
        self.dlg_modal.open = True
        self.page.update()
    def get_selected_date(self):
        return self.selected_date

        