from flet import *


# from form.Register import Main
from dung.formStatistic import Main
from form.service.face.Train import training


application = None

def main(page: Page):
    global application
    # page.window_resizable = False 

    application =  Main(page,2)
    application.run()
# training()
app(target=main, view=WEB_BROWSER)
