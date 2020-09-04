import time
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QSizePolicy, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt

from opcua import Server

from MainWindow import Ui_MainWindow

server = Server()
url = "opc.tcp://129.168.0.10:4840" # Ip anpassen

server.set_endpoint(url)
name = "OPCUA_SERVER"
addspace = server.get_objects_node()

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
        AscE.set_value(1)
        print("gedrückt")


if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())