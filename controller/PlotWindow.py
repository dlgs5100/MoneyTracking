from PyQt5 import QtWidgets, QtCore
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

        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,2,1)
        self.ax2 = self.fig.add_subplot(1,2,2)
        self.ax1.axis('off')
        self.ax2.axis('off')
        self.plotCid = 0

        self.canvasSpending = FigureCanvas(self.fig)
        #    self.canvasIncome = FigureCanvas(self.fig)
        self.VLayoutSpending.addWidget(self.canvasSpending)
        #    self.VLayoutIncome.addWidget(self.canvasIncome)

        self.buttonShow.clicked.connect(lambda: self.listenerShow(dbO))

    def updateCombox(self, dbO):
        self.comboBoxMMYYYY.setEditable(False)
        self.comboBoxMMYYYY.addItems(dbO.getAllYearsAndMonthInSpending())

    def make_picker(self, wedgesSpending, wedgesIncome):
    
        def onclick(event):
            wedge = event.artist
            label = wedge.get_label()
            print(label)

        # Make wedges selectable
        for wedge1 in wedgesSpending:
            wedge1.set_picker(True)

        for wedge2 in wedgesIncome:
            wedge2.set_picker(True)

        self.plotCid = self.canvasSpending.mpl_connect('pick_event', onclick)

    def listenerShow(self, dbO):
        self.ax1.cla()
        self.canvasSpending.mpl_disconnect(self.plotCid)

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
        wedges1, plt_labels , temp = self.ax1.pie(listCost , labels = listType, autopct='%1.1f%%')
        self.ax1.axis('equal')

        # ###

        listType = dbO.getAllTypeByMMYYYFromIncome(mmyyyy)
        listCost = []
        i = 0
        for type in listType:
            listCost.append(dbO.getAllCostByTypeFromIncome(type, mmyyyy))
            listType[i] += ' ' + str(+listCost[i])
            i+=1
    
        plt.rcParams['font.family']='DFKai-SB'
        plt.rcParams['axes.unicode_minus']=False
        wedges2, plt_labels , temp = self.ax2.pie(listCost , labels = listType, autopct='%1.1f%%')
        self.ax2.axis('equal')

        self.make_picker(wedges1, wedges2)
        self.canvasSpending.draw()
