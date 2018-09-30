from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import datetime
import calendar
import matplotlib.pyplot as plt
import repository.database as db
import controller.SettingDialog as SettingDialog
import controller.RecordDialog as RecordDialog
import controller.MessageDialog as MessageDialog
import controller.PlotWindow as PlotWindow

class MainWindow(QtWidgets.QMainWindow):
    listCurrentBehavior = []

    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('main.ui', self)
        dbO = db.database()
        self.buttonDepositeAndBudget.clicked.connect(lambda: self.listenerOpenSettingPage(dbO))
        self.buttonNewRecord.clicked.connect(lambda: self.listenerOpenRecordPage(dbO))
        self.buttonPrevious.clicked.connect(lambda: self.listenerPrevious(dbO))
        self.buttonMonthlyReport.clicked.connect(self.listenerOpenPieChart)
        self.updateUI(dbO)

    def updateUI(self, dbO):
        mmyyyy = datetime.datetime.now().strftime('%Y-%m')
        totalDeposit, lastUpdate = dbO.getTotalDeposit()
        self.labelUpdateTime.setText(lastUpdate)
        self.labelAutoTotal.setText(str(totalDeposit))
        self.labelAutoMonthlyLast.setText(str(dbO.getTypeBudget(mmyyyy,'月預算')-dbO.getTotalSpending(mmyyyy)))
        self.labelAutoMonthlyIncome.setText(str(dbO.getTotalIncome(mmyyyy)))
        totalDays = calendar.mdays[int(datetime.datetime.now().strftime('%m'))]
        nowDay = int(datetime.datetime.now().strftime('%d'))
        perDayEat = (dbO.getTypeBudget(mmyyyy,'食物')-dbO.getTypeSpending(mmyyyy,'食物')) / (totalDays-nowDay+1)
        self.labelAutoAvgDay.setText(str(round(perDayEat,2)))

    def listenerOpenSettingPage(self, dbO):
        self.settingPage = SettingDialog.SettingDialog() 
        if self.settingPage.exec_() == 1:
            self.listCurrentBehavior.append(1)
        self.updateUI(dbO)

    def listenerOpenRecordPage(self, dbO):
        self.recordPage = RecordDialog.RecordDialog() 
        if self.recordPage.exec_() == 1:
            if self.recordPage.recording['IncomeOrSpending'] == 'Spending':  
                self.listCurrentBehavior.append(2)
            elif self.recordPage.recording['IncomeOrSpending'] == 'Income': 
                self.listCurrentBehavior.append(3)
        self.updateUI(dbO)
    
    def listenerOpenPieChart(self):
        self.plotWindow = PlotWindow.PlotWindow()
        self.plotWindow.show()
    
    def listenerPrevious(self, dbO):
        if len(self.listCurrentBehavior) != 0:
            latestBehavior = self.listCurrentBehavior.pop(len(self.listCurrentBehavior)-1)
            if latestBehavior == 1:
                dbO.deleteLatestDeposit()
                dbO.deleteLatestBudget()
                message = '成功復原(存款/預算)'
            elif latestBehavior == 2:
                dbO.deleteLatestDeposit()
                dbO.deleteLatestSpending()
                message = '成功復原(新紀錄:支出)'
            elif latestBehavior == 3:
                dbO.deleteLatestDeposit()
                dbO.deleteLatestIncome()
                message = '成功復原(新紀錄:收入)'
            else:
                message = '復原產生未知的錯誤'
            self.updateUI(dbO)
        else:
            message = '無法復原'
        self.messageDialog = MessageDialog.MessageDialog(message)
        self.messageDialog.exec_()
        