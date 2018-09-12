import sys
import calendar
import threading
import sqlite3
from PyQt5 import QtWidgets
from win10toast import ToastNotifier
import controller.MainWindow as MainWindow
import repository.database as db

def Toast():
    toaster = ToastNotifier()
    toaster.show_toast('7777')

if __name__ == "__main__":
    db = db.database()

    t = threading.Thread(target = Toast)
    t.start()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()

    sys.exit(app.exec_())
    