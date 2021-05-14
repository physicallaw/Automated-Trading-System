import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *

from AutoExch import *

class MyWindow(QMainWindow):
    ###------------------------- 초기화 -------------------------###
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyStock")
        self.setGeometry(20, 50, 190, 105)
        self.setFixedSize(600,600)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        self.kiwoom.connect(self.kiwoom, SIGNAL("OnEventConnect(int)"), self.OnEventConnect)
        self.kiwoom.connect(self.kiwoom, SIGNAL("OnReceiveMsg(QString, QString, QString, QString)"), self.OnReceiveMsg)
        self.kiwoom.connect(self.kiwoom, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)
        self.kiwoom.connect(self.kiwoom, SIGNAL("OnReceiveRealCondition(QString, QString, QString, QString)"),self.OnReceiveRealCondition)

        self.number = 1001
        self.winnum = "0101"
        self.stocknum = 2001
        self.count = []
        self.stocktable = []
        self.realtable = [[],[],[],[]]
        #file = open("data.xms","r")
        #print(file.readline())
        self.switch = False
        self.setupUI()

    ###------------------------- UI -------------------------###
    def setupUI(self):
        self.basetab = QTabWidget(self)
        self.basetab.resize(602,322)
        tab = QWidget(self.basetab,)
        self.basetab.addTab(tab,"기본설정")        

        self.bt_login = QPushButton("로그인", tab)
        self.bt_login.setGeometry(10, 10, 80, 30)
        self.bt_login.clicked.connect(self.bt_login_clicked)

        self.bt_quit = QPushButton("종료", tab)
        self.bt_quit.setGeometry(100, 10, 80, 30)
        self.bt_quit.clicked.connect(self.bt_quit_clicked)

        self.bt_auto = QPushButton("자동매매", tab)
        self.bt_auto.setGeometry(100, 50, 80, 30)
        self.bt_auto.setEnabled(0)
        self.bt_auto.clicked.connect(self.bt_auto_clicked)

        self.bt_jsearch = QPushButton("기본설정", tab)
        self.bt_jsearch.setGeometry(10, 50, 80, 30)
        self.bt_jsearch.setEnabled(0)
        self.bt_jsearch.clicked.connect(self.bt_jsearch_clicked)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(0,320,600,280)
        self.tableWidget.setColumnCount(7)

        self.setTableWidgetData()
        self.show()

        #box = QWidget(tab,)
        #box.setStyleSheet("Background: rgb(190,190,190);")
        #box.setGeometry(0,85,190,20)

        self.label = QLabel("", tab)
        self.label.setGeometry(10,90,180,15)

    def setTableWidgetData(self):
        self.tableWidget.setHorizontalHeaderLabels(["종목번호","종목명","평가손익","수익률","매입가","보유수량","현재가"])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Fixed)
        self.tableWidget.verticalHeader().setHidden(True)
        self.tableWidget.horizontalHeader().resizeSection(0,83)
        self.tableWidget.horizontalHeader().resizeSection(1,83)
        self.tableWidget.horizontalHeader().resizeSection(2,83)
        self.tableWidget.horizontalHeader().resizeSection(3,83)
        self.tableWidget.horizontalHeader().resizeSection(4,83)
        self.tableWidget.horizontalHeader().resizeSection(5,83)
        self.tableWidget.horizontalHeader().resizeSection(6,83)

    def checker(self):#[strCode, state, 수량, 1]
        self.stocktable = sorted(self.stocktable)
        num1 = len(self.stocktable)
        num2 = self.tableWidget.rowCount()
        for i in range(0, num1):
            check = False
            for j in range(0, num2):
                if self.stocktable[i][0] == self.realtable[0][j] and self.stocktable[i][2] <= self.realtable[3][j]:
                    check = True
                    if self.stocktable[i][3] == 2:
                        if self.stocktable[i][1][4][0] == 3: #self.stocktable[i][1][4][1]
                            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", self.stocktable[i][0])
                            ret = self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)","호가조회", "opt10004", "0", self.stocktable[i][4])
                        elif self.stocktable[i][1][5][0] == True and self.stocktable[i][1][5][1] > self.realtable[1][j]:
                            account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
                            strCode = self.stocktable[i][0]
                            lot = self.stocktable[i][2]
                            ret = self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["매도", self.stocktable[i][4], account_num.rstrip(';'), 2, strCode, self.stocktable[i][2], lot, "03", ""])
                    if self.stocktable[i][3] == 3:
                        if self.stocktable[i][1][5][0] == True and self.stocktable[i][1][5][1] > self.realtable[1][j]:
                            account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
                            strCode = self.stocktable[i][0]
                            lot = self.stocktable[i][2]
                            ret = self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["매도", self.stocktable[i][4], account_num.rstrip(';'), 6, strCode, self.stocktable[i][2], lot, "03", "1"])
            if check == False:
                del stocktable[i]

    def searchCount(self):
        print("계좌조회중")
        account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", account_num.rstrip(';'))
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "조회구분", "2")
        ret = self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)","계좌조회", "opw00018", "0", "0101")

    def buy(self, strCode, state):
        num = len(self.stocktable)
        for i in range(0, num):
            if stocktable[i][0] == strCode and stocktable[i][1] == state:
                print("동일종목 검색됨")
                break
            else:
                self.kiwoom.dynamicCall("SetInputValue(QString, QString)", " 종목코드", strCode)
                ret = self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "매수", "opt10001", "0", strCode)
                self.stocktable.append([strCode, state, 0, 1, str(self.stocknum)]) # 1->가격조회, 2->매수완료, 3->매도주문
                self.stocknum += 1

    def sell(self, strCode, state):
        num = len(self.stocktable)
        for i in range(0, num):
            if stocktable[i][0] == strCode and stocktable[i][1] == state:
                account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
                lot = self.stocktable[i][2]
                ret = self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["매도", self.stocktable[i][4], account_num.rstrip(';'), 2, strCode, self.stocktable[i][2], lot, "03", ""])

    ###------------------------- 이벤트 처리 -------------------------###
    ### evt - 로그인

    def OnEventConnect(self, ErrCode):
        ### 5+OnEventConnect (성공시 0, 실패시 에러코드 반환)
        if ErrCode == 0:
            self.label.setText("login success")
            self.bt_jsearch.setEnabled(1)

    def OnReceiveTrData(self, ScrNo, RQName, TrCode, RecordName, PrevNext, DataLength, ErrorCode, Message, SplmMsg):
        if RQName == "종료":
            num = len(self.count)
            for i in range(0,num):
                if int(ScrNo) == self.count[i][0]:
                    self.count[i][1].setParent(None)
                    del self.count[i] 
                    break

        if RQName == "호가조회":
            num1 = len(self.stocktable)
            num2 = self.tableWidget.rowCount()
            for i in range(0,num1):
                if self.stocktable[i][4] == ScrNo:
                    for j in range(0,num2):
                        if self.stocktable[i][0] == self.realtable[0][j]:
                            self.stocktable[i][3] = 3
                            strCode = self.stocktable[i][0]
                            for k in ["매도최우선호가","매도2차선호가","매도3차선호가","매도4차선호가","매도5차선호가","매도6차선호가","매도7차선호가","매도8차선호가","매도9차선호가","매도10차선호가"]:
                                temp = abs(int(self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", [TrCode, "", RQName, 0, k])))
                                if (float(self.realtable[2][j]-temp)/temp*100-0.33) > self.stocktable[i][1][4][1]:
                                    account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
                                    ret = self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["매도", self.stocktable[i][4], account_num.rstrip(';'), 2, strCode, self.stocktable[i][2], int(temp), "03", ""])
                                    break


        if RQName == "매수":
            stockcode = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", [TrCode, "", RQName, 0, "종목코드"])
            stockprice = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", [TrCode, "", RQName, 0, "상한가"])
            num = len(self.stocktable)
            for i in range(0, num):
                if self.stocktable[i][0] == stockcode and self.stocktable[i][3] == 1:
                    lot = int(self.stocktable[i][1][0])/int(stockprice)
                    account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
                    ret = self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["매수", self.stocktable[i][4], account_num.rstrip(';'), 1, stockcode, lot, 0, "03", ""])           
                    self.stocktable[i][2] = lot
                    self.stocktable[i][3] = 2
                    break

        if RQName == "계좌조회":
            #print(self, ScrNo, RQName, TrCode, RecordName, PrevNext)
            self.tableWidget.clearContents()
            num = int(self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", [TrCode, "", RQName, 0, "조회건수"]))
            self.realtable = [[],[],[],[]]
            self.tableWidget.setRowCount(num)
            for i in range(0,num):
                scode = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", [TrCode, "", RQName, i, "종목번호"]).strip()
                self.tableWidget.setItem(i,0,QTableWidgetItem(scode[1:7]))
                self.realtable[0].append(scode[1:7])
                self.tableWidget.setItem(i,1,QTableWidgetItem(self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", [TrCode, "", RQName, i, "종목명"])))
                temp = int(self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", [TrCode, "", RQName, i, "평가손익"]))
                self.tableWidget.setItem(i,2,QTableWidgetItem(str(temp)))
                temp = float(self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", [TrCode, "", RQName, i, "수익률(%)"]))
                self.tableWidget.setItem(i,3,QTableWidgetItem(str(temp)))
                self.realtable[1].append(temp)
                temp = int(self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", [TrCode, "", RQName, i, "매입가"]))
                self.tableWidget.setItem(i,4,QTableWidgetItem(str(temp)))
                self.realtable[2].append(temp)
                temp = int(self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", [TrCode, "", RQName, i, "보유수량"]))
                self.tableWidget.setItem(i,5,QTableWidgetItem(str(temp)))
                self.realtable[3].append(temp)
                temp = int(self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", [TrCode, "", RQName, i, "현재가"]))
                self.tableWidget.setItem(i,6,QTableWidgetItem(str(temp)))
            self.checker()
            QTimer.singleShot(10000, lambda: self.searchCount())

    def OnReceiveRealCondition(self, strCode, strType, strConditionName, strConditionIndex):
        num = len(self.count)
        time = QTime.currentTime()
        for i in range(0, num):
            if strType == "I":
                if strConditionIndex == self.count[i][1].state[2]:
                    if self.count[i][1].state[1][0] == True:
                        if self.count[i][1].state[1][1] > time or self.count[i][1].state[1][2] < time:
                            break
                    self.buy(strCode, self.count[i][1].state)
                if self.count[i][1].state[4][0] == 2 and strConditionIndex == self.count[i][1].state[4][1]:
                    if self.count[i][1].state[3][0] == True:
                        if self.count[i][1].state[3][1] > time or self.count[i][1].state[3][2] < time:
                            break
                    self.sell(strCode, self.count[i][1].state)
            if strType == "D" and self.count[i][1].state[4][0] == 1:
                if self.count[i][1].state[3][0] == True:
                    if self.count[i][1].state[3][1] > time or self.count[i][1].state[3][2] < time:
                        break
                self.sell(strCode, self.count[i][1].state)
            #account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
            #ret = self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["매수", self.number, account_num.rstrip(';'), 1, strCode, 1, 0, "03", ""])           
            #account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
            #ret = self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["매도", self.number, account_num.rstrip(';'), 2, strCode, 1, 0, "03", ""])

    ### evt - 메시지
    def OnReceiveMsg(self, ScrNo, RQName, TrCode, Msg):
        print(ScrNo, RQName, TrCode, Msg)

    ###------------------------- 버튼 처리 -------------------------###
    ### bt - 로그인   
    def bt_login_clicked(self): 
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            ### 1.CommConnect (성공시 0 리턴 -> OnEventConnect이벤트 발생)
            ret = self.kiwoom.dynamicCall("CommConnect()")
        else:
            self.label.setText("이미 로그인중입니다")     

    ### bt - 종료
    def bt_quit_clicked(self): 
        if self.kiwoom.dynamicCall("GetConnectState()") == 1:
            ret = self.kiwoom.dynamicCall("CommTerminate()")
        self.close()
        self.setParent(None)

    ### bt - 조건검색
    def bt_jsearch_clicked(self):
        if self.kiwoom.dynamicCall("GetConditionLoad()"):
            self.label.setText("조건검색 성공")
            self.bt_auto.setEnabled(1)  
        else:
            self.label.setText("조건검색 실패")
        if self.switch == False:
            self.searchCount()
            self.switch == True

    #### bt - 자동매매
    def bt_auto_clicked(self):
        self.count.append([self.number,AutoExch(self.number, self.kiwoom)])
        num = len(self.count)
        self.basetab.addTab(self.count[num-1][1],str(self.number))
        self.number += 1
        self.basetab.setCurrentIndex(num+1)

###------------------------- main 실행 -------------------------###
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()