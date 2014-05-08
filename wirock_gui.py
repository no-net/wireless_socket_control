from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

import wirock
from wirock_topblock import top_block


class MainDialog(QDialog, wirock.Ui_dialog):

    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.tb = top_block()

        self.connect(self.onButton, SIGNAL("clicked()"), self.turn_on)
        self.connect(self.offButton, SIGNAL("clicked()"), self.turn_off)

    def turn_on(self):
        print "Turn on!"
        self.refresh_tb()
        self.tb.set_func("on")
        self.tb.run()

    def turn_off(self):
        print "Turn off!"
        self.refresh_tb()
        self.tb.set_func("off")
        self.tb.unlock()

    def refresh_tb(self):
        self.tb.set_dip_conf(self.evaluate_dip())
        self.tb.set_gain(int(self.gainSlider.value()))
        self.tb.set_device(self.devtypeBox.currentText(), self.devaddrEdit.text())
        self.tb.set_socket(str(self.comboBox.itemText(self.comboBox.currentIndex())))

    def evaluate_dip(self):
        dips = []
        dips.append(self.checkBox_1.isChecked())
        dips.append(self.checkBox_2.isChecked())
        dips.append(self.checkBox_3.isChecked())
        dips.append(self.checkBox_4.isChecked())
        dips.append(self.checkBox_5.isChecked())

        dip_config = ''

        for dip in dips:
            if dip:
                dip_config += '1'
            else:
                dip_config += '0'
        print "DIP config:", dip_config

        return dip_config


app = QApplication(sys.argv)
form = MainDialog()
form.show()
app.exec_()
