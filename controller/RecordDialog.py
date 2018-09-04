from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
import datetime
import controller.MessageDialog as MessageDialog
import repository.database as db

class RecordDialog(QtWidgets.QDialog):
    def __init__(self):
        super(RecordDialog,self).__init__()
        loadUi('record.ui', self)
        self.initUI()
    
    def initUI(self):
        self.updateComboboxType()
        self.updateComboboxItem()
        self.buttonBox.accepted.connect(self.listenerAccept)

    def updateComboboxType(self):
        dbO = db.database()
        self.comboBoxType.setEditable(True)
        self.comboBoxType.addItems(dbO.getAllType())
        self.comboBoxType.currentIndexChanged.connect(self.updateComboboxItem)

    def updateComboboxItem(self):
        dbO = db.database()
        itemChosed = self.comboBoxType.currentText()
        self.comboBoxItem.setEditable(True)
        self.comboBoxItem.clear()
        self.comboBoxItem.addItems(dbO.getAllItemFromType(itemChosed))
    
    def listenerAccept(self):
        dbO = db.database()
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
        