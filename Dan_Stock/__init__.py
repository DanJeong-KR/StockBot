from kiwoom.kiwoom import *
from PyQt5.QtWidgets import *
import sys


class Main():
    def __init__(self):
        print("Start Main func")

        self.app = QApplication(sys.argv)  # PyQt5로 실행할 파일명 자동 설정
        self.kiwoom = Kiwoom()
        self.app.exec_() # Excute Event Loop / 프로그램 종료 안되게



if __name__ == "__main__":
    Main()