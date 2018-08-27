from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import controller.SettingDialog as SettingDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('main.ui', self)
        self.buttonDepositeAndBudget.clicked.connect(self.openSettingPage)
    def openSettingPage(self):
        self.settingPage = SettingDialog.SettingDialog() 
        self.settingPage.show()