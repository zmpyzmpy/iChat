from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem,QTableWidget
import sys
import threading
from PyQt5.QtWidgets import QMessageBox,QDialog
from dialog import Ui_Dialog
import operator
import warnings
warnings.filterwarnings('ignore')
# todo: same_time

from datetime import datetime
from dateutil.relativedelta import relativedelta

import itchat
import re

'''from nanpy import (ArduinoApi, SerialManager)'''
from time import sleep

import time
import email
import imaplib
import smtplib
from email.mime.text import MIMEText

'''ledPinY = 7
ledPinR = 8
try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to conncet to Arduino")

a.pinMode(ledPinY, a.OUTPUT)
a.pinMode(ledPinR, a.OUTPUT)'''

start_time = datetime.now()
def open_server():
	wechat = Wechat()
	wechat.run()

def open_email_server():
	email_service = email_handler()
	email_service.start_email_service()

def start_timer():
	server_thread = threading.Thread(target=open_server)
	server_thread.start()
	print("timer started")

	email_thread = threading.Thread(target=open_email_server)
	email_thread.start()



	global start_time
	start_time = datetime.now()
	diff_minutes = 1
	while True:

		time_now = datetime.now()
		total_time= time_now - start_time
		#print("light on")
		'''a.digitalWrite(ledPinY, a.HIGH)
		sleep(1500)
		a.digitalWrite(ledPinY, a.LOW)
		sleep(300)'''
		#if total_time.seconds == diff_minutes * 60:
                    #lights on
                    #print("light on")
                    #a.digitalWrite(ledPin, a.HIGH)
                    #sleep(3)

class email_handler():

	def get_first_text_block(self,msg):
		type = msg.get_content_maintype()

		if type == 'multipart':
			for part in msg.get_payload():
				if part.get_content_maintype() == 'text':
					return part.get_payload()
		elif type == 'text':
			return msg.get_payload()

	def start_email_service(self):
		imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
		imap_ssl_port = 993
		username = 'weijiewangnl@gmail.com'
		password = 'weijiewang77'
		uid_max = 0



		server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
		server.login(username, password)
		server.select('INBOX')

		result, data = server.uid('search', None, "unseen")

		uids = [int(s) for s in data[0].split()]
		if uids:
			uid_max = max(uids)
			# Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

		server.logout()


		# Keep checking messages ...
		print("Email service started...")
		while 1:
			# Have to login/logout each time because that's the only way to get fresh results.
			server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
			server.login(username, password)
			server.select('INBOX')

			result, data = server.uid('search', None, "unseen")

			uids = [int(s) for s in data[0].split()]

			for uid in uids:
				# Have to check again because Gmail sometimes does not obey UID criterion.
				if uid > uid_max:
					reply_msg = ''
					result, data = server.uid('fetch', str(uid), '(RFC822)')  # fetch entire message
					msg = email.message_from_string(data[0][1].decode("utf-8"))

					uid_max = uid

					text = self.get_first_text_block(msg)


					if '#important' in text:
						reply_msg = 'Weijie will contact you very soon.'


					elif 'min' in text:
						minutes = None
						try:
							minutes = re.findall(r"(\d+) min", text)[0]
						except:
							minutes = re.findall(r"(\d+)min", text)[0]
						if minutes == None:
							reply_msg = 'Could you mention how much time you need.'
						else:
							reply_msg = ui.buttonClicked(wechat=2,minutes = int(minutes))
					else:
						reply_msg = ui.buttonClicked(wechat=2,minutes = 1)


					smtp_ssl_host = 'smtp.gmail.com'
					smtp_ssl_port = 465
					username = 'weijiewangnl@gmail.com'
					password = 'weijiewang77'
					sender = 'weijiewangnl@gmail.com'
					targets = [msg['From']]

					msg1 = MIMEText(reply_msg)
					msg1['Subject'] = 'Hello'
					msg1['From'] = sender
					msg1['To'] = ', '.join(targets)

					server1 = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
					server1.login(username, password)
					server1.sendmail(sender, targets, msg1.as_string())
					server1.quit()


#					print('A new message')
#					print("From :"+ (email.utils.parseaddr(msg['From']))[1])
#					print("Subject:"+ str(msg['Subject']))
#					print("Content:"+ str(text))




