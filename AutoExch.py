import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *

class AutoExch(QMainWindow):
    ###------------------------- 초기화 -------------------------###
    def __init__(self, num, kiwoom):
        super().__init__()
        
        self.winnum = str(num)
        self.setWindowTitle("자동매매 : " + str(num))
        self.setFixedSize(600,300)

        self.kiwoom = kiwoom

        list = self.kiwoom.dynamicCall("GetConditionNameList()")
        list = list.split(';')
        self.jolist = []
        for i in range(0,len(list)-1):
            self.jolist.append(list[i].split('^'))

        self.switch = [False,False,False]
        self.state = [0,[0,0,0],[0],[0,0,0],[0,0],[0,0],[0,0],[0,0]]
        self.setupUI()

    ###------------------------- UI -------------------------###
    def setupUI(self):

        ### 기본설정
        object = [[],[],[]]
        self.button = [[],[],[]]
        self.layout = []

        self.layout.append(QGroupBox("매수설정",self)) #layout[0]
        self.layout[0].setGeometry(5,10,285,245)

        self.layout.append(QGroupBox("매도설정",self)) #layout[1]
        self.layout[1].setGeometry(300,10,285,245)

        object[2].append(QTime(9,0,0,0)) #object[2][0]
        object[2].append(QTime(15,20,0,0)) #object[2][1]

        ### 매수창
        self.button[0].append(QCheckBox("매수시간지정",self.layout[0])) #button[0][0]
        self.button[0][0].setGeometry(10,15,100,20)
        self.button[0][0].clicked.connect(self.bt0f)

        self.button[0].append(QTimeEdit(self.layout[0])) #button[0][1]
        self.button[0][1].setTimeRange(object[2][0], object[2][1])
        self.button[0][1].setGeometry(10,40,100,20)
        self.button[0][1].setTime(object[2][0])
        self.button[0][1].setEnabled(0)

        object[0].append(QLabel("~",self.layout[0],)) #object[0][0]
        object[0][0].setGeometry(115,45,10,10)

        self.button[0].append(QTimeEdit(self.layout[0])) #button[0][2]
        self.button[0][2].setTimeRange(object[2][0], object[2][1])
        self.button[0][2].setGeometry(130,40,100,20)
        self.button[0][2].setTime(object[2][1])
        self.button[0][2].setEnabled(0)

        object[0].append(QWidget(self.layout[0],)) #object[0][1]
        object[0][1].setStyleSheet("border: 1px solid rgb(190,190,190);")
        object[0][1].setGeometry(10,70,270,1)

        object[0].append(QLabel("조건",self.layout[0],)) #object[0][2]
        object[0][2].setGeometry(10,80,280,20)

        self.button[0].append(QComboBox(self.layout[0])) #button[0][3]
        self.button[0][3].setGeometry(40,80,90,20)
        for i in range(0,len(self.jolist)):
           self.button[0][3].addItem(self.jolist[i][1],)

        object[0].append(QLabel("에 편입시 시장가에 매수",self.layout[0],)) #object[0][3]
        object[0][3].setGeometry(130,80,280,20)

        object[0].append(QWidget(self.layout[0],)) #object[0][4]
        object[0][4].setStyleSheet("border: 1px solid rgb(190,190,190);")
        object[0][4].setGeometry(10,155,270,1)

        object[0].append(QLabel("1회 매수 금액 : ",self.layout[0],)) #object[0][5]
        object[0][5].setGeometry(10,165,100,20)

        self.button[0].append(QSpinBox(self.layout[0])) #button[0][4]
        self.button[0][4].setGeometry(100,165,80,20)
        self.button[0][4].setRange(10000,1000000)
        self.button[0][4].setSingleStep(10000)

        ### 매도창
        self.button[1].append(QCheckBox("매도시간지정",self.layout[1])) #button[1][0]
        self.button[1][0].setGeometry(10,15,100,20)
        self.button[1][0].clicked.connect(self.bt1f)

        self.button[1].append(QTimeEdit(self.layout[1])) #button[1][1]
        self.button[1][1].setTimeRange(object[2][0], object[2][1])
        self.button[1][1].setGeometry(10,40,100,20)
        self.button[1][1].setTime(object[2][0])
        self.button[1][1].setEnabled(0)

        object[1].append(QLabel("~",self.layout[1],)) #object[1][0]
        object[1][0].setGeometry(115,45,10,10)

        self.button[1].append(QTimeEdit(self.layout[1])) #button[1][2]
        self.button[1][2].setTimeRange(object[2][0], object[2][1])
        self.button[1][2].setGeometry(130,40,100,20)
        self.button[1][2].setTime(object[2][1])
        self.button[1][2].setEnabled(0)

        object[1].append(QWidget(self.layout[1],)) #object[1][1]
        object[1][1].setStyleSheet("border: 1px solid rgb(190,190,190);")
        object[1][1].setGeometry(10,70,270,1)

        self.button[1].append(QRadioButton("조건 이탈시 매도", self.layout[1])) #button[1][3]
        self.button[1][3].setGeometry(10,80,200,20)
        self.button[1][3].setChecked(1)

        self.button[1].append(QRadioButton(self.layout[1])) #button[1][4]
        self.button[1][4].setGeometry(10,105,20,20)

        object[1].append(QLabel("조건",self.layout[1],)) #object[1][2]
        object[1][2].setGeometry(30,105,280,20)

        self.button[1].append(QComboBox(self.layout[1])) #button[1][5]
        self.button[1][5].setGeometry(60,105,90,20)
        for i in range(0,len(self.jolist)):
           self.button[1][5].addItem(self.jolist[i][1],)

        object[1].append(QLabel("에 편입시 시장가에 매도",self.layout[1],)) #object[1][3]
        object[1][3].setGeometry(150,105,280,20)

        self.button[1].append(QRadioButton(self.layout[1])) #button[1][6]
        self.button[1][6].setGeometry(10,130,200,20)

        self.button[1].append(QDoubleSpinBox(self.layout[1])) #button[1][7]
        self.button[1][7].setGeometry(30,130,45,20)
        self.button[1][7].setRange(0,10)
        self.button[1][7].setSingleStep(0.1)
        self.button[1][7].setValue(2)

        object[1].append(QLabel("%시 익절",self.layout[1],)) #object[1][4]
        object[1][4].setGeometry(75,130,280,20)

        object[1].append(QWidget(self.layout[1],)) #object[1][5]
        object[1][5].setStyleSheet("border: 1px solid rgb(190,190,190);")
        object[1][5].setGeometry(10,155,270,1)

        self.button[1].append(QCheckBox(self.layout[1])) #button[1][8]
        self.button[1][8].setGeometry(10,165,100,20)

        self.button[1].append(QDoubleSpinBox(self.layout[1])) #button[1][9]
        self.button[1][9].setGeometry(30,165,50,20)
        self.button[1][9].setRange(-50,0)
        self.button[1][9].setSingleStep(0.1)
        self.button[1][9].setValue(-2)

        object[1].append(QLabel("%시 손절",self.layout[1],)) #object[1][6]
        object[1][6].setGeometry(80,165,280,20)

        self.button[1].append(QCheckBox("장 종료",self.layout[1])) #button[1][10]
        self.button[1][10].setGeometry(10,190,100,20)

        self.button[1].append(QSpinBox(self.layout[1])) #button[1][11]
        self.button[1][11].setGeometry(70,190,35,20)
        self.button[1][11].setRange(0,180)
        self.button[1][11].setValue(10)

        object[1].append(QLabel("분 전에 일괄 매도",self.layout[1],)) #object[1][7]
        object[1][7].setGeometry(105,190,280,20)

        self.button[1].append(QCheckBox("매수 후",self.layout[1])) #button[1][12]
        self.button[1][12].setGeometry(10,215,100,20)

        self.button[1].append(QSpinBox(self.layout[1])) #button[1][13]
        self.button[1][13].setGeometry(70,215,35,20)
        self.button[1][13].setRange(0,180)
        self.button[1][13].setValue(10)

        object[1].append(QLabel("분 후에 일괄 매도",self.layout[1],)) #object[1][8]
        object[1][8].setGeometry(105,215,280,20)

        ### 버튼, 거래내역

        self.button[2].append(QPushButton("매매시작", self)) #button[2][0]
        self.button[2][0].setGeometry(420, 260, 80, 30)
        self.button[2][0].clicked.connect(self.bt_login_clicked)

        self.button[2].append(QPushButton("종료", self)) #button[2][1]
        self.button[2][1].setGeometry(510, 260, 80, 30)
        self.button[2][1].clicked.connect(self.bt_quit_clicked)

  
    ###------------------------- 이벤트 처리 -------------------------###

    ### evt - TR

    def getdata(self):
            self.state[0] = self.button[0][4].text()
            self.state[1][0] = self.button[0][0].isChecked()
            self.state[1][1] = self.button[0][1].time()
            self.state[1][2] = self.button[0][2].time()
            self.state[2] = self.button[0][3].currentIndex()
            self.state[3][0] = self.button[1][0].isChecked()
            self.state[3][1] = self.button[1][1].time()
            self.state[3][2] = self.button[1][2].time()
            if self.button[1][3].isChecked():
                self.state[4][0] = 1
            elif self.button[1][4].isChecked():
                self.state[4][0] = 2
                self.state[4][1] = self.button[1][5].currentIndex()
            else:
                self.state[4][0] = 3
                self.state[4][1] = float(self.button[1][7].text())
            self.state[5][0] = self.button[1][8].isChecked()
            self.state[5][1] = float(self.button[1][9].text())
            self.state[6][0] = self.button[1][10].isChecked()
            self.state[6][1] = int(self.button[1][11].text())
            self.state[7][0] = self.button[1][12].isChecked()
            self.state[7][1] = int(self.button[1][13].text())       

    ###------------------------- 버튼 처리 -------------------------###
    ### bt - 매수시작   
    def bt_login_clicked(self): 
        if self.switch[0] == False:
            self.layout[0].setEnabled(0)
            self.layout[1].setEnabled(0)
            self.button[2][1].setEnabled(0)
            self.button[2][0].setText("매매중단")
            self.switch[0] = True
            self.getdata()
            self.kiwoom.dynamicCall("SendCondition(QString, QString, int, int)",self.winnum,self.jolist[self.state[2]][1],int(self.jolist[self.state[2]][0]), 1)
            if self.state[4][0] == 2:
                self.kiwoom.dynamicCall("SendCondition(QString, QString, int, int)",self.winnum,self.jolist[self.state[4][1]][1],int(self.jolist[self.state[4][1]][0]), 1)
        else:
            self.layout[0].setEnabled(1)
            self.layout[1].setEnabled(1)
            self.button[2][1].setEnabled(1)
            self.button[2][0].setText("매매시작")            
            self.switch[0] = False
            self.kiwoom.dynamicCall("SendConditionStop(QString, QString, int)",self.winnum,self.jolist[self.state[2]][1],int(self.jolist[self.state[2]][0]))
            if self.state[4][0] == 2:
                self.kiwoom.dynamicCall("SendConditionStop(QString, QString, int)",self.winnum,self.jolist[self.state[4][1]][1],int(self.jolist[self.state[4][1]][0]))

    def bt0f(self):
        if self.switch[1] == False:
            self.switch[1] = True
            self.button[0][1].setEnabled(1)
            self.button[0][2].setEnabled(1)
        else:
            self.switch[1] = False
            self.button[0][1].setEnabled(0)
            self.button[0][2].setEnabled(0)

    def bt1f(self):
        if self.switch[2] == False:
            self.switch[2] = True
            self.button[1][1].setEnabled(1)
            self.button[1][2].setEnabled(1)
        else:
            self.switch[2] = False
            self.button[1][1].setEnabled(0)
            self.button[1][2].setEnabled(0)

    ### bt - 종료
    def bt_quit_clicked(self): 
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", " 종목코드", "000660")
        ret = self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "종료", "opt10001", "0", self.winnum)