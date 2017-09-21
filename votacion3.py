# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import paho.mqtt.client as mqtt
import json
import yaml
import pandas as pd
import threading
import time

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
	def __init__(self):
		cant=3
		self.dispositivos=range(0,cant)#,199)	#200 dispositivos
		self.afavor=0
		self.encontra=0
		self.abstencion=0
		self.id=''
		self.id_acum=[]
		self.res=[]
		self.cant=0
			
	def on_connect(self,client, userdata, flags, rc):
		print("Connected with result code "+str(rc))
		
		for i in self.dispositivos:
			trama="votacion/cliente/"+str(i)+"/publish"
			client.subscribe(trama)
			print "se suscribio a",trama

	def on_message(self,client, userdata, msg):
		data=yaml.load(msg.payload)
		print data
		if isinstance(data,str):
			self.cant+=1
			self.comboBox.addItem(data)
			self.label_6.setText("conectados: "+str(self.cant))
		if(isinstance(data,dict)): 
			self.id=data['id']
			
			filtro = data['favor'] | data['contra']<<1 | data['abstencion']<<2
			
			if not(self.id in self.id_acum) and (filtro in [1,2,4]):
				self.afavor+=data['favor']
				self.encontra+=data['contra']
				self.abstencion+=data['abstencion']
				self.lcdNumber_2.display(self.afavor)
				self.lcdNumber_3.display(self.encontra)
				self.lcdNumber_4.display(self.abstencion)
				self.id_acum.append(self.id)
				self.res.append([self.id, data['favor'], data['contra'], data['abstencion']])
				
	def mqtt(self):
		self.client = mqtt.Client()
		self.client.loop_start()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.connect("iot.eclipse.org", 1883, 60)
		
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(753, 474)
		MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(85, 255, 255);"))
		MainWindow.setTabShape(QtGui.QTabWidget.Triangular)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.lcdNumber_2 = QtGui.QLCDNumber(self.centralwidget)
		self.lcdNumber_2.setGeometry(QtCore.QRect(20, 170, 231, 131))
		self.lcdNumber_2.setObjectName(_fromUtf8("lcdNumber_2"))
		self.lcdNumber_3 = QtGui.QLCDNumber(self.centralwidget)
		self.lcdNumber_3.setGeometry(QtCore.QRect(260, 170, 231, 131))
		self.lcdNumber_3.setObjectName(_fromUtf8("lcdNumber_3"))
		self.lcdNumber_4 = QtGui.QLCDNumber(self.centralwidget)
		self.lcdNumber_4.setGeometry(QtCore.QRect(500, 170, 231, 131))
		self.lcdNumber_4.setObjectName(_fromUtf8("lcdNumber_4"))
		self.label = QtGui.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(70, 20, 611, 51))
		self.label.setStyleSheet(_fromUtf8("font:43pt \"Ubuntu\";\n"
	"color: rgb(188, 0, 0);"))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(self.centralwidget)
		self.label_2.setGeometry(QtCore.QRect(60, 110, 151, 41))
		self.label_2.setStyleSheet(_fromUtf8("font: 24pt \"Ubuntu\";\n"
	"color: rgb(85, 85, 255);"))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_3 = QtGui.QLabel(self.centralwidget)
		self.label_3.setGeometry(QtCore.QRect(290, 110, 171, 41))
		self.label_3.setStyleSheet(_fromUtf8("font: 24pt \"Ubuntu\";\n"
	"color: rgb(255, 0, 0);"))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_4 = QtGui.QLabel(self.centralwidget)
		self.label_4.setGeometry(QtCore.QRect(510, 110, 201, 41))
		self.label_4.setStyleSheet(_fromUtf8("font: 24pt \"Ubuntu\";\n"
	"color: rgb(185, 185, 0);"))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.comboBox = QtGui.QComboBox(self.centralwidget)
		self.comboBox.setGeometry(QtCore.QRect(40, 370, 151, 27))
		self.comboBox.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);"))
		self.comboBox.setObjectName(_fromUtf8("comboBox"))
		self.comboBox.addItem("-- dispositivos --")
		self.label_5 = QtGui.QLabel(self.centralwidget)
		self.label_5.setGeometry(QtCore.QRect(50, 340, 101, 21))
		self.label_5.setStyleSheet(_fromUtf8("font: 14pt \"Ubuntu\";\n"
	"color: rgb(0, 85, 0);"))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.pushButton = QtGui.QPushButton(self.centralwidget)
		self.pushButton.setGeometry(QtCore.QRect(557, 360, 141, 27))
		self.pushButton.setStyleSheet(_fromUtf8("background-color: rgb(0, 255, 0);\n"
	"color: rgb(0, 170, 0);\n"
	"font: 16pt \"Ubuntu\";"))
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.pushButton.clicked.connect(self.exportar)
		
		self.label_6 = QtGui.QLabel(self.centralwidget)
		self.label_6.setGeometry(QtCore.QRect(40, 410, 141, 17))
		self.label_6.setObjectName(_fromUtf8("label_6"))
		
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 753, 25))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "VOTACION", None))
		MainWindow.setWindowIcon(QtGui.QIcon("./voto2.png"))
		self.label.setText(_translate("MainWindow", "SISTEMA DE VOTACION", None))
		self.label_2.setText(_translate("MainWindow", "A FAVOR", None))
		self.label_3.setText(_translate("MainWindow", "ENCONTRA", None))
		self.label_4.setText(_translate("MainWindow", "ABSTENCION", None))
		self.label_5.setText(_translate("MainWindow", "CONEXION", None))
		self.pushButton.setText(_translate("MainWindow", "EXPORTAR", None))
		self.label_6.setText(_translate("MainWindow", "conectados: 0", None))
	
	def exportar(self):
		self.res_var=[]
		fileName = QtGui.QFileDialog.getSaveFileName(MainWindow, 'Open file')#, '/home')getSaveFileName
		#fileName = QtGui.QFileDialog.getOpenFileName(MainWindow, 'Open file')#, '/home')getSaveFileName
		print fileName
		self.res_var=self.res
		self.res_var.append(['----','----','----','----'])
		self.res_var.append(['global: ',self.afavor,self.encontra,self.abstencion])
		my_df = pd.DataFrame(self.res_var)
		my_df.to_csv(str(fileName), index=False, header=['ID','A FAVOR','ENCONTRA','ABSTENCION'])
		print 'se exporto correctamente'



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.mqtt()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
