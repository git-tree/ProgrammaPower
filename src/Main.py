# -*- coding: utf-8 -*-

'''
@Time    : 2020/7/26 16:08
@Author  : shusen.cui
@FileName: Main.py
@Software: PyCharm
 
'''
import sys
from Power_main import controller_main
from PyQt5.QtWidgets import QApplication

# 程序主入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login=controller_main()
    login.show()
    sys.exit(app.exec_())