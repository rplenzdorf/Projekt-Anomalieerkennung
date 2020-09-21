import time
import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QSizePolicy, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt

from opcua import Server

from MainWindow import Ui_MainWindow


"""
Running Simulation on CMD
current working directory is the folder the .py-file is located
changing the working directory to the folder the simulation is located in
"""
subprocess.Popen('cmd /k "cd ../ & cd ./Modelica/BouncingBallFull_RPi & BouncingBallFull_RPI.exe -embeddedServer=opc-ua -rt=1"')
#opens the command and starts the simulation !parallel! (subprocess.Popen, sonst os.system(...)) to the main.py  
#os.system('cmd /k "cd ../ & cd ./Modelica/BouncingBallFull_RPi & BouncingBallFull_RPI.exe -embeddedServer=opc-ua -rt=1"') #os.system command

"""
Setting up Server
"""

server = Server()
url = "opc.tcp://192.168.0.13:4840" # Ip anpassen
server.set_endpoint(url)

name = "OPCUA_SERVER"
addspace = server.register_namespace(name) #addspace = server.get_objects_node()

node = server.get_objects_node()

param = node.add_object(addspace, "parameters")

DesE = param.add_variable(addspace, "Descend e", 0)
AscE = param.add_variable(addspace, "Ascend e", 0)

DesE.set_writable()
AscE.set_writable()

server.start()







class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.setupUi(self)
        self.show()

        self.setWindowTitle("TEST opcua")

        self.btn_1.pressed.connect(self.press_1)

        self.btn_1.clicked.connect(self.release_1)

        self.btn_2.pressed.connect(self.press_2)

        self.btn_2.clicked.connect(self.release_2)

    def press_1(self):
        DesE.set_value(1)
        print("gedrückt")

    def release_1(self):
        DesE.set_value(0)
        print("losgelassen")

    def press_2(self):
        AscE.set_value(1)
        print("gedrückt")

    def release_2(self):
        AscE.set_value(0)
        print("losgelassen")


if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())
