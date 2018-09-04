from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import datetime
import repository.database as db
import controller.SettingDialog as SettingDialog
import controller.RecordDialog as RecordDialog

class MainWindow(QtWidgets.QMainWindow):
    listCurrentBehavior = []

    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('main.ui', self)
        self.buttonDepositeAndBudget.clicked.connect(self.listenerOpenSettingPage)
        self.buttonNewRecord.clicked.connect(self.listenerOpenRecordPage)
        self.buttonPrevious.clicked.connect(self.listenerPrevious)
        self.updateUI()

    def updateUI(self):
        dbO = db.database()
        mmyyyy = datetime.datetime.now().strftime('%Y-%m')
        totalDeposit, lastUpdate = dbO.getTotalDeposit()
        self.labelUpdateTime.setText(lastUpdate)
        self.labelAutoTotal.setText(str(totalDeposit))
        self.labelAutoMonthlyLast.setText(str(dbO.getTypeBudget(mmyyyy,'月預算') - dbO.getTotalSpending(mmyyyy)))
        self.labelAutoAvgDay.setText(str((dbO.getTypeBudget(mmyyyy,'食物') - dbO.getTypeSpending(mmyyyy,'食物'))/30))

    def listenerOpenSettingPage(self):
        self.settingPage = SettingDialog.SettingDialog() 
        if self.settingPage.exec_() == 1:
            self.listCurrentBehavior.append(1)
        self.updateUI()
        
    def listenerOpenRecordPage(self):
        self.recordPage = RecordDialog.RecordDialog() 
        if self.recordPage.exec_() == 1:
            self.listCurrentBehavior.append(2)
        self.updateUI()
    
    def listenerPrevious(self):
        dbO = db.database()
        latestBehavior = self.listCurrentBehavior.pop(len(self.listCurrentBehavior)-1)
        if latestBehavior == 1:
            dbO.deleteLatestDeposit()
            dbO.deleteLatestBudget()
        elif latestBehavior == 2:
            dbO.deleteLatestDeposit()
            dbO.deleteLatestSpending()
        else:
            print('error')
        self.updateUI()