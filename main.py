from UI.MainW import Ui_MainWindow

from PyQt5.QtWidgets import *


class Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.but_new_order.clicked.connect(self.swTo_NewOrder)
        self.but_add_to_inventory.clicked.connect(self.swTo_EditInventory)

        self.but_return_to_start.clicked.connect(self.swTo_Start)
        self.stackedWidget.setCurrentIndex(0)

    def swTo_NewOrder (self):
        self.stackedWidget.setCurrentWidget(self.new_order)

    def swTo_Start(self):
        self.stackedWidget.setCurrentWidget(self.start)

    def swTo_EditInventory(self):
        self.stackedWidget.setCurrentWidget(self.edit_inventory)

def main():
    app = QApplication([])
    tmp = Window()
    win = QMainWindow()

    tmp.setupUi(win)
    win.show()

    app.exec_()


main()