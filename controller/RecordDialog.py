from PyQt5 import QtWidgets
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
        self.checkBoxIncome.stateChanged.connect(lambda: self.changeCBIncome(dbO))
        self.updateComboboxType(dbO)
        self.updateComboboxItem(dbO)
        self.buttonBox.accepted.connect(lambda: self.listenerAccept(dbO))
    
    def changeCBIncome(self, dbO):   #@不確定要不要放兩個
        self.updateComboboxType(dbO)
        self.updateComboboxItem(dbO)

    def updateComboboxType(self, dbO):
        self.comboBoxType.setEditable(True)
        self.comboBoxType.clear()
        if self.checkBoxIncome.isChecked():
            self.comboBoxType.addItems(dbO.getAllTypeFromIncome())
        else:
            self.comboBoxType.addItems(dbO.getAllTypeFromSpending())
        self.comboBoxType.currentIndexChanged.connect(lambda: self.updateComboboxItem(dbO))

    def updateComboboxItem(self, dbO):
        typeChosed = self.comboBoxType.currentText()
        self.comboBoxItem.setEditable(True)
        self.comboBoxItem.clear()
        if self.checkBoxIncome.isChecked():
            self.comboBoxItem.addItems(dbO.getAllItemByTypeFromIncome(typeChosed))
        else:
            self.comboBoxItem.addItems(dbO.getAllItemByTypeFromSpending(typeChosed))
    
    def listenerAccept(self, dbO):
        lastUpdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date = self.calendarWidget.selectedDate().toPyDate()
        type = self.comboBoxType.currentText()
        item = self.comboBoxItem.currentText()
        money = int(self.editMoney.text())

        deposit, temp = dbO.getTotalDeposit()
        if self.checkBoxIncome.isChecked(): #@
            dbO.insertTableIncome(lastUpdate, date, type, item, money)
            dbO.insertTableDeposit(lastUpdate, deposit+money)
        else:
            dbO.insertTableSpending(lastUpdate, date, type, item, money)
            dbO.insertTableDeposit(lastUpdate, deposit-money)

        self.messageDialog = MessageDialog.MessageDialog('新紀錄已存入資料庫')
        self.messageDialog.exec_()
        