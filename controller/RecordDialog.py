from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
import datetime
import controller.MessageDialog as MessageDialog
import repository.database as db

class RecordDialog(QtWidgets.QDialog):
    def __init__(self):
        super(RecordDialog,self).__init__()
        loadUi('record.ui', self)
        dbO = db.database()
        self.initUI(dbO)
    
    def initUI(self, dbO):
        self.updateComboboxType(dbO)
        self.updateComboboxItem(dbO)
        self.buttonBox.accepted.connect(lambda: self.listenerAccept(dbO))

    def updateComboboxType(self, dbO):
        self.comboBoxType.setEditable(True)
        self.comboBoxType.addItems(dbO.getAllType())
        self.comboBoxType.currentIndexChanged.connect(lambda: self.updateComboboxItem(dbO))

    def updateComboboxItem(self, dbO):
        itemChosed = self.comboBoxType.currentText()
        self.comboBoxItem.setEditable(True)
        self.comboBoxItem.clear()
        self.comboBoxItem.addItems(dbO.getAllItemFromType(itemChosed))
    
    def listenerAccept(self, dbO):
        lastUpdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date = self.calendarWidget.selectedDate().toPyDate()
        type = self.comboBoxType.currentText()
        item = self.comboBoxItem.currentText()
        spending = int(self.editSpending.text())
        dbO.insertTableSpending(lastUpdate, date, type, item, spending)
        
        deposit, temp = dbO.getTotalDeposit()
        dbO.insertTableDeposit(lastUpdate, deposit-spending)

        self.messageDialog = MessageDialog.MessageDialog('新紀錄已存入資料庫')
        self.messageDialog.exec_()
        