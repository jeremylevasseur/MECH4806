import sys
from mpmath import *
from sympy import *
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSlot
from pprint import pprint


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'D_H Table'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 400
        self.initialList = [
            ('i', 'alpha_(i-1)', 'a_(i-1)', 'd_i', 'theta_i'),
            ('', '', '', '', ''),
            ('', '', '', '', ''),
            ('', '', '', '', ''),
            ('', '', '', '', '')
        ]

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()
        self.createButtons()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.addRowButton)
        self.layout.addWidget(self.removeRowButton)
        self.layout.addWidget(self.generateMatrices)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.initialList))
        self.tableWidget.setColumnCount(len(self.initialList[0]))
        for i in range(len(self.initialList)):
            for j in range(len(self.initialList[i])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(self.initialList[i][j]))

        self.tableWidget.move(0, 0)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    def createButtons(self):
        self.addRowButton = QPushButton('Add Row', self)
        self.addRowButton.setToolTip('Add Row')

        self.removeRowButton = QPushButton('Remove Row', self)
        self.removeRowButton.setToolTip('Remove Row')

        self.generateMatrices = QPushButton('Generate Matrices', self)
        self.generateMatrices.setToolTip('Generate Matrices')

        self.addRowButton.clicked.connect(self.on_click_add_row)
        self.removeRowButton.clicked.connect(self.on_click_remove_row)
        self.generateMatrices.clicked.connect(self.on_click_generate_matrices)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        # for currentQTableWidgetItem in self.tableWidget.selectedItems():
        #     print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    @pyqtSlot()
    def on_click_add_row(self):
        rowPosition = len(self.initialList)
        self.tableWidget.insertRow(rowPosition)
        for j in range(len(self.initialList[0])):
            self.tableWidget.setItem(rowPosition, j, QTableWidgetItem(''))

        self.initialList.append(('', '', '', '', ''))

    @pyqtSlot()
    def on_click_remove_row(self):
        rowPosition = len(self.initialList) - 1
        self.tableWidget.removeRow(rowPosition)

        del self.initialList[-1]

    @pyqtSlot()
    def on_click_generate_matrices(self):
        iVals = []
        alphaVals = []
        aVals = []
        dVals = []
        thetaVals = []

        for i in range(self.tableWidget.rowCount()):
            for j in range(len(self.initialList[0])):
                tempRow = i
                tempCol = j
                tempVal = self.tableWidget.item(i, j).text()
                if tempRow != 0:
                    if tempCol == 0:
                        iVals.append(tempVal)
                    elif tempCol == 1:
                        alphaVals.append(tempVal)
                    elif tempCol == 2:
                        aVals.append(tempVal)
                    elif tempCol == 3:
                        dVals.append(tempVal)
                    elif tempCol == 4:
                        thetaVals.append(tempVal)

        tableDataObject = {
            'iVals': iVals,
            'alphaVals': alphaVals,
            'aVals': aVals,
            'dVals': dVals,
            'thetaVals': thetaVals
        }

        # self.printTable(tableDataObject)
        self.makeCalculations(tableDataObject)

    def printTable(self, tableDataObject):

        rowCount = len(tableDataObject['iVals'])
        columnCount = len(tableDataObject)

        print("=================================================================")
        print("iVals\talphaVals\taVals\t\tdVals\t\tthetaVals\t")
        print("=================================================================")
        for i in range(rowCount):
            for j in range(columnCount):
                if j == 0:
                    print(tableDataObject['iVals'][i], end="\t\t")
                elif j == 1:
                    print(tableDataObject['alphaVals'][i], end="\t\t\t")
                elif j == 2:
                    print(tableDataObject['aVals'][i], end="\t\t\t")
                elif j == 3:
                    print(tableDataObject['dVals'][i], end="\t\t\t")
                elif j == 4:
                    print(tableDataObject['thetaVals'][i], end="\n")

        print("=================================================================")

    def makeCalculations(self, tableDataObject):

        iVals = tableDataObject['iVals']
        alphaVals = tableDataObject['alphaVals']
        aVals = tableDataObject['aVals']
        dVals = tableDataObject['dVals']
        thetaVals = tableDataObject['thetaVals']

        allMatrices = []

        for i in range(len(iVals)):
            print(str(i))
            print("\tT = ")
            print(str(i+1))
            matrix = self.calculateMatrix(alphaVals[i], aVals[i], dVals[i], thetaVals[i])
            allMatrices.append(matrix)
            pprint(matrix)
            print("\r\n\r\n")

        baseToToolMatrix = self.calculateBaseToToolMatrix(allMatrices, verbose=1)

        print("Base")
        print("\tT = ")
        print("Tool")
        pprint(baseToToolMatrix)
        print("\r\n\r\n")

    def calculateMatrix(self, alphaStr, aStr, dStr, thetaStr):
        init_printing()
        alpha, a, d, theta = symbols("alpha a d theta")
        result = Matrix([[cos(theta), -sin(theta), 0, a], [sin(theta)*cos(alpha), cos(theta)*cos(alpha), -sin(alpha), -sin(alpha)*d], [sin(theta)*sin(alpha), cos(theta)*sin(alpha), cos(alpha), cos(alpha)*d], [0, 0, 0, 1]])

        if self.isANumber(alphaStr):
            alphaNum = int(alphaStr)
            alphaNumRadians = self.wholeDegreeToWholeRadian(alphaNum)
            result = result.subs(alpha, alphaNumRadians)
        else:
            print(alphaStr)
            result = result.subs(alpha, alphaStr)

        if self.isANumber(aStr):
            result = result.subs(a, int(aStr))
        else:
            result = result.subs(a, aStr)

        if self.isANumber(dStr):
            result = result.subs(d, int(dStr))
        else:
            result = result.subs(d, dStr)

        if self.isANumber(thetaStr):
            thetaNum = int(thetaStr)
            thetaNumRadians = self.wholeDegreeToWholeRadian(thetaNum)
            result = result.subs(theta, thetaNumRadians)
        else:
            result = result.subs(theta, thetaStr)

        return result

    def calculateBaseToToolMatrix(self, allMatrices, verbose):
        matrixSum = None
        calculationString = "{Base}_{Tool}T = "

        if verbose == 1:
            print("Calculating Base To Tool Matrix")
            print("======================================================")

        if len(allMatrices) < 1:
            return matrixSum
        elif len(allMatrices) < 2:
            return allMatrices[0]
        else:
            matrixSum = allMatrices[0] * allMatrices[1]
            calculationString = calculationString + "{0}_{1}T * {1}_{2}T"
            print("\r\n\r\n-------------\r\n{0}_{2}T = {0}_{1}T * {1}_{2}T = ")
            pprint(matrixSum)
            for i in range(2, len(allMatrices)):
                matrixSum = matrixSum * allMatrices[i]
                calculationString = calculationString + " * {" + str(i) + "}_{" + str(i + 1) + "}T"
                print("\r\n\r\n-------------\r\n{0}_{" + str(i + 1) + "}T = {0}_{" + str(i) + "}T * {" + str(i) + "}_{" + str(i + 1) + "}T = ")
                pprint(matrixSum)

        if verbose == 1:
            print("======================================================")
            print("Final Expression: " + calculationString + "\r\n\r\n")

        return matrixSum

    def isANumber(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def wholeDegreeToWholeRadian(self, wholeDegree):
        wholeRadian = 0
        if wholeDegree == -360:
            wholeRadian = -2*pi
        elif wholeDegree == -270:
            wholeRadian = (-3*pi)/2
        elif wholeDegree == -180:
            wholeRadian = -pi
        elif wholeDegree == -90:
            wholeRadian = -1*pi/2
        elif wholeDegree == 90:
            wholeRadian = pi / 2
        elif wholeDegree == 180:
            wholeRadian = pi
        elif wholeDegree == 270:
            wholeRadian = (3*pi)/2
        elif wholeDegree == 360:
            wholeRadian = 2*pi

        return wholeRadian


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