#       	print('Start: %s' % time.ctime())
			server.logout()
			time.sleep(10)
#       	print('End: %s' % time.ctime())


class Wechat():


	def run(self):
		itchat.auto_login()
		itchat.run()



	@itchat.msg_register(itchat.content.TEXT)
	def text_reply(msg):
		global ui
		if '#important' in msg.text:
#			ui.buttonClicked(wechat=2)
			print("alert")
			return 'Weijie will contact you very soon.'

		'''
			a.digitalWrite(ledPinR, a.HIGH)
            sleep(1)
            a.digitalWrite(ledPinR, a.LOW)
            sleep(1)
            a.digitalWrite(ledPinR, a.HIGH)
            sleep(1)
            a.digitalWrite(ledPinR, a.LOW)
            sleep(1)
            a.digitalWrite(ledPinR, a.HIGH)
            sleep(1)
            a.digitalWrite(ledPinR, a.LOW)
            sleep(1)
        '''


		if 'min' in msg.text:
			minutes = None
			try:
				minutes = re.findall(r"(\d+) min", msg.text)[0]
			except:
				minutes = re.findall(r"(\d+)min", msg.text)[0]
			if minutes == None:
				return 'Could you mention how much time you need.'
			msg = ui.buttonClicked(wechat=1,minutes = int(minutes))
		else:
			msg = ui.buttonClicked(wechat=1,minutes = 1)

		return msg

