import sys
import calendar
import datetime
import threading
import sqlite3
from PyQt5 import QtWidgets
from win10toast import ToastNotifier
import controller.MainWindow as MainWindow
import repository.database as db

def Toast(dbO):
    spendingDate = dbO.getLatestSpendingDate()
    incomeDate = dbO.getLatestIncomeDate()
    Date = spendingDate if spendingDate >= incomeDate else incomeDate
    
    if Date != 0:
        temp = datetime.datetime.strptime(Date, "%Y-%m-%d")
        nowDate = datetime.datetime.now()
        toaster = ToastNotifier()
        toaster.show_toast('最後一次紀錄為 : ' + str((nowDate-temp).days)+'天前\n'+Date)

if __name__ == "__main__":
    dbO = db.database()

    t = threading.Thread(target = Toast, args = (dbO,))
    t.start()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()

    sys.exit(app.exec_())
    