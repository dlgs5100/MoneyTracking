import datetime
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
import repository.database as db

class SettingDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SettingDialog,self).__init__()
        loadUi('setting.ui', self)

        self.labelYear.setText(str(datetime.datetime.now().year))
        for i in range (1,13):
            if i < 10:
                self.comboBoxMonth.addItem('0' + str(i))
            else:
                self.comboBoxMonth.addItem(str(i))
        self.buttonInsertRow.clicked.connect(self.listenerInsertRow)
        self.buttonBox.accepted.connect(self.listenerAccept)

        # self.comboBoxMonth.activated[str].connect(self.onActivated)
    
    def listenerInsertRow(self):
        rowPosition = self.tableBudget.rowCount()
        self.tableBudget.insertRow(rowPosition)
        
    # def onActivated(self, text):
    #     self.lb1.setText(text)
    #     self.lb1.adjustSize()