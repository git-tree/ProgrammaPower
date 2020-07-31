# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\ProgrammaPower\test\power_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
StyleSheet = '''
/*设置红色进度条*/
#progressBar {
    border: 2px solid #2196F3;/*边框以及边框颜色*/
    border-radius: 5px;
    background-color: #E0E0E0;
    max-height: 12px;
    text-align: center; /*进度值居中*/
}
#progressBar::chunk {
    background-color: #2196F3;
    width: 10px; /*区块宽度*/
    margin: 0.5px;
}'''

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(674, 462)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.btn_checkdevice = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(False)
        font.setWeight(50)
        self.btn_checkdevice.setFont(font)
        self.btn_checkdevice.setObjectName("btn_checkdevice")
        self.gridLayout.addWidget(self.btn_checkdevice, 0, 0, 1, 1)
        self.tip = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.tip.setFont(font)
        self.tip.setStyleSheet("color: rgb(0, 170, 0);")
        self.tip.setText("")
        self.tip.setObjectName("tip")
        self.gridLayout.addWidget(self.tip, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_6.addWidget(self.label_5, 2, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 5, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem3, 3, 1, 1, 1)
        self.lcd_a = QtWidgets.QLCDNumber(self.centralWidget)
        self.lcd_a.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(6, 255, 118);")
        self.lcd_a.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcd_a.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_a.setDigitCount(15)
        self.lcd_a.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_a.setObjectName("lcd_a")
        self.gridLayout_6.addWidget(self.lcd_a, 3, 2, 3, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem4, 1, 2, 1, 1)
        self.lcd_v = QtWidgets.QLCDNumber(self.centralWidget)
        self.lcd_v.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(6, 255, 118);")
        self.lcd_v.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcd_v.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_v.setDigitCount(15)
        self.lcd_v.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_v.setObjectName("lcd_v")
        self.gridLayout_6.addWidget(self.lcd_v, 3, 0, 3, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem5, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_6.addWidget(self.label_4, 2, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.progressBar.setStyleSheet(StyleSheet)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_6.addWidget(self.progressBar, 0, 0, 1, 3)
        # self.progressBar.setVisible(False)
        self.gridLayout_2.addLayout(self.gridLayout_6, 5, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btn_turnon = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.btn_turnon.setFont(font)
        self.btn_turnon.setObjectName("btn_turnon")
        self.gridLayout_4.addWidget(self.btn_turnon, 4, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem6, 0, 0, 1, 1)
        self.txt_min = QtWidgets.QDoubleSpinBox(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.txt_min.setFont(font)
        self.txt_min.setDecimals(1)
        self.txt_min.setSingleStep(0.5)
        self.txt_min.setObjectName("txt_min")
        self.gridLayout_4.addWidget(self.txt_min, 1, 2, 1, 1)
        self.btn_input = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.btn_input.setFont(font)
        self.btn_input.setObjectName("btn_input")
        self.gridLayout_4.addWidget(self.btn_input, 1, 3, 1, 1)
        self.btn_startTest = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.btn_startTest.setFont(font)
        self.btn_startTest.setObjectName("btn_startTest")
        self.gridLayout_4.addWidget(self.btn_startTest, 5, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 2, 1, 1, 1)
        self.tip_switch = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.tip_switch.setFont(font)
        self.tip_switch.setText("")
        self.tip_switch.setObjectName("tip_switch")
        self.gridLayout_4.addWidget(self.tip_switch, 4, 3, 1, 1)
        self.txt_v = QtWidgets.QDoubleSpinBox(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(False)
        font.setWeight(50)
        self.txt_v.setFont(font)
        self.txt_v.setDecimals(4)
        self.txt_v.setSingleStep(0.0001)
        self.txt_v.setProperty("value", 0.0)
        self.txt_v.setObjectName("txt_v")
        self.gridLayout_4.addWidget(self.txt_v, 0, 2, 1, 1)
        self.txt_second = QtWidgets.QSpinBox(self.centralWidget)
        self.txt_second.setObjectName("txt_second")
        self.gridLayout_4.addWidget(self.txt_second, 2, 2, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem7, 0, 6, 1, 1)
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_4.addWidget(self.line, 3, 2, 1, 1)
        self.tip_starttest = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.tip_starttest.setFont(font)
        self.tip_starttest.setText("")
        self.tip_starttest.setObjectName("tip_starttest")
        self.gridLayout_4.addWidget(self.tip_starttest, 5, 3, 1, 1)
        self.btn_searchinput = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.btn_searchinput.setFont(font)
        self.btn_searchinput.setObjectName("btn_searchinput")
        self.gridLayout_4.addWidget(self.btn_searchinput, 1, 4, 1, 1)
        self.btn_clearinput = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.btn_clearinput.setFont(font)
        self.btn_clearinput.setObjectName("btn_clearinput")
        self.gridLayout_4.addWidget(self.btn_clearinput, 1, 5, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.btn_stop.setFont(font)
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout_4.addWidget(self.btn_stop, 5, 4, 1, 1)
        self.btn_report = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.btn_report.setFont(font)
        self.btn_report.setObjectName("btn_report")
        self.gridLayout_4.addWidget(self.btn_report, 5, 5, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_4, 2, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.gridLayout_2.addItem(spacerItem8, 1, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 3, 0, 1, 1)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_10.addWidget(self.textEdit, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_10, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "电流测试_1.0"))
        self.btn_checkdevice.setText(_translate("MainWindow", "检查连接"))
        self.label_5.setText(_translate("MainWindow", "当前电流:"))
        self.label_4.setText(_translate("MainWindow", "当前电压:"))
        self.btn_turnon.setText(_translate("MainWindow", "打开/关闭开关"))
        self.label.setText(_translate("MainWindow", "设置电压(VolTage):"))
        self.btn_input.setText(_translate("MainWindow", "录入数据"))
        self.btn_startTest.setText(_translate("MainWindow", "开始测试(Measure)"))
        self.label_2.setText(_translate("MainWindow", "设置时长(分钟):"))
        self.label_3.setText(_translate("MainWindow", "设置间隔(秒):"))
        self.btn_searchinput.setText(_translate("MainWindow", "查询已录入"))
        self.btn_clearinput.setText(_translate("MainWindow", "清空录入"))
        self.btn_stop.setText(_translate("MainWindow", "停止测试"))
        self.btn_report.setText(_translate("MainWindow", "生成图表"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
