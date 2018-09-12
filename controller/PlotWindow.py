from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import repository.database as db

class PlotWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PlotWindow,self).__init__()
        loadUi('plot.ui', self)
        self.initUI()

    def initUI(self):
        self.updateCombox()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.buttonShow.clicked.connect(self.listenerShow)
        self.verticalLayout.addWidget(self.canvas)

    def updateCombox(self):
        dbO = db.database()
        self.comboBoxMMYYYY.setEditable(False)
        self.comboBoxMMYYYY.addItems(dbO.getAllYearsAndMonthInSpending())

    def listenerShow(self):
        plt.clf()

        dbO = db.database()
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
        