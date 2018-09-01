from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
import datetime
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
        date = self.calendarWidget.selectedDate().toPyDate()
        type = self.comboBoxType.currentText()
        item = self.comboBoxItem.currentText()
        spending = int(self.editSpending.text())
        dbO.insertTableSpending(date, type, item, spending)
        
        lastUpdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        deposit, temp = dbO.getTotalDeposit()
        dbO.insertTableDeposit(lastUpdate, deposit-spending)
        