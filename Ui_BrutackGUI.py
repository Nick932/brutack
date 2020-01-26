# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/nickel/Документы/Brutack/BrutackGUI.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os,  threading,  time

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(402, 300)
        Frame.setMinimumSize(QtCore.QSize(402, 300))
        Frame.setMaximumSize(QtCore.QSize(402, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("art.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Frame.setWindowIcon(icon)
        Frame.setAutoFillBackground(True)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_3 = QtWidgets.QLabel(Frame)
        self.label_3.setGeometry(QtCore.QRect(10, 0, 371, 131))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.line = QtWidgets.QFrame(Frame)
        self.line.setGeometry(QtCore.QRect(-10, 120, 421, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton = QtWidgets.QPushButton(Frame)
        self.pushButton.setGeometry(QtCore.QRect(150, 260, 99, 27))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(20, 141, 161, 17))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Frame)
        self.lineEdit.setGeometry(QtCore.QRect(20, 164, 191, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(20, 197, 191, 17))
        self.label.setObjectName("label")
        self.lineEdit_2 = QtWidgets.QLineEdit(Frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 220, 189, 31))
        self.lineEdit_2.setMinimumSize(QtCore.QSize(189, 27))
        self.lineEdit_2.setObjectName("lineEdit_2")
        
        
        def on_clicked():
            WIFIname = str(self.lineEdit.text())
            passwords = str(self.lineEdit_2.text())
            log = open('BrutackGUI_logfile.txt',  'w')
            l = 'Attack was tried at:\n'+str(time.ctime())+'\n\nWIFI:\n'+str(WIFIname)+'\n\nfile with passwords:\n'+str(passwords)
            log.write(l)
            log.close()
            StartAttack = os.popen('python3 brutack.py {0} {1}'.format(WIFIname, passwords))
            lock = threading.Lock()
            with lock:
                threading.Thread(target = StartAttack)
            
            
        self.pushButton.clicked.connect(lambda: on_clicked()) # Если не 
        # лямбдой, то функция должна возвращать что-то, иначе 
        # "TypeError: argument 1 has unexpected type 'NoneType'" выдаст!
        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Brutack"))
        self.label_3.setText(_translate("Frame", "Brutack - это программа для брут-форс атаки WI-FI, которая пытается подключиться к указанному соединению. Brutack перебирает пароли, заданные в файле, путь к которому вы указываете ниже.                           Каждый следующий пароль в файле  должен начинаться с новой строки, а сам файл сохранён в кодировке UTF-8."))
        self.pushButton.setText(_translate("Frame", "Старт"))
        self.label_2.setText(_translate("Frame", "Имя WI-FI соединения:"))
        self.label.setText(_translate("Frame", "Путь к файлу с паролями:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())

