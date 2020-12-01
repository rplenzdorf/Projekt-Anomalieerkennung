import time
import sys
import os
import subprocess
import serial
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from random import randint
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QSizePolicy, QVBoxLayout, QSlider, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5 import uic


pressed = False
pen = pg.mkPen(color=(255, 255, 255))
a = 0

#-------------- Definition der Variablen mit OPC UA ----------------
# P_ist_Wr1 = clientOME.get_node("ns=1;i= ----- ")
# P_soll_Wr1 = clientOME.get_node("ns=1;i= ----- ")
# P_ist_Wr2 = clientOME.get_node("ns=1;i= ----- ")
# P_soll_Wr2 = clientOME.get_node("ns=1;i= ----- ")
# P_ist_Wr3 = clientOME.get_node("ns=1;i= ----- ")
# P_soll_Wr3 = clientOME.get_node("ns=1;i= ----- ")




#------------- QT ---------------------
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)

        uic.loadUi("MainWindow.ui",self)
        global pen
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)

        self.plot_timer = QtCore.QTimer()
        self.plot_timer.setInterval(50)
        self.plot_timer.timeout.connect(self.update_plot_data)
        self.plot_timer.start()

        self.serial_timer = QtCore.QTimer()
        self.serial_timer.setInterval(100)
        self.serial_timer.timeout.connect(self.send_serial)
        self.serial_timer.start()

        self.btn_Home.clicked.connect(self.change_Home)
        self.btn_Wr1.clicked.connect(self.change_Wr1)
        self.btn_Wr2.clicked.connect(self.change_Wr2)
        self.btn_Wr3.clicked.connect(self.change_Wr3)
        self.btn_Daten.clicked.connect(self.change_Daten)

        self.sli_Pist_Wr1.valueChanged.connect(self.update_Slider_Pist_Wr1)
        self.sli_Pist_Wr2.valueChanged.connect(self.update_Slider_Pist_Wr2)
        self.sli_Pist_Wr3.valueChanged.connect(self.update_Slider_Pist_Wr3)
        self.sli_Psoll_Wr1.valueChanged.connect(self.update_Slider_Psoll_Wr1)
        self.sli_Psoll_Wr2.valueChanged.connect(self.update_Slider_Psoll_Wr2)
        self.sli_Psoll_Wr3.valueChanged.connect(self.update_Slider_Psoll_Wr3)


    def change_Home(self):
        self.stackedWidget.setCurrentIndex(1)
        self.btn_Home.setChecked(True)
        self.btn_Wr1.setChecked(False)
        self.btn_Wr2.setChecked(False)
        self.btn_Wr3.setChecked(False)
        self.btn_Daten.setChecked(False)     
    def change_Wr1(self):
        self.stackedWidget.setCurrentIndex(2)
        self.btn_Home.setChecked(False)
        self.btn_Wr1.setChecked(True)
        self.btn_Wr2.setChecked(False)
        self.btn_Wr3.setChecked(False)
        self.btn_Daten.setChecked(False)
    def change_Wr2(self):
        self.stackedWidget.setCurrentIndex(3)
        self.btn_Home.setChecked(False)
        self.btn_Wr1.setChecked(False)
        self.btn_Wr2.setChecked(True)
        self.btn_Wr3.setChecked(False)
        self.btn_Daten.setChecked(False)
    def change_Wr3(self):
        self.stackedWidget.setCurrentIndex(4)
        self.btn_Home.setChecked(False)
        self.btn_Wr1.setChecked(False)
        self.btn_Wr2.setChecked(False)
        self.btn_Wr3.setChecked(True)
        self.btn_Daten.setChecked(False)
    def change_Daten(self):
        self.stackedWidget.setCurrentIndex(0)
        self.btn_Home.setChecked(False)
        self.btn_Wr1.setChecked(False)
        self.btn_Wr2.setChecked(False)
        self.btn_Wr3.setChecked(False)
        self.btn_Daten.setChecked(True)

    def update_Slider_Pist_Wr1(self):
        Pist_Wr1_hack = self.sli_Pist_Wr1.value()
        self.num_Pist_Wr1.setText(str(Pist_Wr1_hack))
        
    def update_Slider_Pist_Wr2(self):
        Pist_Wr2_hack = self.sli_Pist_Wr2.value()
        self.num_Pist_Wr2.setText(str(Pist_Wr2_hack))

    def update_Slider_Pist_Wr3(self):
        Pist_Wr3_hack = self.sli_Pist_Wr3.value()
        self.num_Pist_Wr3.setText(str(Pist_Wr3_hack))

    def update_Slider_Psoll_Wr1(self):
        Psoll_Wr1_hack = self.sli_Psoll_Wr1.value()
        self.num_Psoll_Wr1.setText(str(Psoll_Wr1_hack))
        
    def update_Slider_Psoll_Wr2(self):
        Psoll_Wr2_hack = self.sli_Psoll_Wr2.value()
        self.num_Psoll_Wr2.setText(str(Psoll_Wr2_hack))

    def update_Slider_Psoll_Wr3(self):
        Psoll_Wr3_hack = self.sli_Psoll_Wr3.value()
        self.num_Psoll_Wr3.setText(str(Psoll_Wr3_hack))

    def update_plot_data(self):
        global pen

        if self.check_Red.isChecked():
            pen = pg.mkPen(color=(255, 0, 0))
            self.check_Green.setChecked(False)      
            self.check_Blue.setChecked(False)
            y_neu = 1

        elif self.check_Green.isChecked():
            pen = pg.mkPen(color=(0, 255, 0))
            self.check_Red.setChecked(False)
            self.check_Blue.setChecked(False)
            y_neu = 2

        elif self.check_Blue.isChecked():
            pen = pg.mkPen(color=(0, 0, 255))
            self.check_Green.setChecked(False)
            self.check_Red.setChecked(False)
            y_neu = 3

        else:    
            pen = pg.mkPen(color=(0, 0, 0))
            self.check_Green.setChecked(False)
            self.check_Blue.setChecked(False)
            self.check_Red.setChecked(False)
            y_neu = 0

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first 
        self.y.append(y_neu)  # Add a new random value.

        self.data_line.setData(self.x, self.y, pen=pen)  # Update the data.


# Übergabe an Arduino: Trennung: :, Ende: \n, Reihenfolge: Wr1, Wr2, Wr3, P_soll_gesamt, P_ist_gesamt 


if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)

    w = MainWindow()
    w.stackedWidget.setCurrentIndex(1)
    w.show()

    sys.exit(app.exec_())
   