class Ui_MainWindow(object):
	def __init__(self):
		self.rest_5min = [0,0,0,0]

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1200, 768)
		MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(215,196,187, 255), stop:1 rgba(215,196,187, 255));")
		MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(80, 80, 761, 351))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.rest1 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.rest1.setMaximumSize(QtCore.QSize(16777215, 60))
		self.rest1.setStyleSheet('background-color: rgba(0, 35, 163, 0)')
		self.rest1.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.rest1.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.rest1.setText("")
		self.rest1.setObjectName("rest1")
		self.gridLayout.addWidget(self.rest1, 0, 1, 1, 1)
		self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_2.setEnabled(True)
		self.label_2.setLocale(QtCore.QLocale(QtCore.QLocale.Dzongkha, QtCore.QLocale.Bhutan))
		self.label_2.setAlignment(QtCore.Qt.AlignCenter)
		self.label_2.setObjectName("label_2")
		self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
		self.label = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label.setMaximumSize(QtCore.QSize(200, 16777215))
		self.label.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
		self.rest3 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.rest3.setMaximumSize(QtCore.QSize(16777215, 60))
		self.rest3.setStyleSheet('background-color: rgba(0, 35, 163, 0)')
		self.rest3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.rest3.setText("")
		self.rest3.setObjectName("rest3")
		self.gridLayout.addWidget(self.rest3, 2, 1, 1, 1)
		self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_3.setLocale(QtCore.QLocale(QtCore.QLocale.Embu, QtCore.QLocale.Kenya))
		self.label_3.setAlignment(QtCore.Qt.AlignCenter)
		self.label_3.setObjectName("label_3")
		self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
		self.rest2 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.rest2.setMaximumSize(QtCore.QSize(16777215, 60))
		self.rest2.setStyleSheet('background-color: rgba(0, 35, 163, 0)')
		self.rest2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.rest2.setText("")
		self.rest2.setObjectName("rest2")
		self.gridLayout.addWidget(self.rest2, 1, 1, 1, 1)
		self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_4.setLocale(QtCore.QLocale(QtCore.QLocale.Dzongkha, QtCore.QLocale.Bhutan))
		self.label_4.setAlignment(QtCore.Qt.AlignCenter)
		self.label_4.setObjectName("label_4")
		self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
		self.rest4 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.rest4.setMaximumSize(QtCore.QSize(16777215, 60))
		self.rest4.setStyleSheet('background-color: rgba(0, 35, 163, 0)')
		self.rest4.setLocale(QtCore.QLocale(QtCore.QLocale.Dzongkha, QtCore.QLocale.Bhutan))
		self.rest4.setText("")
		self.rest4.setObjectName("rest4")
		self.gridLayout.addWidget(self.rest4, 3, 1, 1, 1)
		self.label_7 = QtWidgets.QLabel(self.centralwidget)
		self.label_7.setGeometry(QtCore.QRect(520, 70, 111, 21))
		self.label_7.setObjectName("label_7")

		#  The last pomodoro's break
		self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(100, 425, 761, 61))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")
		self.rest30_1 = QtWidgets.QLabel(self.verticalLayoutWidget)
		self.rest30_1.setEnabled(True)
		self.rest30_1.setMaximumSize(QtCore.QSize(16777215, 60))
		self.rest30_1.setStyleSheet('background-color: rgba(0, 35, 163, 0)')
		self.rest30_1.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.rest30_1.setText("")
		self.rest30_1.setObjectName("rest30_1")
		self.verticalLayout.addWidget(self.rest30_1)

		# Text 'Additional time slot'
		self.label_10 = QtWidgets.QLabel(self.centralwidget)
		self.label_10.setGeometry(QtCore.QRect(400, 500, 200, 32))
		self.label_10.setAlignment(QtCore.Qt.AlignCenter)
		self.label_10.setObjectName("label_10")

		# Additional time slot = 30 x 2
		self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
		self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(100, 525, 761, 160))
		self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
		self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.rest30_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
		self.rest30_2.setMaximumSize(QtCore.QSize(16777215, 60))
		self.rest30_2.setStyleSheet('background-color: rgba(0, 35, 163, 0)')
		self.rest30_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.rest30_2.setText("")
		self.rest30_2.setObjectName("rest30_2")
		self.verticalLayout_2.addWidget(self.rest30_2)
		self.rest30_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
		self.rest30_3.setMaximumSize(QtCore.QSize(16777215, 60))
		self.rest30_3.setStyleSheet('background-color: rgba(0, 35, 163, 0)')
		self.rest30_3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.rest30_3.setText("")
		self.rest30_3.setObjectName("rest30_3")
		self.verticalLayout_2.addWidget(self.rest30_3)



		self.menu = QtWidgets.QComboBox(self.centralwidget)
		self.menu.setGeometry(QtCore.QRect(100, 680, 180, 32))
		self.menu.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.menu.setObjectName("menu")
		self.menu.addItem("")
		self.menu.addItem("")
		self.menu.addItem("")
		self.menu.addItem("")
		self.menu.addItem("")
		self.menu.addItem("")

		# Add button
		self.add = QtWidgets.QPushButton(self.centralwidget)
		self.add.setGeometry(QtCore.QRect(290, 680, 110, 32))
		self.add.setObjectName("add")

		# Press to start the program
		self.pushButton = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton.setGeometry(QtCore.QRect(340, 8, 110, 32))
		self.pushButton.setObjectName("pushButton")
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setBold(True)
		font.setWeight(75)
		self.add.setFont(font)
		self.add.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.add.setObjectName("add")

		# Confirm to change time
		self.change_time = QtWidgets.QPushButton(self.centralwidget)
		self.change_time.setGeometry(QtCore.QRect(220, 8, 110, 32))
		self.change_time.setObjectName("change_time")

		# Edit time (default time = 25)
		self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
		self.lineEdit.setObjectName("lineEdit")
		self.lineEdit.setGeometry(QtCore.QRect(100, 8, 110, 32))
		self.lineEdit.setText("25")

		'''
		# black BG
		self.frame = QtWidgets.QFrame(self.centralwidget)
		self.frame.setGeometry(QtCore.QRect(70, 270, 291, 191))
		self.frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0,0,0, 255), stop:1 rgba(0,0,0, 255));")
		self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame.setObjectName("frame")
		'''



		self.rest_5min_widgets = [self.rest1,self.rest2,self.rest3,self.rest4]
		self.rest_30min = [0]
		self.rest_30min_widgets = [self.rest30_1]
		self.rest_240min = [0,0]
		self.rest_240min_widgets = [self.rest30_2,self.rest30_3]
		self.item_list = {}
		self.item_list['Working'] = (25,'no')
		self.item_list['Cooking & Eating'] = (30,'no')
		self.item_list['Washing the clothes'] = (30,'Strong yes')
		self.item_list['Opening the door'] = (5,'no')
		self.item_list['Reminder'] = (1,'no')
		self.item_list['Boiling the water'] = (5,'Strong yes')


		self.dialog = Ui_Dialog()



		# table
		self.verticalLayoutWidget1 = QtWidgets.QWidget(self.centralwidget)
		self.verticalLayoutWidget1.setGeometry(QtCore.QRect(850, 50, 233, 371))
		self.verticalLayoutWidget1.setObjectName("verticalLayoutWidget1")
		self.verticalLayout1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget1)
		self.verticalLayout1.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout1.setSpacing(0)
		self.verticalLayout1.setObjectName("verticalLayout1")
		
		self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget1)
		self.tableWidget.setObjectName("tableWidget")
		self.tableWidget.setColumnCount(3)
		self.tableWidget.setRowCount(1)
		self.tableWidget.setColumnWidth(0, 100)
		self.tableWidget.setColumnWidth(1, 100)
		self.tableWidget.setColumnWidth(2, 30)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		self.tableWidget.setVerticalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setVerticalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setBold(False)
		font.setWeight(50)
		item.setFont(font)
		self.tableWidget.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		item.setTextAlignment(QtCore.Qt.AlignCenter)
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		self.tableWidget.setItem(0, 0, item)
		item = QtWidgets.QTableWidgetItem()
		item.setTextAlignment(QtCore.Qt.AlignCenter)
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		item.setFont(font)
		self.tableWidget.setItem(0, 1, item)
		self.tableWidget.horizontalHeader().setVisible(False)
		self.tableWidget.horizontalHeader().setHighlightSections(False)
		self.tableWidget.verticalHeader().setVisible(False)
		self.tableWidget.verticalHeader().setHighlightSections(False)
		self.verticalLayout1.addWidget(self.tableWidget)
		self.label_table = QtWidgets.QLabel(self.verticalLayoutWidget1)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_table.setFont(font)
		self.label_table.setAlignment(QtCore.Qt.AlignCenter)
		self.label_table.setObjectName("label_table")
		self.verticalLayout1.addWidget(self.label_table)
		self.tableWidget_2 = QtWidgets.QTableWidget(self.verticalLayoutWidget1)
		self.tableWidget_2.setObjectName("tableWidget_2")
		self.tableWidget_2.setColumnCount(3)
		self.tableWidget_2.setRowCount(0)
		self.tableWidget_2.setColumnWidth(0, 100)
		self.tableWidget_2.setColumnWidth(1, 100)
		self.tableWidget_2.setColumnWidth(2, 30)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget_2.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget_2.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.tableWidget_2.setHorizontalHeaderItem(2, item)
		self.tableWidget_2.horizontalHeader().setVisible(False)
		self.tableWidget_2.verticalHeader().setVisible(False)
		self.verticalLayout1.addWidget(self.tableWidget_2)
		self.label_table.setStyleSheet("border-width: 1px;border-style: solid;")
		self.tableWidget.setStyleSheet("border-width: 1px;border-style: solid;")
		self.tableWidget_2.setStyleSheet("border-width: 1px;border-style: solid;")
		self.table_1_count = 1
		self.table_2_count = 0
		self.tableWidget.itemClicked.connect(self.table1_click)
		self.tableWidget_2.itemClicked.connect(self.table2_click)
		
		
		self.table_list = []
		
		
		self.add.raise_()
		# self.frame.raise_()raise_
		self.gridLayoutWidget.raise_()
		self.label_7.raise_()
		self.verticalLayoutWidget.raise_()
		self.label_10.raise_()
		self.verticalLayoutWidget_2.raise_()
		self.menu.raise_()
		self.add.raise_()
		self.rest30_3.raise_()
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 22))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)


	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.label.setText(_translate("MainWindow", "Working time 25 min"))
		self.label_2.setText(_translate("MainWindow", "Working time 25 min"))
		self.label_3.setText(_translate("MainWindow", "Working time 25 min"))
		self.label_4.setText(_translate("MainWindow", "Working time 25 min"))
		self.label_7.setText(_translate("MainWindow", "5mins break"))
		# self.label_8.setText(_translate("MainWindow", "work time: "))
		self.label_10.setText(_translate("MainWindow", "Additional time slot"))
		self.menu.setItemText(0, _translate("MainWindow", "Working"))
		self.menu.setItemText(1, _translate("MainWindow", "Cooking & Eating"))
		self.menu.setItemText(2, _translate("MainWindow", "Washing the clothes"))
		self.menu.setItemText(3, _translate("MainWindow", "Opening the door"))
		self.menu.setItemText(4, _translate("MainWindow", "Reminder"))
		self.menu.setItemText(5, _translate("MainWindow", "Boiling the water"))
		self.menu.setItemText(6, _translate("MainWindow", "Custom"))
		self.add.setText(_translate("MainWindow", "add"))
		self.change_time.setText(_translate("MainWindow", "set time"))
		self.add.clicked.connect(self.buttonClicked)
		self.pushButton.setText(_translate("MainWindow", "start"))
		self.pushButton.clicked.connect(self.timer_buttonClicked)
		self.change_time.clicked.connect(self.change_working_time)
		
		item = self.tableWidget.verticalHeaderItem(0)
