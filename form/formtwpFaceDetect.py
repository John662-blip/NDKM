from flet import *
import threading
import base64
import time
from .settings import *
from connectdb import cursor
import cv2
import os
from form.Register import Main as Form_register

cascadePath = PATH_XML
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
class Main:
    def __init__(self,page):
        self.recognizer = cv2.face.LBPHFaceRecognizer.create()
        self.recognizer.read(PATH_TRAINER)
        self.page=page
        self.canStart = False
        self.cap = cv2.VideoCapture(0)
        self.image_Box = Image(
            src_base64="///Z",
            expand=True,
        )
        self.update_image_thread = threading.Thread(target=self.update_image)
        self.update_image_thread.daemon = True
        self.update_image_thread.start()
        self.btn = ElevatedButton(content=Text("Bắt đầu"),height=30,bgcolor="#00FFFF",on_click=lambda e:self.clickSubmit())
        self.first_page = Container(
            expand=True,
            border_radius=20,
            bgcolor=BG,
            content=Column(
                controls=[
                    Container(
                        alignment=alignment.Alignment(0,0),
                        content=Column(
                            controls=[
                                Container(
                                     margin = Margin(5,10,0,0),
                                    content= ElevatedButton(content=Text("Quay lại",color='white'),height=30,bgcolor="black",on_click=lambda e:self.clickBack())
                                ),
                                Container(
                                    margin = Margin(0,-20,0,0),
                                    alignment=alignment.Alignment(0,0),
                                    content=Text("Hãy để khuôn mặt vào", size=30,weight=FontWeight.BOLD, color="pink600", italic=True),
                                ),
                                Container(
                                    alignment=alignment.Alignment(0,0),
                                    margin=Margin(0,10,0,0),
                                    content=Container(
                                        border_radius=185,
                                        content=self.image_Box
                                    ) 
                                ),
                                Container(
                                    margin = Margin(0,10,0,0),
                                    alignment=alignment.Alignment(0,0),
                                    content = self.btn
                                )
                            ]
                        )
                    ),    
                ]
            )
        )
    def callDB(self):
        self.update_image_thread = threading.Thread(target=self.update_image)
        self.update_image_thread.daemon = True
        self.update_image_thread.start()
    def Recognize(self,img):
        check = False
        ima = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        equalized_image = cv2.equalizeHist(ima)

        # Áp dụng bộ lọc Gaussian để làm mờ ảnh
        col = cv2.GaussianBlur(equalized_image, (5, 5), 0)    
        faces = faceCascade.detectMultiScale(
            col,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            id,confidence = self.recognizer.predict(col[y:y+h,x:x+w])
            if (confidence<conF):
                confidence = "  {0}".format(round(100-confidence))
                check = True
                cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
            else:
                id = "unknow"
                check = False
                if (self.canStart):
                    cv2.imwrite(self.stringPath+"/User." + str(self.maxId + 1) + "." + str(self.cout) + ".jpg", col[y:y+h, x:x+w])
                    self.cout+=1
                confidence = " {0}".format(round(100-confidence))
                cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
            cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(255,255,0),1)
        return img,check

    def update_image(self):
        self.cout = 0        
        while  self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret == True:
                frame = cv2.flip(frame,1)
                image,check = self.Recognize(frame)
                _, buffer = cv2.imencode('.jpg', image)
                b64_string = base64.b64encode(buffer).decode('utf-8')
                if (self.image_Box):
                    self.image_Box.src_base64 = b64_string
                self.page.update()     
            else:
                break
            if (self.cout>30):
                self.page.clean()
                self.exit()
                Form_register(self.page,int(self.maxId+1)).run()
                self.page.update()
            time.sleep(1/115)
    def clickBack(self):
        from .form_main import Main as Form_Main
        self.page.clean()
        self.exit()
        Form_Main(self.page).run()
        self.page.update()
    def clickSubmit(self):
        self.canStart = True
        self.btn.content = Text("Đã bắt đầu chụp")
    def changeRouter(self,router):
        self.page.route=router
        self.page.update()
    def run(self):
        cursor.execute("SELECT MAX(id) AS max_id FROM users")
        myResult = cursor.fetchall()
        if myResult[0][0] is None:
            self.maxId = 0
        else:
            self.maxId = int(myResult[0][0])
        self.stringPath = "form/service/face/twp/"+str(self.maxId+1)
        if not os.path.exists(self.stringPath):
            os.makedirs(self.stringPath)
        for filename in os.listdir(self.stringPath):
            file_path = os.path.join(self.stringPath, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.page.add(self.first_page)
    def exit(self):
        if self.cap.isOpened():
            self.cap.release()
