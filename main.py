import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel,QVBoxLayout,QFrame,QPushButton,QFileDialog
from PyQt5.QtCore import Qt
import json
from PyQt5.QtWidgets import QWidget, QApplication, QRubberBand
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt, QPoint, QRect
import time
import requests
import openai

def ask_chatgpt(question):
    openai.api_key = 'Enter Your own openai api key bro'
    question += "Give me the accurate ans of this question"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are jarvis, a large language model trained by subhashis. Your task to help him what he ask you need to answers all requests and follows all instructions And Give 1005 Accurate answer"},
            {"role": "user", "content": question},
            {"role": "assistant", "content": "Continue"}
        ],
        stream=False
    )
    
    response_json = response.__str__()
    response_dict = json.loads(response_json)
    mainresp = response_dict['choices'][0]['message']['content'].replace("OpenAI", "subhashis")
    return mainresp

def extract_text():
    upload_url = 'https://lens.google.com/v3/upload?hl=en-IN&re=df&st=1713462961116&vpw=1543&vph=877&ep=gsbubb'
    image_path = 'TEST.png'
    with open(image_path, 'rb') as image_file:
        files = {'encoded_image': (image_path, image_file, 'image/jpeg')}
        response = requests.post(upload_url, files=files)
        resp = response.text
        mainresp = resp.split('"en",[[["')[1].split('"]],')[0]
        return mainresp

def showans():
        extracted_text = extract_text()
        print("====================QUESTION==========================")
        print(extracted_text)
        print("=====================ANSWER===========================")
        print(ask_chatgpt(extracted_text))
        print("======================================================")


class Capture(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.main.hide()
        
        self.setMouseTracking(True)
        desk_size = QApplication.desktop()
        self.setGeometry(0, 0, desk_size.width(), desk_size.height())
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.15)

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()


        QApplication.setOverrideCursor(Qt.CrossCursor)
        screen = QApplication.primaryScreen()
        rect = QApplication.desktop().rect()

        time.sleep(0.31)
        self.imgmap = screen.grabWindow(
            QApplication.desktop().winId(),
            rect.x(), rect.y(), rect.width(), rect.height()
        )

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rubber_band.show() 

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        if not self.origin.isNull():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.rubber_band.hide()
            
            rect = self.rubber_band.geometry()
            self.imgmap = self.imgmap.copy(rect)
            QApplication.restoreOverrideCursor()
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(self.imgmap)
            self.imgmap.save("TEST.png")
            self.main.label.setPixmap(self.imgmap)
            self.main.show()
            self.close()
            print("Extracting Answer Please Wait...")
            Thread(target=showans).start()


class ScreenRegionSelector(QMainWindow):
    def __init__(self,):
        super().__init__(None)
        self.m_width = 400
        self.m_height = 500
        self.setWindowTitle("SM ALWAYS PRO")
        self.setMinimumSize(self.m_width, self.m_height)
        frame = QFrame()
        frame.setContentsMargins(0, 0, 0, 0)
        lay = QVBoxLayout(frame)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(5, 5, 5, 5)

        self.label = QLabel()
        self.btn_capture = QPushButton("Capture")
        self.btn_capture.clicked.connect(self.capture)
        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save)
        self.btn_save.setVisible(False)
        lay.addWidget(self.label)
        lay.addWidget(self.btn_capture)
        lay.addWidget(self.btn_save)
        self.setCentralWidget(frame)
    def capture(self):
        self.capturer = Capture(self)
        self.capturer.show()
        # self.btn_save.setVisible(True)
    def save(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image files (*.png *.jpg *.bmp)")
        if file_name:
            self.capturer.imgmap.save(file_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QFrame {
        background-color: #3f3f3f;
    }
                      
    QPushButton {
        border-radius: 5px;
        background-color: rgb(60, 90, 255);
        padding: 10px;
        color: white;
        font-weight: bold;
        font-family: Arial;
        font-size: 12px;
    }
                      
    QPushButton::hover {
        background-color: rgb(60, 20, 255)
    }
    """)
    selector = ScreenRegionSelector()
    selector.show()
    app.exit(app.exec_())
