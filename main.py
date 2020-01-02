from UI.MainW import Ui_MainWindow

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QAbstractItemModel

import AppData

class Window(Ui_MainWindow):    
    def setupUi(self, MainWindow):
        self.data = AppData.Add()
        super().setupUi(MainWindow)

        self.add_item_text_fields = (self.nameLineEdit_3,self.lastNameLineEdit,self.phoneNumberLineEdit,\
            self.nameLineEdit,self.spinBox,\
                self.nameLineEdit_2,self.materialComboBox_3,self.costoDelCarreteSpinBox,self.spinBox_2,self.spinBox_3,\
                    self.materialComboBox_3,self.prippComboBox,self.materialComboBox,self.customers_comboBox)

        self.last_order = None
        self.connect_all()

        self.items_to_add = ('Impresora','Carrete','Cliente')

        self.listWidget_SelectNewItem.insertItems(0,self.items_to_add)

        self.refreshUI()

    def connect_all(self):
        '''conecta todas las signals con sus slots'''
        self.but_new_order.clicked.connect(self.swTo_NewOrder)

        self.listWidget_SelectNewItem.currentRowChanged.connect(self.select_add)

        self.but_return_to_start.clicked.connect(self.swTo_Start)
        self.but_return_to_start_2.clicked.connect(self.swTo_Start)

        self.but_add.clicked.connect(self.addItem)
        self.pushButton_2.clicked.connect(self.createWholeOrder)
        self.but_add_item.clicked.connect(self.swTo_AddItem)
        
        self.materialComboBox.currentTextChanged.connect(self.updateFilaments)

        self.spinBox_7.valueChanged.connect(self.updateClientCost)
        self.spinBox_8.valueChanged.connect(self.updateNetProfitMargin)
    
        self.prippComboBox.currentIndexChanged.connect(self.updateFabricationCost)
        self.filament_comboBox.currentIndexChanged.connect(self.updateFabricationCost)
        self.customers_comboBox.currentIndexChanged.connect(self.updateFabricationCost)
        self.spinBox_5.valueChanged.connect(self.updateFabricationCost)
        self.spinBox_4.valueChanged.connect(self.updateFabricationCost)
        self.spinBox_6.valueChanged.connect(self.updateFabricationCost)
        self.slicing_time_SpinBox.valueChanged.connect(self.updateFabricationCost)
        self.iniciarImpresiNSpinBox.valueChanged.connect(self.updateFabricationCost)
        self.cambioDeFilamentoYHerramientasSpinBox.valueChanged.connect(self.updateFabricationCost)
        self.removerImpresiNSpinBox.valueChanged.connect(self.updateFabricationCost)
        self.spinBox_9.valueChanged.connect(self.updateFabricationCost)
        

    def refreshUI(self, index=0):

        for iter in self.add_item_text_fields:
            iter.clear()
        
        self.materialComboBox_3.insertItems(0,self.data.getMaterialsName())
        self.prippComboBox.insertItems(0,self.data.getPrintersName())
        self.materialComboBox.insertItems(0,self.data.getMaterialsName())
        self.customers_comboBox.insertItems(0,self.data.getCustomersName())
        self.updateFilaments()
        self.stackedWidget.setCurrentIndex(index)

    def refresh_CreateOrderUI(self):
        items_to_clear = {'spinBox':(self.spinBox_4,self.spinBox_5,self.spinBox_6,self.slicing_time_SpinBox,\
            self.iniciarImpresiNSpinBox,self.cambioDeFilamentoYHerramientasSpinBox,\
                self.removerImpresiNSpinBox,self.spinBox_9),'textEdit':(self.textEdit)}
        

        for iter in items_to_clear['spinBox']:
            iter.setValue(0)

        try:
            for iter in items_to_clear['textEdit']:
                iter.clear()
        except:
            items_to_clear['textEdit'].clear()

        self.customers_comboBox.setCurrentIndex(0)
        

    def updateFilaments(self,i=0,e=0):
        self.filament_comboBox.clear()

        ids = self.data.getFilamentsID(self.materialComboBox.currentText())
        self.filament_comboBox.insertItems(0,self.data.getFilamentsName(ids))


        
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
                self.refreshUI(self.stackedWidget.currentIndex())
        elif current_item == 'Impresora':
            name = self.nameLineEdit.text().strip()
            consumption = self.spinBox.value()
            if len(name.replace(' ','')) > 0:
                self.data.printer(name,consumption)
                self.refreshUI(self.stackedWidget.currentIndex())
        elif current_item == 'Cliente':
            name = self.nameLineEdit_3.text().strip()
            last_name = self.lastNameLineEdit.text().strip().lower()
            phone_number = self.phoneNumberLineEdit.text().replace(' ', '').replace('-','')
            self.data.customer(name, last_name, phone_number)
            self.refreshUI(self.stackedWidget.currentIndex())

    def updateFabricationCost(self,*args):
        human_time = (self.slicing_time_SpinBox.value() + self.iniciarImpresiNSpinBox.value() +\
            self.cambioDeFilamentoYHerramientasSpinBox.value() + self.slicing_time_SpinBox.value() +\
            self.spinBox_9.value())/60 + self.removerImpresiNSpinBox.value()/60
        printing_time = self.spinBox_5.value() + self.spinBox_4.value()/60
        grams_of_material = self.spinBox_6.value()
        printer_depracation = self.data.getPrinterDepracation(self.prippComboBox.currentIndex()+2)
        cost_per_gram = 0
        fabrication_cost = 0
        try:
            cost_per_gram = self.data.getFilamentCostPerGram(dict(zip(self.data.getFilamentsName(self.data.getFilamentsID(self.materialComboBox.currentText())),self.data.getFilamentsID(self.materialComboBox.currentText())))[self.filament_comboBox.currentText()])
        except:
            pass
        fabrication_cost = (human_time)*(self.data.getHumanTimeCost()) + printing_time*printer_depracation + grams_of_material*cost_per_gram
        self.frabricationCost_label_7.setText('$ {}'.format(round(fabrication_cost,2)))
        self.updateClientCost()

    def getOrderInfo(self):
        customer_id = self.customers_comboBox.currentIndex()+1
        printer_id = self.prippComboBox.currentIndex()+2
        net_cost = float(self.frabricationCost_label_7.text().replace('$',''))
        customer_cost = self.spinBox_8.value()
        description = self.textEdit.toPlainText()
        return (customer_id,printer_id,net_cost,customer_cost,description)
    
    def getHumanLaborInfo(self):
        slicing_time = self.slicing_time_SpinBox.value()/60
        print_removal_time = self.slicing_time_SpinBox.value()/60
        support_removal_time = self.slicing_time_SpinBox.value()/60
        tool_change_time = self.slicing_time_SpinBox.value()/60
        return (self.last_order,slicing_time,print_removal_time,support_removal_time,tool_change_time)
    
    def createOrder(self):
        self.last_order = self.data.order(*self.getOrderInfo())
    def createHumanTime(self):
        if self.last_order != None:
            self.data.human_labor(*self.getHumanLaborInfo())
    def createFilamentConsumption(self):
        if self.last_order != None:
            filament_id = dict(zip(self.data.getFilamentsName(self.data.getFilamentsID(self.materialComboBox.currentText())),self.data.getFilamentsID(self.materialComboBox.currentText())))[self.filament_comboBox.currentText()]
            grams_of_material = self.spinBox_6.value()
            printing_time = self.spinBox_5.value() + self.spinBox_4.value()/60
            self.data.filament_order(filament_id,self.last_order,grams_of_material,printing_time)
    def createWholeOrder(self):
        self.createOrder()
        self.createHumanTime()
        self.createFilamentConsumption()
        self.refresh_CreateOrderUI()


    def updateClientCost(self):
        self.spinBox_8.blockSignals(True)
        fabrication_cost = float(self.frabricationCost_label_7.text().replace('$',''))
        self.spinBox_8.setValue(fabrication_cost*self.spinBox_7.value()/100 + fabrication_cost)
        self.spinBox_8.blockSignals(False)
        self.getOrderInfo()

    def updateNetProfitMargin(self,i=None,e=None):
        self.spinBox_7.blockSignals(True)
        fabrication_cost = float(self.frabricationCost_label_7.text().replace('$',''))

        if(fabrication_cost != 0):
            net_profit = (self.spinBox_8.value()/fabrication_cost -1)*100
            self.spinBox_7.setValue(net_profit)
        self.spinBox_7.blockSignals(False)




def main():
    app = QApplication([])
    tmp = Window()
    win = QMainWindow()

    tmp.setupUi(win)
    win.show()

    app.exec_()


main()