#		item.setText(_translate("MainWindow", "New Row"))
		item = self.tableWidget.horizontalHeaderItem(0)
#		item.setText(_translate("MainWindow", "New Column"))
		item = self.tableWidget.horizontalHeaderItem(1)
#		item.setText(_translate("MainWindow", "New Column"))
		item = self.tableWidget.horizontalHeaderItem(2)
#		item.setText(_translate("MainWindow", "New Column"))
		__sortingEnabled = self.tableWidget.isSortingEnabled()
		self.tableWidget.setSortingEnabled(True)
		item = self.tableWidget.item(0, 0)
		item.setText(_translate("MainWindow", "Event"))
		item = self.tableWidget.item(0, 1)
		item.setText(_translate("MainWindow", "Duration"))
		self.tableWidget.setSortingEnabled(__sortingEnabled)
		self.label_table.setText(_translate("MainWindow", "\n2 mins\n"))
		item = self.tableWidget_2.horizontalHeaderItem(0)
		item.setText(_translate("MainWindow", "New Column"))
		item = self.tableWidget_2.horizontalHeaderItem(1)
		item.setText(_translate("MainWindow", "New Column"))
		item = self.tableWidget_2.horizontalHeaderItem(2)
		item.setText(_translate("MainWindow", "New Column"))

	def change_working_time(self):
		self.work_time = int(self.lineEdit.text())
		self.label.setText("Working time " + str(self.work_time) +" min")
		self.label_2.setText("Working time " + str(self.work_time) +" min")
		self.label_3.setText("Working time " + str(self.work_time) +" min")
		self.label_4.setText("Working time " + str(self.work_time) +" min")


	def timer_buttonClicked(self):
		timer_thread = threading.Thread(target=start_timer)
		timer_thread.start()
		self.work_time = int(self.lineEdit.text())
		self.rest_time = 5
		self.work_and_rest = self.work_time + self.rest_time

	def buttonClicked(self,wechat = 0,minutes = 0):
		txt = self.menu.currentText()
		if wechat == 1:
			activity = 'WeChat'
		elif wechat == 2:
			activity = 'Email'
		else:
			activity = txt
		if wechat == 1 or wechat ==2:

			setted = False
			same_time = self.item_list[txt][1]
			full = False
			i = 0
			j = 0
			j_changed = False
			if minutes <= 5:
				for i in range(len(self.rest_5min)):
					if 5 - self.rest_5min[i] >= minutes:
						self.rest_5min[i] += minutes
						self.rest_5min_widgets[i].setText(self.rest_5min_widgets[i].text() + ' ' + activity)
						self.rest_5min_widgets[i].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_5min[i]/self.work_and_rest) + ")")
						setted = True
						self.table_list.append((i,activity,minutes))
						break
				if setted == False:
					full = True
					if 30 - self.rest_30min[j] >= minutes:
						self.rest_30min[j] += minutes
						self.rest_30min_widgets[j].setText(self.rest_30min_widgets[j].text() + ' ' + activity)
						self.rest_30min_widgets[j].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_30min[j]/30) + ")")
						setted = True
						j_changed = True
						self.table_list.append((4,activity,minutes))
				if setted == False:
					for j in range(len(self.rest_240min)):
						if 240 - self.rest_240min[j] >= minutes:
							self.rest_240min[j] += minutes
							self.rest_240min_widgets[j].setText(self.rest_240min_widgets[j].text() + ' ' + activity)
							self.rest_240min_widgets[j].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_240min[j]/240) + ")")
							setted = True
							j_changed = True
							j += 1
							self.table_list.append((j+4,activity,minutes))
							break
				if setted:
					if minutes > 2:
						self.table_1_count += 1
						self.tableWidget.setRowCount(self.table_1_count)
						item = QTableWidgetItem(activity)
						item.setTextAlignment(QtCore.Qt.AlignCenter)
						self.tableWidget.setItem(self.table_1_count - 1,0, item)
						item = QTableWidgetItem(str(minutes))
						item.setTextAlignment(QtCore.Qt.AlignCenter)
						self.tableWidget.setItem(self.table_1_count - 1,1, item)
						item = QTableWidgetItem("x")
						item.setTextAlignment(QtCore.Qt.AlignCenter)
						self.tableWidget.setItem(self.table_1_count - 1,2, item)
						
						self.table_1_items = []
						for idx in range(1,self.table_1_count):
							self.table_1_items.append((self.tableWidget.item(idx,0).text(),int(self.tableWidget.item(idx,1).text())))
							
						
						self.table_1_items = sorted(self.table_1_items, key=lambda x: x[1],reverse=True)
						
						for idx,(act,mnt) in enumerate(self.table_1_items):
							item = QTableWidgetItem(act)
							item.setTextAlignment(QtCore.Qt.AlignCenter)
							self.tableWidget.setItem(idx + 1,0, item)
							item = QTableWidgetItem(str(mnt))
							item.setTextAlignment(QtCore.Qt.AlignCenter)
							self.tableWidget.setItem(idx + 1,1, item)
						
						
					else:
						self.table_2_count += 1
						self.tableWidget_2.setRowCount(self.table_2_count)
						item = QTableWidgetItem(activity)
						item.setTextAlignment(QtCore.Qt.AlignCenter)
						self.tableWidget_2.setItem(self.table_2_count - 1,0, item)
						item = QTableWidgetItem(str(minutes))
						item.setTextAlignment(QtCore.Qt.AlignCenter)
						self.tableWidget_2.setItem(self.table_2_count - 1,1, item)
						item = QTableWidgetItem("x")
						item.setTextAlignment(QtCore.Qt.AlignCenter)
						self.tableWidget_2.setItem(self.table_2_count - 1,2, item)
						
						
						self.table_2_items = []
						for idx in range(self.table_2_count):
							self.table_2_items.append((self.tableWidget_2.item(idx,0).text(),int(self.tableWidget_2.item(idx,1).text())))
							
						
						self.table_2_items = sorted(self.table_2_items, key=lambda x: x[1],reverse=True)
						
						for idx,(act,mnt) in enumerate(self.table_2_items):
							item = QTableWidgetItem(act)
							item.setTextAlignment(QtCore.Qt.AlignCenter)
							self.tableWidget_2.setItem(idx ,0, item)
							item = QTableWidgetItem(str(mnt))
							item.setTextAlignment(QtCore.Qt.AlignCenter)
							self.tableWidget_2.setItem(idx ,1, item)
				if setted == False:
					return "Sorry, Weijie cannot make that long time today, but he will try to arrange his time to contact you asap."
				else:
					global start_time
					time_now = datetime.now()
					diff = time_now-start_time
					diff_minutes = diff.seconds/60

					time_togo = 0
					if i == 0 and j_changed == False:
						time_togo = self.work_time - diff_minutes
					elif i > 0 and not full:
						time_togo = self.work_and_rest * (i+1) - diff_minutes - 5
						
					elif j == 0 and full:
						time_togo = self.work_and_rest *4
					elif j > 0 or full:
						return "Weijie will contact you in some time, maybe during the lunch break or dinner break"
					return "Weijie is busy now, he will contact you " + str(round(time_togo,2)) + " minutes later. If you have something very important, please add \"#important\" before your message"
					


		if (txt != 'Custom') and (activity == txt):
			
			
			setted = False
			minutes = self.item_list[txt][0]
			same_time = self.item_list[txt][1]
			if minutes <= 5:
				for i in range(len(self.rest_5min)):
					if 5 - self.rest_5min[i] >= minutes:
						self.rest_5min[i] += minutes
						self.rest_5min_widgets[i].setText(self.rest_5min_widgets[i].text() + ' ' + txt)
						self.rest_5min_widgets[i].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_5min[i]/30) + ")")
						setted = True
						self.table_list.append((i,activity,minutes))
						break
			if setted == False:
				j = 0
				if 30 - self.rest_30min[j] >= minutes:
					self.rest_30min[j] += minutes
					self.rest_30min_widgets[j].setText(self.rest_30min_widgets[j].text() + ' ' + activity)
					self.rest_30min_widgets[j].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_30min[j]/30) + ")")
					setted = True
					j_changed = True
					self.table_list.append((4,activity,minutes))
			if setted == False:
				for j in range(len(self.rest_240min)):
					if 240 - self.rest_240min[j] >= minutes:
						self.rest_240min[j] += minutes
						self.rest_240min_widgets[j].setText(self.rest_240min_widgets[j].text() + ' ' + activity)
						self.rest_240min_widgets[j].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_240min[j]/240) + ")")
						setted = True
						j_changed = True
						j += 1
						self.table_list.append((j + 4,activity,minutes))
						break
			if setted == False:
				print("wwj")
				msg = QMessageBox()
				msg.setText("无法继续添加")
				msg.setStandardButtons(QMessageBox.Ok)
				retval = msg.exec_()
				
			if setted:
				if minutes > 2:
					self.table_1_count += 1
					self.tableWidget.setRowCount(self.table_1_count)
					item = QTableWidgetItem(activity)
					item.setTextAlignment(QtCore.Qt.AlignCenter)
					self.tableWidget.setItem(self.table_1_count - 1,0, item)
					item = QTableWidgetItem(str(minutes))
					item.setTextAlignment(QtCore.Qt.AlignCenter)
					self.tableWidget.setItem(self.table_1_count - 1,1, item)
					item = QTableWidgetItem("x")
					item.setTextAlignment(QtCore.Qt.AlignCenter)
					self.tableWidget.setItem(self.table_1_count - 1,2, item)
					
					self.table_1_items = []
					for idx in range(1,self.table_1_count):
						self.table_1_items.append((self.tableWidget.item(idx,0).text(),str(self.tableWidget.item(idx,1).text())))
						
					
					self.table_1_items = sorted(self.table_1_items, key=lambda x: x[1],reverse=True)
					
					for idx,(act,mnt) in enumerate(self.table_1_items):
						item = QTableWidgetItem(act)
						item.setTextAlignment(QtCore.Qt.AlignCenter)
						self.tableWidget.setItem(idx + 1,0, item)
						item = QTableWidgetItem(str(mnt))
						item.setTextAlignment(QtCore.Qt.AlignCenter)
						self.tableWidget.setItem(idx + 1,1, item)
					
					
				else:
					self.table_2_count += 1
					self.tableWidget_2.setRowCount(self.table_2_count)
					item = QTableWidgetItem(activity)
					item.setTextAlignment(QtCore.Qt.AlignCenter)
					self.tableWidget_2.setItem(self.table_2_count - 1,0, item)
					item = QTableWidgetItem(str(minutes))
					item.setTextAlignment(QtCore.Qt.AlignCenter)
					self.tableWidget_2.setItem(self.table_2_count - 1,1, item)
					item = QTableWidgetItem("x")
					item.setTextAlignment(QtCore.Qt.AlignCenter)
					self.tableWidget_2.setItem(self.table_2_count - 1,2, item)
					
					
					self.table_2_items = []
					for idx in range(self.table_2_count):
						self.table_2_items.append((self.tableWidget_2.item(idx,0).text(),int(self.tableWidget_2.item(idx,1).text())))
						
					
					self.table_2_items = sorted(self.table_2_items, key=lambda x: x[1],reverse=True)
					
					for idx,(act,mnt) in enumerate(self.table_2_items):
						item = QTableWidgetItem(act)
						item.setTextAlignment(QtCore.Qt.AlignCenter)
						self.tableWidget_2.setItem(idx ,0, item)
						item = QTableWidgetItem(str(mnt))
						item.setTextAlignment(QtCore.Qt.AlignCenter)
						self.tableWidget_2.setItem(idx ,1, item)
					
				
		elif txt == 'Custom':

			d = QDialog()
			self.dialog.setupUi(d)
			if d.exec_() == QDialog.Accepted:
				name = self.dialog.lineEdit.text()
				period = self.dialog.lineEdit_2.text()
				same_time =self.dialog.comboBox.currentText()
				self.menu.addItem("")
				self.item_list[name] = (int(period),same_time)
				self.menu.setItemText(self.menu.count() - 2, name)
				self.menu.setItemText(self.menu.count() - 1, 'Custom')
				
	# delete items
	def table1_click(self,item):
		if (item.column() == 2) and item.row()>0:
			self.table_1_count -= 1
			
			activity, minutes = self.table_1_items.pop(item.row()-1)
			minutes = int(minutes)
			label_idx = 0
			for i,(idx,act,mnt) in enumerate(self.table_list):
				if (act == activity) and (minutes == mnt):
					label_idx = idx
					break
			self.table_list.pop(i)
			if label_idx < 4:
