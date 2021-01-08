import time
import sys
import os
import subprocess
import serial
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from random import randint
from numpy import genfromtxt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QSizePolicy, QVBoxLayout, QSlider, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5 import uic

#--------------- Alllgemeine Definitionen ------------------
AnAus = True
custom_Wind = True
pen = pg.mkPen(color=(255, 255, 255))
a = 0
Anomalie = False
wind_gain = 8
wind = 1
index_Wind = 1

#--------------- Winddaten aus csv -----------------------
winddata = genfromtxt('Winddata.csv', delimiter=',')
wind_speed = winddata[:,1]

#--------------- Setup Serial -----------------------
# arduino_write = serial.Serial("")
# arduino_read = serial.Serial("")

#-------------- Setup OPCUA Client --------------------
sim_place = input("Wo soll die Simulation laufen?\n(1) Raspberry Pi\n(2) Server")
if sim_place == 1:
    urlOME = "opc.tcp://localhost:4841"
elif sim_place == 2:
    pass
    #urlOME = "opc.tcp://IP:4841" ====IP einfügen====

clientOME = Client(urlOME)
clientOME.connect()
print("OME Client connected")

if sim_place == 1:
    pass
    #subprocess.Popen('cmd /k "cd ../ & cd ./Modelica/BouncingBallFull_RPi & BouncingBallFull_RPI.exe -embeddedServer=opc-ua -rt=1"')
    #Richtigen Pfad einfügen
    run = clientOME.get_node("ns=1;i= ----- ")
    run.set_value(float(1))
#-------------- Definition der Variablen mit OPC UA ----------------

# P_ist_Wr1 = clientOME.get_node("ns=1;i=100000767")
# P_soll_Wr1 = clientOME.get_node("ns=1;i= ----- ")
# P_ist_Wr2 = clientOME.get_node("ns=1;i=100001443")
# P_soll_Wr2 = clientOME.get_node("ns=1;i= ----- ")
# P_ist_Wr3 = clientOME.get_node("ns=1;i=100002119")
# P_soll_Wr3 = clientOME.get_node("ns=1;i= ----- ")

# P_max_Wr1 = clientOME.get_node("ns=1;i=150001523")
# P_max_Wr2 = clientOME.get_node("ns=1;i=150003429")
# P_max_Wr3 = clientOME.get_node("ns=1;i=150005335")

# beta_Wr1 = clientOME.get_node("ns=1;i=150001524")
# beta_Wr2 = clientOME.get_node("ns=1;i=150003430")
# beta_Wr3 = clientOME.get_node("ns=1;i=150005336")

# hack = clientOME.get_node("ns=1;i= ----- ")

# P_ges = clientOME.get_node("ns=1;i=150001523")

# P_soll = clientOME.get_node("ns=1;i=100000189")

