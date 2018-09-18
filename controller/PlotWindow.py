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
        self.buttonShow.clicked.connect(lambda: self.listenerShow(dbO))

        self.figure = plt.figure()
        self.canvasSpending = FigureCanvas(self.figure)
        self.canvasIncome = FigureCanvas(self.figure)
        self.VLayoutSpending.addWidget(self.canvasSpending)
        self.VLayoutIncome.addWidget(self.canvasIncome)

    def updateCombox(self, dbO):
        self.comboBoxMMYYYY.setEditable(False)
        self.comboBoxMMYYYY.addItems(dbO.getAllYearsAndMonthInSpending())

    def listenerShow(self, dbO):
        plt.clf()

        mmyyyy = self.comboBoxMMYYYY.currentText()
        listType = dbO.getAllTypeByMMYYYFromSpending(mmyyyy)

        listCost = []
        i = 0
        for type in listType:
            listCost.append(dbO.getAllCostByTypeFromSpending(type, mmyyyy))
            listType[i] += ' ' + str(+listCost[i])
            i+=1
        
        plt.rcParams['font.family']='DFKai-SB'
        plt.rcParams['axes.unicode_minus']=False
        plt.pie(listCost , labels = listType, autopct='%1.1f%%')
        plt.axis('equal')

        self.canvasSpending.draw()

        ###

        plt.clf()

        listType = dbO.getAllTypeByMMYYYFromIncome(mmyyyy)
        listCost = []
        i = 0
        for type in listType:
            listCost.append(dbO.getAllCostByTypeFromIncome(type, mmyyyy))
            listType[i] += ' ' + str(+listCost[i])
            i+=1
    
        plt.rcParams['font.family']='DFKai-SB'
        plt.rcParams['axes.unicode_minus']=False
        plt.pie(listCost , labels = listType, autopct='%1.1f%%')
        plt.axis('equal')
        
        self.canvasIncome.draw()
        