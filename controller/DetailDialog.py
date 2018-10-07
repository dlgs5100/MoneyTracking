from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
import repository.database as db

class DetailDialog(QtWidgets.QDialog):
    def __init__(self, type, mmyyyy, attribute):
        super(DetailDialog,self).__init__()
        loadUi('detail.ui', self)
        self.dbO = db.database()
        self.updateUI(type, mmyyyy, attribute)
    
    def listenerDelete(self, row):
        button = self.sender()
        x = self.gridLayout.indexOf(button)
        location = self.gridLayout.getItemPosition(x)

        id_wanna_delete = int(self.gridLayout.itemAtPosition(location[0],0).widget().text())
        print(id_wanna_delete)

    def updateUI(self, type, mmyyyy, attribute):
        self.labelType.setText(type)
        self.attribute = attribute
        if self.attribute == 'spending':
            detail = self.dbO.getDetailByTypeFromSpending(type, mmyyyy)
        elif self.attribute == 'income':
            detail = self.dbO.getDetailByTypeFromIncome(type, mmyyyy)
        
        widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(widget)
        self.gridLayout = QtWidgets.QGridLayout(widget)

        row = 0
        colume = 0
        self.listButton = []
        for listDetail in detail:
            self.gridLayout.addWidget(QtWidgets.QLabel(str(listDetail[0])), row, colume)
            self.gridLayout.addWidget(QtWidgets.QLabel(str(listDetail[1])), row, colume+1)
            self.gridLayout.addWidget(QtWidgets.QLabel(str(listDetail[2])), row, colume+2)
            self.gridLayout.addWidget(QtWidgets.QLabel(str(listDetail[3])), row, colume+3)
            self.listButton.append(QtWidgets.QPushButton('刪除'))
            self.listButton[row].clicked.connect(lambda state, x = row: self.listenerDelete(x))
            self.gridLayout.addWidget(self.listButton[row], row, colume+4)
            row = row + 1
