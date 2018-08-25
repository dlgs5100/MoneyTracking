import repository.database as db
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('main.ui', self)
        self.ButtonDepositeAndBudget.clicked.connect(self.openSettingPage)
    def openSettingPage(self):
        self.settingPage = SettingWindow() 
        self.settingPage.show()

class SettingWindow(QtWidgets.QDialog):
    def __init__(self):
        super(SettingWindow,self).__init__()
        loadUi('setting.ui', self)

if __name__ == "__main__":
    # db = db.database()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())