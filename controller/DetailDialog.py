from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import repository.database as db

class DetailDialog(QtWidgets.QDialog):
    def __init__(self, type, mmyyyy, attribute):
        super(DetailDialog,self).__init__()
        loadUi('detail.ui', self)
        self.dbO = db.database()
        self.updateUI(type, mmyyyy, attribute)

    #     self.buttonLeave.clicked.connect(self.listenerLeave)
    
    # def listenerLeave(self):
    #     # self.HBox = QtWidgets.QHBoxLayout()
    #     # self.HBox.addWidget(QtWidgets.QLabel('123'))
    #     # self.VBox.addLayout(self.HBox)
    #     self.VBox.addWidget(QtWidgets.QLabel(str(1)))

    def updateUI(self, type, mmyyyy, attribute):
        self.labelType.setText(type)
        if attribute == 'spending':
            detail = self.dbO.getDetailByTypeFromSpending(type, mmyyyy)
        elif attribute == 'income':
            detail = self.dbO.getDetailByTypeFromIncome(type, mmyyyy)

        print(detail)
        
        row = 0
        colume = 0
        widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(widget)
        self.gridLayout = QtWidgets.QGridLayout(widget)

        for listDetail in detail:
            self.gridLayout.addWidget(QtWidgets.QLabel(str(listDetail[0])), row, colume)
            self.gridLayout.addWidget(QtWidgets.QLabel(str(listDetail[1])), row, colume+1)
            self.gridLayout.addWidget(QtWidgets.QLabel(str(listDetail[2])), row, colume+2)
            self.gridLayout.addWidget(QtWidgets.QLabel(str(listDetail[3])), row, colume+3)
            self.gridLayout.addWidget(QtWidgets.QPushButton('刪除'), row, colume+4)
            row = row + 1
