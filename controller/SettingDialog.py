from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
import datetime
import controller.MessageDialog as MessageDialog
import repository.database as db

class SettingDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SettingDialog,self).__init__()
        loadUi('setting.ui', self)
        dbO = db.database()
        self.initUI(dbO)
    
    def initUI(self, dbO):
        self.labelYear.setText(str(datetime.datetime.now().year))
        for i in range (1,13):
            if i < 10:
                self.comboBoxMonth.addItem('0' + str(i))
            else:
                self.comboBoxMonth.addItem(str(i))
        now = datetime.datetime.now()
        self.comboBoxMonth.setCurrentIndex(now.month-1)
                
        deposit, temp = dbO.getTotalDeposit()
        self.editDeposit.setText(str(deposit))
        self.buttonInsertRow.clicked.connect(self.listenerInsertRow)
        self.buttonBox.accepted.connect(lambda: self.listenerAccept(dbO))

    def listenerInsertRow(self):
        rowPosition = self.tableBudget.rowCount()
        self.tableBudget.insertRow(rowPosition)

    def listenerAccept(self, dbO):
        lastUpdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        deposit = int(self.editDeposit.text())
        
        mmyyyy = str(datetime.datetime.now().year) + '-' + str(self.comboBoxMonth.currentText())
        monthlyBudget = int(self.editMonthlyBudget.text())
        
        totalBudget = 0
        for row in range (0, self.tableBudget.rowCount()):
            totalBudget += int(self.tableBudget.item(row,1).text())
        
        if monthlyBudget < 0:
            message = '總預算必須為正數'
        elif totalBudget != monthlyBudget:
            message = '各項預算總和與總預算不符'
        else:
            dbO.insertTableDeposit(lastUpdate, deposit)
            dbO.insertTableBudget(lastUpdate, mmyyyy, '月預算', monthlyBudget)
            for row in range (0, self.tableBudget.rowCount()):
                type = self.tableBudget.item(row,0).text()
                budget = self.tableBudget.item(row,1).text()
                dbO.insertTableBudget(lastUpdate, mmyyyy, type, budget)
                message = '存款/預算已存入資料庫'
        
        self.messageDialog = MessageDialog.MessageDialog(message)
        self.messageDialog.exec_()