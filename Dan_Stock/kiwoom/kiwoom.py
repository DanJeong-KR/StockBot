from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errorCode import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("start Kiwoom() class")

        self.login_event_loop = QEventLoop()

        ### Properties
        self.account_num = None
        self.deposit = 0 # 예수금
        self.use_money = 0 # 실제 투자에 사용할 금액
        self.use_money_percent = 0.5 # 예수금 기준 실제 사용할 비율
        self.output_deposit = 0 # 출력 가능 금액

        self.screen_my_info = "2000" # 계좌 관련 스크린 번호

        ### init  funcs
        self.get_ocx_instance()
        self.event_slots() # 키움과 연결을 위한 시그널, 슬롯 모음
        self.signal_login_commConnect() # 로그인 요청
        self.get_account_info()
        self.detail_account_info()


    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.onReceiveTrData.connect(self.trDa)

    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    def login_slot(self, err_code):
        print(errors(err_code)[1])
        self.login_event_loop.exit()

    def trdata_slot(self, sScNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == "예수금상세현황요청":
            deposit = self.dynamicCall("GetCommData(QString, QString)")

    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(Qstring)", "ACCNO") # 계좌번호 반환
        account_num = account_list.split(";")[0]

        self.account_num = account_num

        print("계좌번호 : {}".format(account_num))

    def detail_account_info(self, sPrevNext = 0):
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "예수금상세현황요청", "opw00001", sPrevNext, self.screen_my_info)