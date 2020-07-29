# -*- coding: utf-8 -*-

"""
Module implementing controller_main.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from Ui_power_main import Ui_MainWindow
import pyvisa,time,threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

class controller_main(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(controller_main, self).__init__(parent)
        self.setupUi(self)
        # power超时时间
        self.timeout=3000
        # 是否在检查设备
        self.ischecking=False
        # 设备是否可用
        self.powerok=False
        # 设备
        self.power=None
        # 插入的数据
        self.testinfodict=[]#显示用
        self.testdata=[]# 真的数据
        # 开关是否打开
        self.isOUTPutOn=False
        # 刷新显示电压
        self.isfreshV=False
        # 刷新显示电流
        self.isfreshA=False
        # 正在测试（已经开始测试）
        self.isTesting=False
    @pyqtSlot()
    def on_btn_checkdevice_clicked(self):
        """
        检查连接...
        """
        if not self.power is None and self.powerok:
            self.showmsg("已连接.")
            return
        if self.ischecking:
            self.showmsg("正在检查...")
            return
        t=threading.Thread(target=self.check_connect)
        self.ischecking=True
        t.start()
    @pyqtSlot()
    def on_btn_turnon_clicked(self):
        """
        打开/关闭开关
        """
        if self.power is not None:
            if self.isOUTPutOn:
                self.power.write("*RST")
                self.power.write("*CLS")
                self.power.write("OUTPut OFF")
                self.isOUTPutOn=False
                self.switchtip("×测试开关已关闭",False)
            else:
                self.power.write("*RST")
                self.power.write("*CLS")
                # self.power.write("VOLTage 2.36001")
                self.power.write("OUTPut ON")
                self.switchtip("√测试开关已打开",True)
                self.isOUTPutOn=True
        else:
            self.showmsg("未检查到电源！")
    @pyqtSlot()
    def on_btn_input_clicked(self):
        """
        录入数据
        """
        get_v=self.txt_v.text()
        get_min=self.txt_min.text()
        get_steptime=self.txt_second.text()
        if get_v=='0.0000' or get_min=='0.0':
            self.showmsg('电压或时间不能设置为0')
            return
        self.testinfodict.append("电压【%sV】下测试【%s分钟】,间隔【%s秒】后测试下一组"%(get_v,get_min,get_steptime))
        # self.insert2textedit('录入成功,当前数据:%s'%self.testinfodict)
        self.testdata.append("%s-%s-%s"%(get_v,get_min,get_steptime))
        self.insert2textedit("录入成功!")
    @pyqtSlot()
    def on_btn_searchinput_clicked(self):
        """
        查询录入的数据
        """
        print(self.testdata)
        self.insert2textedit("当前数据:")
        for i in range(len((self.testdata))):
            self.insert2textedit("第%d组测试任务:%s"%(i+1,self.testinfodict[i]))
    @pyqtSlot()
    def on_btn_clearinput_clicked(self):
        """
        清空录入的数据
        """
        if len(self.testdata)==0:
            self.insert2textedit("暂无数据")
            return
        self.showmsg_sure("你确定清空录入的数据吗?")
    @pyqtSlot()
    def on_btn_startTest_clicked(self):
        """
        开始测试
        """
        if self.power is None:
            self.showmsg("未检查到电源！")
            return
        if len(self.testdata)==0:
            self.showmsg("请添加测试数据!")
            return
        if not self.isOUTPutOn:
            self.showmsg("请打开开关!")
            return
        if self.isTesting:
            self.showmsg("请停止运行的测试任务后重试!")
            return
        t=threading.Thread(target=self.startTest,args=(self.testdata,))
        self.isTesting=True
        t.start()
    @pyqtSlot()
    def on_textEdit_textChanged(self):
        """
        光标最下
        """
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End) # 还可以有别的位置
        self.textEdit.setTextCursor(cursor)
    @pyqtSlot()
    def closeEvent(self, event):
        '''
        :param event: 窗口关闭事件
        '''
        reply = QtWidgets.QMessageBox.question(self, '提示', '确定要退出吗?',QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            if not self.power is None:
                if self.isfreshV:
                    self.isfreshV=False
                if self.isfreshA:
                    self.isfreshA=False
                if self.isTesting:
                    self.isTesting=False
                self.power.write("*RST")
                self.power.write("*CLS")
                self.power.write("OUTPut OFF")
            event.accept()
        else:
            event.ignore()
    def startTest(self,data):
        for i in range(len(data)):
            print(data[i])
            work1=str(data[i]).split('-')
            testv=work1[0]
            testt=int(float(work1[1])*60)
            testwait=int(work1[2])
            print("电压%s,时间%s,间隔%s"%(testv,testt,testwait))
            # self.isfreshV=False
            # self.isfreshA=False
            time.sleep(2)
            # self.power.write("*RST")
            self.power.write("*CLS")
            self.power.write("VOLTage %s"%testv)
            for t in range(testt):
                print(t)
                if self.isTesting:
                    self.power.write("*CLS")
                    aNum=float(self.power.query("MEAS:CURR?"))
                    print(aNum)
                    time.sleep(1)
                else:
                    return
            print("准备间隔...")
            for w in range(testwait):
                print('正在休息.%d'%w)
                time.sleep(1)
    def readV(self):
        """
        读取电压
        """
        while self.isfreshV:
            self.power.write("*CLS")
            vNum=float(self.power.query("MEAS:VOLT?"))
            self.lcd_v.display(vNum)
            time.sleep(1)
    def readA(self):
        """
        读取电流
        """
        while self.isfreshA:
            time.sleep(1)
            self.power.write("*CLS")
            aNum=float(self.power.query("MEAS:CURR?"))
            self.lcd_a.display(aNum)
    def check_connect(self):
        """
        检查连接
        """
        self.btn_checkdevice.setEnabled(False)
        self.btn_checkdevice.setText("正在检查...")
        rm = pyvisa.ResourceManager("c:/windows/system32/visa32.dll")
        print("resource:\t",rm.list_resources())
        # 检查所有线
        allLine=rm.list_resources()
        # 线材名
        GPIB_Line_name=""
        # 是否有线材
        isLineFind=False
        # 是否有电源设备
        isPowerFind=False
        # 电源
        power=None
        # 电源信息
        power_info=''
        for i in range(len(allLine)):
            if 'GPIB' in str(allLine[i]):
                GPIB_Line_name= str(allLine[i])
                isLineFind=True
                break
        print("GPIB数据线:"+GPIB_Line_name)
        # 有数据线连接
        if isLineFind:
            # 检查电源,通过线材连接打开
            try:
                power=rm.open_resource(GPIB_Line_name)
                power_info="程控电源设备信息:"+str(power.query("*IDN?"))
                isPowerFind=True
            except:
                power_info="未检查到设备"
        if isLineFind and isPowerFind:
            self.tip_ok("GPIB地址:"+GPIB_Line_name+"\n"+power_info)
            self.powerok=True
            self.power=power
            self.power.write("*RST")
            self.power.write("*CLS")
            self.power.write("OUTPut OFF")
            self.power.timeout=3000

            t_readv=threading.Thread(target=self.readV)
            self.isfreshV=True

            t_readA=threading.Thread(target=self.readA)
            self.isfreshA=True

            t_readv.start()
            t_readA.start()
        else:
            self.tip_error("未发现设备，请确保打开电源后重试！")
        self.btn_checkdevice.setEnabled(True)
        self.btn_checkdevice.setText("检查连接")
        self.ischecking=False
    def tip_ok(self,msg):
        """
        成功提示
        """
        self.tip.setStyleSheet("color: rgb(0, 170, 0);")
        self.tip.setText(msg)
    def tip_error(self,msg):
        """
        失败提示
        """
        self.tip.setStyleSheet("color: rgb(255, 0, 0);")
        self.tip.setText(msg)
    def showmsg(self,msg):
        QMessageBox.information(self,'提示',str(msg), QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
    def showmsg_sure(self,msg):
        reply =QMessageBox.information(self,'提示',str(msg), QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
        if reply == QMessageBox.Ok:
            self.testdata.clear()
            self.testinfodict.clear()
            self.insert2textedit("操作成功！")
        else:
            print("no")
    def insert2textedit(self,msg):
        self.textEdit.insertPlainText("\n"+str(msg))
    def switchtip(self,msg,isok):
        """
        打开/关闭开关右边提示
        """
        if isok:
            # 绿色
            self.tip_switch.setStyleSheet("color: rgb(0, 170, 0);")
        else:
            # 红色
            self.tip_switch.setStyleSheet("color: rgb(255, 0, 0);")
        self.tip_switch.setText(str(msg))
    def starttestbtntip(self,msg,isok):
        """
        开始按钮右边提示
        """
        if isok:
            # 绿色
            self.tip_starttest.setStyleSheet("color: rgb(0, 170, 0);")
        else:
            # 红色
            self.tip_starttest.setStyleSheet("color: rgb(255, 0, 0);")
        self.tip_starttest.setText(str(msg))


        # ('GPIB1::0::INSTR', 'ASRL1::INSTR', 'ASRL3::INSTR', 'ASRL10::INSTR')
        # inst = rm.open_resource('GPIB1::0::INSTR')
        # inst.timeout=self.timeout
        # print("inst:\t",inst)
        # print("设备信息\t",inst.query("*IDN?"))
        # print("错误信息\t",inst.query("*Esr?"))
        # inst.write("*RST")
        # 开启开关
        # inst.write("OUTPut ON")
        # 设置电压
        # inst.write("VOLTage 2.9")
        # time.sleep(3)
        # 关闭开关
        # inst.write("OUTPut OFF")
        # 当前电压
        # print(self.power.query("MEAS:VOLT?"))