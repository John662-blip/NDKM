from flet import *
from form.service.face.Train import training

# from form.Register import Main
from form.form_main import Main

application = None
def main(page: Page):
    global application
    application = Main(page)
    application.run()

app(target=main, view=WEB_BROWSER)