# Wind = clientOME.get_node("ns=1;i=100000190")


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
        self.plot_timer.setInterval(100)
        self.plot_timer.timeout.connect(self.update_plot_data)
        self.plot_timer.timeout.connect(self.send_sim)
        self.plot_timer.start()


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

        self.sli_P_Stadt.valueChanged.connect(self.update_Slider_Stadt)

        self.btn_Reset.clicked.connect(self.reset)
        self.btn_Hack.clicked.connect(self.hack)

        self.btn_AnAus.clicked.connect(self.anaus)
        self.btn_Wind.clicked.connect(self.change_Wind)

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
        self.num_sli_Pist_Wr1.setText(str(Pist_Wr1_hack))
        
    def update_Slider_Pist_Wr2(self):
        Pist_Wr2_hack = self.sli_Pist_Wr2.value()
        self.num_sli_Pist_Wr2.setText(str(Pist_Wr2_hack))

    def update_Slider_Pist_Wr3(self):
        Pist_Wr3_hack = self.sli_Pist_Wr3.value()
        self.num_sli_Pist_Wr3.setText(str(Pist_Wr3_hack))

    def update_Slider_Psoll_Wr1(self):
        Psoll_Wr1_hack = self.sli_Psoll_Wr1.value()
        self.num_sli_Psoll_Wr1.setText(str(Psoll_Wr1_hack))
        
    def update_Slider_Psoll_Wr2(self):
        Psoll_Wr2_hack = self.sli_Psoll_Wr2.value()
        self.num_sli_Psoll_Wr2.setText(str(Psoll_Wr2_hack))

    def update_Slider_Psoll_Wr3(self):
        Psoll_Wr3_hack = self.sli_Psoll_Wr3.value()
        self.num_sli_Psoll_Wr3.setText(str(Psoll_Wr3_hack))

    def update_Slider_Stadt(self):
        P_Stadt = self.sli_P_Stadt.value()
        self.num_sli_P_Stadt.setText(str(P_Stadt))
        #P_Verbrauch.setValue(float(P_ges))

    def reset(self):
        self.sli_Pist_Wr1.setValue(0)
        self.sli_Pist_Wr2.setValue(0)
        self.sli_Pist_Wr3.setValue(0)
        self.sli_Psoll_Wr1.setValue(0)
        self.sli_Psoll_Wr2.setValue(0)
        self.sli_Psoll_Wr3.setValue(0)

        # hack.set_value(float(10))

        time.sleep(5)

    def hack(self):
        P_ist_Wr1_hack.set_value(float(P_ist_Wr1 + self.sli_Pist_Wr1.value() ))
        P_ist_Wr2_hack.set_value(float(P_ist_Wr2 + self.sli_Pist_Wr2.value() ))
        P_ist_Wr3_hack.set_value(float(P_ist_Wr3 + self.sli_Pist_Wr3.value() ))
        P_soll_Wr1_hack.set_value(float(P_soll_Wr1 + self.sli_Psoll_Wr1.value() ))
        P_soll_Wr2_hack.set_value(float(P_soll_Wr2 + self.sli_Psoll_Wr2.value() ))
        P_soll_Wr3_hack.set_value(float(P_soll_Wr3 + self.sli_Psoll_Wr1.value() ))

    def anaus(self):
        global AnAus
        if AnAus:
            self.btn_AnAus.setText("Anomalieerkennung\nAUS")
            self.btn_AnAus.setStyleSheet("background-color: rgb(255, 153, 153);")
            AnAus = False
        else:
            self.btn_AnAus.setText("Anomalieerkennung\nAN")
            self.btn_AnAus.setStyleSheet("background-color: rgb(189, 255, 170);")
            AnAus = True

    def change_Wind(self):
        global custom_Wind
        if custom_Wind:
            self.btn_Wind.setText("Winddaten\nAutomatisch")
            custom_Wind = False
        else:
            self.btn_Wind.setText("Winddaten\nManuell")
            custom_Wind = True

    def send_serial(self):
        pass
        #global n_Wr1, n_Wr2, n_Wr3, Pist_gesamt, P_ges
        #arduino_write.write(str(n_Wr1)+":"+str(n_Wr2)+":"+str(n_Wr3)+":"+str(Pist_gesamt)+":"+str(P_ges)+"\n").encode("utf8")
        #Wind = int(arduino_read.read())

    def update_numbers(self):
        pass
        #self.num_P_ges.setText(str(P_ges))
        #self.num_P_Stadt.setText(str(P_Stadt))
        #self.num_P_imp.setText(str(P_imp))

        # self.num_Pist_Wr1.setText(str(P_ist_Wr1))
        # self.num_Psoll_Wr1.setText(str(P_soll_Wr1))
        # self.num_beta_Wr1.setText(str(beta_Wr1))
        # self.num_lambda_Wr1.setText(str(lambda_Wr1))

        # self.num_Pist_Wr2.setText(str(P_ist_Wr2))
        # self.num_Psoll_Wr2.setText(str(P_soll_Wr2))
        # self.num_beta_Wr2.setText(str(beta_Wr2))
        # self.num_lambda_Wr2.setText(str(lambda_Wr2))

        # self.num_Pist_Wr3.setText(str(P_ist_Wr3))
        # self.num_Psoll_Wr3.setText(str(P_soll_Wr3))
        # self.num_beta_Wr3.setText(str(beta_Wr3))
        # self.num_lambda_Wr3.setText(str(lambda_Wr3))

    def update_plot_data(self):
        global pen
        if self.check_Pges.isChecked():
            pen = pg.mkPen(color=(255, 0, 0))
            self.check_Psoll.setChecked(False)      
            self.check_wind.setChecked(False)
            self.check_beta.setChecked(False)
            y_neu = 1

        elif self.check_Psoll.isChecked():
            pen = pg.mkPen(color=(0, 255, 0))
            self.check_Pges.setChecked(False)
            self.check_wind.setChecked(False)
            self.check_beta.setChecked(False)
            y_neu = 2

        elif self.check_wind.isChecked():
            pen = pg.mkPen(color=(0, 0, 255))
            self.check_Pges.setChecked(False)
            self.check_Psoll.setChecked(False)
            self.check_beta.setChecked(False)
            y_neu = wind

        elif self.check_beta.isChecked():
            pen = pg.mkPen(color=(0, 0, 255))
            self.check_Pges.setChecked(False)
            self.check_Psoll.setChecked(False)
            self.check_wind.setChecked(False)
            y_neu = 3

        else:    
            pen = pg.mkPen(color=(0, 0, 0))
            self.check_Pges.setChecked(False)
            self.check_Psoll.setChecked(False)
            self.check_wind.setChecked(False)
            self.check_beta.setChecked(False)
            y_neu = 0

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first 
        self.y.append(y_neu)  # Add a new random value.

        self.data_line.setData(self.x, self.y, pen=pen)  # Update the data.

    def send_sim(self):
        global Anomalie, wind_gain, index_Wind, wind

        print("tick")

        if custom_Wind:
            pass
            #wind = ser.read(...)
        else:
            wind = wind_speed[index_Wind] * wind_gain
            print(wind)
            index_Wind += 1
            if index_Wind == 86399:
                index_Wind = 0


        # if P_ges > P_ist:
        #     self.sym_Unzureichend.setHidden(False)
        # else:
        #     self.sym_Unzureichend.set.setHidden(True)

        # if P_ges > P_ist:
        #     self.sym_Ueberlastet.setHidden(False)
        # else:
        #     self.sym_Uerberlastet.setHidden(True)

        # if Anmomalie:
        #     self.sym_Erkannt.setHidden(False)
        # else:
        #     self.sym_Erkannt.set.setHidden(True)
        
        Wind.set_value(float(wind))



    def check_anomalie(self):
        pass


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    w = MainWindow()
    w.stackedWidget.setCurrentIndex(1)
    w.show()

    sys.exit(app.exec_())
   