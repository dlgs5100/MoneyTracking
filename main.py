import sys
from PyQt5 import QtWidgets
import controller.MainWindow as MainWindow
import sqlite3
import repository.database as db

if __name__ == "__main__":
    db = db.database()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()
    sys.exit(app.exec_())

    # conn = sqlite3.connect('dbmoneytracking.db')
    # cursor = conn.cursor()
    # sqlTruncateTable = "DROP TABLE Deposit"
    # cursor.execute(sqlTruncateTable)
    # cursor.close()
    # conn.commit()
    # conn.close()