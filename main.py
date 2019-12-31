from UI.MainW import Ui_MainWindow

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QAbstractItemModel

import AppData

class Window(Ui_MainWindow):    
    def setupUi(self, MainWindow):
        self.data = AppData.Add()
        super().setupUi(MainWindow)
        self.but_new_order.clicked.connect(self.swTo_NewOrder)

        self.listWidget_SelectNewItem.currentRowChanged.connect(self.select_add)

        self.but_return_to_start.clicked.connect(self.swTo_Start)
        self.but_return_to_start_2.clicked.connect(self.swTo_Start)

        self.but_add.clicked.connect(self.addItem)

        self.but_add_item.clicked.connect(self.swTo_AddItem)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        

        self.materialComboBox_3.insertItems(0,self.data.getMaterialsName())

        self.items_to_add = ('Impresora','Carrete','Cliente')

        self.listWidget_SelectNewItem.insertItems(0,self.items_to_add)



    def select_add(self, i):
        self.stackedWidget_2.setCurrentIndex(i + 1)

    def swTo_NewOrder (self):
        self.stackedWidget.setCurrentWidget(self.new_order)

    def swTo_Start(self):
        self.stackedWidget.setCurrentWidget(self.start)

    def swTo_EditInventory(self):
        self.stackedWidget.setCurrentWidget(self.edit_inventory)

    def swTo_AddItem(self):
        self.stackedWidget.setCurrentWidget(self.edit_inventory)

    def addItem(self):
        current_item = self.items_to_add[self.listWidget_SelectNewItem.currentRow()]
        if current_item == 'Carrete':
            material = self.materialComboBox_3.currentText()
            name = self.nameLineEdit_2.text().strip()
            cost = self.costoDelCarreteSpinBox.value()
            grams = self.spinBox_2.value()
            actual_grams = self.spinBox_3.value()
            if len(name.replace(' ','')) > 0:
                self.data.filament(name,material,cost,grams,actual_grams)
        elif current_item == 'Impresora':
            name = self.nameLineEdit.text().strip()
            consumption = self.spinBox.value()
            if len(name.replace(' ','')) > 0:
                self.data.printer(name,consumption)

def main():
    app = QApplication([])
    tmp = Window()
    win = QMainWindow()

    tmp.setupUi(win)
    win.show()

    app.exec_()


main()