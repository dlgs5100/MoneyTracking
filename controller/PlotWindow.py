from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import repository.database as db

class PlotWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PlotWindow,self).__init__()
        loadUi('plot.ui', self)
        dbO = db.database()
        self.initUI(dbO)

    def initUI(self, dbO):
        self.updateCombox(dbO)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.buttonShow.clicked.connect(lambda: self.listenerShow(dbO))
        self.verticalLayout.addWidget(self.canvas)

    def updateCombox(self, dbO):
        self.comboBoxMMYYYY.setEditable(False)
        self.comboBoxMMYYYY.addItems(dbO.getAllYearsAndMonthInSpending())

    def listenerShow(self, dbO):
        plt.clf()

        mmyyyy = self.comboBoxMMYYYY.currentText()
        listType = dbO.getAllTypeByMMYYY(mmyyyy)

        listCost = []
        for type in listType:
            listCost.append(dbO.getAllCostFromType(type, mmyyyy))
        
        plt.rcParams['font.family']='DFKai-SB'
        plt.rcParams['axes.unicode_minus']=False
        plt.pie(listCost , labels = listType, autopct='%1.1f%%')
        plt.axis('equal')
        
        self.canvas.draw()
        