#				self.rest_5min[label_idx] -= minutes
				self.rest_5min_widgets[label_idx].setText(self.rest_5min_widgets[label_idx].text().replace(' ' + activity, "", 1))
#				self.rest_5min_widgets[label_idx].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_5min[label_idx]/30) + ")")
			elif label_idx == 4:
#				self.rest_30min[0] -= minutes
				self.rest_30min_widgets[0].setText(self.rest_30min_widgets[0].text().replace(' ' + activity, "", 1))
#				self.rest_30min_widgets[0].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_30min[0]/30) + ")")
			else:
#				self.rest_240min[label_idx-5] -= minutes
				self.rest_240min_widgets[label_idx-5].setText(self.rest_240min_widgets[label_idx-5].text().replace(' ' + activity, "", 1))
#				self.rest_240min_widgets[label_idx-5].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_240min[label_idx-5]/240) + ")")
			
			
			
			for idx,(act,mnt) in enumerate(self.table_1_items):
				item = QTableWidgetItem(act)
				item.setTextAlignment(QtCore.Qt.AlignCenter)
				self.tableWidget.setItem(idx + 1,0, item)
				item = QTableWidgetItem(str(mnt))
				item.setTextAlignment(QtCore.Qt.AlignCenter)
				self.tableWidget.setItem(idx + 1,1, item)
			self.tableWidget.setRowCount(self.table_1_count)
			
	
	def table2_click(self,item):
		if (item.column() == 2) and item.row()>=0:
			
			self.table_2_count -= 1
			activity, minutes = self.table_2_items.pop(item.row())
			minutes = int(minutes)
			label_idx = 0
			for i,(idx,act,mnt) in enumerate(self.table_list):
				if (act == activity) and (minutes == mnt):
					label_idx = idx
					break
			self.table_list.pop(i)
			if label_idx < 4:
