from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import datetime
import repository.database as db
import controller.SettingDialog as SettingDialog
import controller.RecordDialog as RecordDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('main.ui', self)
        self.buttonDepositeAndBudget.clicked.connect(self.openSettingPage)
        self.buttonNewRecord.clicked.connect(self.openRecordPage)
        self.updateUI()

    def updateUI(self):
        dbO = db.database()
        totalDeposit, lastUpdate = dbO.getTotalDeposit()
        self.labelUpdateTime.setText(lastUpdate)
        self.labelAutoTotal.setText(str(totalDeposit))
        self.labelAutoMonthlyLast.setText(str(dbO.getTypeBudget('2018-08','月預算') - dbO.getTotalSpending('2018-08')))
        self.labelAutoAvgDay.setText(str((dbO.getTypeBudget('2018-08','食物') - dbO.getTypeSpending('2018-08','食物'))/30))

    def openSettingPage(self):
        self.settingPage = SettingDialog.SettingDialog() 
        self.settingPage.exec_()
        self.updateUI()

    def openRecordPage(self):
        self.recordPage = RecordDialog.RecordDialog() 
        self.recordPage.exec_()
        self.updateUI()