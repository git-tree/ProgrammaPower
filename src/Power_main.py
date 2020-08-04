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
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
import os
from numpy import *

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
        # 生成数据
        self.log=None
        self.dir_name=None
        self.startfresh=True
        # 进度条相关
        self.thread_progress=None
    @pyqtSlot()
    def on_btn_checkdevice_clicked(self):
        """
        检查连接...
        """
        try:
            rm = pyvisa.ResourceManager("C:/windows/system32/visa32.dll")
        except:
            self.showmsg("未找到C:/windows/system32/visa32.dll文件，请配置电流测试环境！")
            return
        if not self.power is None and self.powerok:
            self.showmsg("已连接.")
            return
        if self.ischecking:
            self.showmsg("正在检查...")
            return
        t=threading.Thread(target=self.check_connect)
        self.ischecking=True
        t.setDaemon(True)
        t.start()
    @pyqtSlot()
    def on_btn_turnon_clicked(self):
        """
        打开/关闭开关
        """
        if self.power is  None:
            self.showmsg("未检查到电源！")
            return
        if self.isTesting:
            self.showmsg("正在测试,请勿关闭电源!")
            return
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
    @pyqtSlot()
    def on_btn_input_clicked(self):
        """
        录入数据
        """
        if self.isTesting:
            self.showmsg("请等待测试任务完成,再录入数据!")
            return
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
        if self.isTesting:
            self.insert2textedit("请等待测试完成!")
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
        self.startfresh=False
        time.sleep(2)
        t=threading.Thread(target=self.startTest,args=(self.testdata,))
        self.isTesting=True
        t.setDaemon(True)
        t.start()
    @pyqtSlot()
    def on_btn_stop_clicked(self):
        """
        停止测试
        """
        print("stop被点击")
        if not self.isTesting:
            self.showmsg("当前无任务!")
            return
        reply = QtWidgets.QMessageBox.question(self, '提示', '确定要停止吗?',QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
        if reply == QMessageBox.Ok:
            self.isTesting=False
            time.sleep(2)
            self.startfresh=True
            # if not self.power is None:
            #     # self.power.write("*RST")
            #     self.power.write("*CLS")
            #     self.power.write("IOCLEAR")
            #     self.power.write("OUTPut OFF")
            #     self.isOUTPutOn=False
            #     self.switchtip("电源已关闭",False)
            self.resetPower()
        else:
            print("取消")
    @pyqtSlot()
    def on_btn_report_clicked(self):
        """
        生成图表
        """
        if self.isTesting:
            self.insert2textedit("正在测试中，请等待完成后重试!")
            return
        fnames = QFileDialog.getOpenFileNames(self, '选择多个文件','./',("logs (*.txt)"))
        print(fnames)
        if fnames[0]:
            plt.figure("图表")
            plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
            plt.title('电流曲线')
            plt.xlabel('时间(s)')
            plt.ylabel('电流(A)')
            for fname in fnames[0]:
                print(fname)
                try:
                    file = open(fname)  #打开文档
                    data = file.readlines() #读取文档数据
                    dx = []  #新建列表，用于保存第一列数据
                    dy = []  #新建列表，用于保存第二列数据
                    for num in data:
                        # split用于将每一行数据用逗号分割成多个对象
                        #取分割后的第0列，转换成float格式后添加到para_1列表中
                        dx.append(float(num.split(',')[0]))
                        #取分割后的第1列，转换成float格式后添加到para_1列表中
                        dy.append(float(num.split(',')[1]))
                    # print(sorted(dy))
                    # print(max(dy))
                    # print(min(dy))
                    # print(mean(dy)*5)
                    plt.ylim(0,mean(dy)*2)
                    plt.plot(dx,dy)
                    plt.plot(dx,dy,'.')
                    # for a, b in zip(dx, dy):
                    #     plt.text(a, b, (a,b),ha='center', va='bottom', fontsize=7)
                    # plt.legend() #加坐标
                except:
                    self.showmsg("请打开正确的log文件!")
                    return
            plt.show()
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
        self.starttestbtntip("",True)
        # self.progressBar.setValue(0)
        # self.progressBar.setVisible(True)
        self.dir_name=time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        os.mkdir(os.getcwd()+'/'+self.dir_name)
        for i in range(len(data)):
            if not self.isOUTPutOn:
                print("开关已关闭,重新打开...")
                # self.power.write("*RST")
                self.power.write("*CLS")
                self.power.write("IOCLEAR")
                self.power.write("OUTPut ON")
                self.isOUTPutOn=True
            print(data[i])
            work1=str(data[i]).split('-')
            testv=work1[0]
            testt=int(float(work1[1])*60)
            testwait=int(work1[2])
            print("电压%s,时间%s,间隔%s"%(testv,testt,testwait))
            self.insert2textedit("正在测试第%d组,电压【%sV】,时间【%s秒】,间隔【%s秒】"%(i+1,testv,testt,testwait))
            # self.isfreshV=False
            # self.isfreshA=False
            # 打开文件，写入数据
            try:
                self.log=open(os.getcwd()+'/'+self.dir_name+'/第%d组.txt'%(i+1),'w')
            except:
                self.insert2textedit("创建log文件错误，请重试 ~!")
                return
            # time.sleep(2)
            # self.power.write("*RST")
            self.power.write("*CLS")
            self.power.write("IOCLEAR")
            print(testv)
            self.power.write("VOLTage %s"%testv)
            print("设置电压ok")
            # try:
            #     self.progressBar.setValue(0)
            #     self.progressBar.setMaximum(testt)
            #     print("进度条ok")
            # except:
            #     print("进度条不OK")
            time.sleep(2)
            print("休息ok")
            self.start_loading(testt)
            for t in range(testt):
                print(t)
                if self.isTesting:
                    self.power.write("IOCLEAR")
                    self.power.write("*CLS")
                    vNum=float(self.power.query("MEAS:VOLT?"))
                    self.power.write("IOCLEAR")
                    aNum=float(self.power.query("MEAS:CURR?"))
                    print(aNum)
                    self.lcd_v.display(vNum)
                    self.lcd_a.display(aNum)
                    self.log.write("%s,%s\n"%(t,aNum))
                    time.sleep(1)
                    self.log.flush()
                    # self.progressBar.setValue(self.progressBar.value()+1)
                else:
                    print("中断...")
                    # if self.progressBar.isVisible():
                    #     self.progressBar.setVisible(False)
                    if not self.log.closed:
                        self.log.close()
                        print("close-log!")
                    # if not self.dir_name is None:
                    #     self.dir_name=None
                    self.insert2textedit("操作停止(⊙︿⊙)")
                    self.starttestbtntip("",True)
                    if not self.thread_progress is None:
                        self.stop_loading()
                    print("stop!")
                    return
            print("准备间隔...")
            self.stop_loading()
            self.insert2textedit("准备等待%s秒"%testwait)
            self.power.write("OUTPut OFF")
            self.isOUTPutOn=False
            for w in range(testwait):
                print('正在休息.%d'%w)
                time.sleep(1)
        # 测试完成
        if not self.log.closed:
            self.log.close()
        self.resetPower()
        print("测试完成")
        self.startfresh=True
        self.starttestbtntip("测试完成\(^o^)/~",True)
        self.insert2textedit("测试完成\(^o^)/~")
    def  setprogressValue(self):
        self.progressBar.setValue(self.progressBar.value()+1)
    def resetPower(self):
        if not self.power is None:
            # self.power.write("*RST")
            self.power.write("*CLS")
            self.power.write("*IOCLEAR")
            self.power.write("OUTPut OFF")
            self.switchtip("电源已关闭",False)
            if self.isOUTPutOn:
                self.isOUTPutOn=False
            if self.isTesting:
                self.isTesting=False
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
    def readV_A(self):
        while True:
            if self.startfresh:
                print("持续读取...")
                time.sleep(1)
                self.power.write("IOCLEAR")
                self.power.write("*CLS")
                try:
                    aNum=float(self.power.query("MEAS:CURR?"))
                except:
                    aNum=0
                    print("有错误")
                self.lcd_a.display(aNum)
                self.power.write("IOCLEAR")
                self.power.write("*CLS")
                try:
                    vNum=float(self.power.query("MEAS:VOLT?"))
                except:
                    vNum=0
                    print("电压错误")
                self.lcd_v.display(vNum)
            else:
                print("正在测试，就先不读取了！")
                time.sleep(2)


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

            # t_readv=threading.Thread(target=self.readV)
            # self.isfreshV=True
            #
            # t_readA=threading.Thread(target=self.readA)
            # self.isfreshA=True
            # t_readv.setDaemon(True)
            # t_readA.setDaemon(True)
            # t_readv.start()
            # t_readA.start()
            t_fresh=threading.Thread(target=self.readV_A)
            t_fresh.setDaemon(True)
            self.startfresh=True
            t_fresh.start()
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
    def start_loading(self,max):
        # 创建线程
        self.thread_progress = Runthread()
        self.thread_progress.max_value=max
        # 连接信号
        self.thread_progress._setmax.connect(self.setmax_progress)
        self.thread_progress._signal.connect(self.call_backlog)  # 进程连接回传到GUI的事件
        # 开始线程
        # print(self.thread_progress.max_value)
        self.thread_progress.start()
    def stop_loading(self):
        self.thread_progress.stop()

    def call_backlog(self, msg):
        if not self.progressBar.isVisible():
            self.progressBar.setVisible(True)
        self.progressBar.setValue(msg)
    def setmax_progress(self,max):
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(max)
        print("设置最大成功%s"%max)
# 继承QThread
class Runthread(QtCore.QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(int)
    _setmax = pyqtSignal(int)
    max_value=0
    def __init__(self):
        super(Runthread, self).__init__()
        self.isrun=True

    def stop(self):
        self.isrun=False

    def run(self):
        i=0
        self._setmax.emit(int(self.max_value))
        time.sleep(1)
        print("###我发送了,max:%s"%self.max_value)
        while self.isrun:
            # print("loading...")
            time.sleep(1)
            self._signal.emit(i)  # 注意这里与_signal = pyqtSignal(int)中的类型相同
            i+=1


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