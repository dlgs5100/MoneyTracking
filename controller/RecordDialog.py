from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
import repository.database as db

class RecordDialog(QtWidgets.QDialog):
    def __init__(self):
        super(RecordDialog,self).__init__()
        loadUi('record.ui', self)
        self.initUI()
    
    def initUI(self):
        self.updateComboboxType()
        self.updateComboboxItem()
        self.buttonBox.accepted.connect(self.listenerAccept)
        # dbO.insertTableSpending('2018-08-31', '食物', '早餐', 50)
        # dbO.insertTableSpending('2018-08-31', '交通', '公車', 15)

    def updateComboboxType(self):
        dbO = db.database()
        self.comboBoxType.setEditable(True)
        self.comboBoxType.addItems(dbO.getAllType())
        self.comboBoxType.currentIndexChanged.connect(self.updateComboboxItem)

    def updateComboboxItem(self):
        dbO = db.database()
        itemChosed = self.comboBoxType.currentText()
        self.comboBoxItem.setEditable(True)
        self.comboBoxItem.clear()
        self.comboBoxItem.addItems(dbO.getAllItemFromType(itemChosed))
    
    def listenerAccept(self):
        dbO = db.database()
        # # self.comboBoxType.currentText()
        # print(dbO.getAllItemFromType())
        