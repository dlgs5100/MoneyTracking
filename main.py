import sys
import calendar
import sqlite3
from PyQt5 import QtWidgets
import controller.MainWindow as MainWindow
import repository.database as db

if __name__ == "__main__":
    db = db.database()
    # db.truncateTable('Deposit')
    # db.truncateTable('Budget')
    # db.truncateTable('Spending')

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()
    sys.exit(app.exec_())