#				self.rest_5min[label_idx] -= minutes
				self.rest_5min_widgets[label_idx].setText(self.rest_5min_widgets[label_idx].text().replace(' ' + activity, "", 1))
#				self.rest_5min_widgets[label_idx].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_5min[label_idx]/30) + ")")
			elif label_idx == 4:
#				self.rest_30min[0] -= minutes
				self.rest_30min_widgets[0].setText(self.rest_30min_widgets[0].text().replace(' ' + activity, "", 1))
#				self.rest_30min_widgets[0].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_30min[0]/30) + ")")
			else:
#				self.rest_240min[label_idx-5] -= minutes
				self.rest_240min_widgets[label_idx-5].setText(self.rest_240min_widgets[label_idx-5].text().replace(' ' + activity, "", 1))
#				self.rest_240min_widgets[label_idx-5].setStyleSheet("background-color: rgba(0, 35, 163,"+ str(255*self.rest_240min[label_idx-5]/240) + ")")
			

			for idx,(act,mnt) in enumerate(self.table_2_items):
				item = QTableWidgetItem(act)
				item.setTextAlignment(QtCore.Qt.AlignCenter)
				self.tableWidget_2.setItem(idx,0, item)
				item = QTableWidgetItem(str(mnt))
				item.setTextAlignment(QtCore.Qt.AlignCenter)
				self.tableWidget_2.setItem(idx,1, item)
			self.tableWidget_2.setRowCount(self.table_2_count)
			

ui = Ui_MainWindow()
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QMainWindow()

	ui.setupUi(MainWindow)




	MainWindow.show()
	sys.exit(app.exec_())
