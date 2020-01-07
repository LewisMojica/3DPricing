from UI.MainW import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow

import AppData

class Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.data = AppData.Add()

        #CreateOrderUI
        '''impresoras en el combobox'''
        self.current_printers_CreateOrderUI = ()
        '''carretes en el combobox'''
        self.current_filaments_CreateOrderUI = ()
        '''clientes en el combobox'''
        self.current_customers_CreateOrderUI = ()
        self.current_materials_CreateOrderUI = ()

        #AddItemUI
        self.current_materials_AddItemsUI = ()
    
        #EditDeleteUI
        self.current_materials_EditDeleteUI = ()
        self.current_printers_EditDeleteUI = ()



        self.item_to_clear_addItem = {\
            'spinBox':(self.spinBox, self.consumoDeElectricidadSpinBox, self.costoDelCarreteSpinBox,\
                self.spinBox_2),
            'textEdit':(self.nameLineEdit, self.nameLineEdit_2, self.nameLineEdit_3, self.lastNameLineEdit, self.phoneNumberLineEdit),
            'comboBox':(self.materialComboBox_3)}

        self.items_to_clear_createOrder = {\
            'spinBox':(self.spinBox_4, self.spinBox_5, self.spinBox_6, self.slicing_time_SpinBox,\
                self.setUpPrinterSpinBox,self.removerImpresiNSpinBox, self.spinBox_9),
            'textEdit':(self.textEdit),\
            'comboBox':(self.customers_comboBox, self.materialComboBox, self.prippComboBox)}

        self.items_to_clear_editDelete ={\
            'spinBox':(self.costoDeElectricidadSpinBox),
            'textEdit':(),
            'comboBox':(self.materialComboBox_9,self.impresoraComboBox),
            }
        self.connect_all()


        self.refreshUI()
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_3.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(1)

    def connect_all(self):
        '''conecta todas las signals con sus slots'''
        self.but_new_order.clicked.connect(self.swTo_NewOrder)

        self.listWidget_SelectNewItem.currentRowChanged.connect(self.select_add)
        self.listWidget.currentRowChanged.connect(self.select_edit)

        self.listWidget.currentRowChanged.connect(self.refresh_EditDeleteUI)

        self.but_return_to_start.clicked.connect(self.swTo_Start)
        self.but_return_to_start_2.clicked.connect(self.swTo_Start)
        self.pushButton_3.clicked.connect(self.swTo_Start)
        self.but_add_item.clicked.connect(self.swTo_AddItem)
        self.pushButton_4.clicked.connect(self.swTo_AddEdit_delete)

        self.pushButton.clicked.connect(self.createMaterialConsumption_EditDeleteUI)

        self.but_add.clicked.connect(self.addItem)
        self.pushButton_2.clicked.connect(self.createWholeOrder)
        
        self.materialComboBox.currentIndexChanged.connect(self.update_CreateOrderUI_Filaments)


        self.materialComboBox_9.currentIndexChanged.connect(self.refresh_EditDeleteUI)
        self.impresoraComboBox.currentIndexChanged.connect(self.refresh_EditDeleteUI)

        to_connect = (self.slicing_time_SpinBox,self.setUpPrinterSpinBox,\
            self.removerImpresiNSpinBox,self.spinBox_9,self.spinBox_5,self.spinBox_4,self.spinBox_6)
        for comboBox in to_connect:
            comboBox.valueChanged.connect(self.updateFabricationCost)      
        self.prippComboBox.currentIndexChanged.connect(self.updateFabricationCost)
        self.filament_comboBox.currentIndexChanged.connect(self.updateFabricationCost)
        self.doubleSpinBox.valueChanged.connect(self.updateClientCost)
        self.spinBox_7.valueChanged.connect(self.updateClientCost)
        self.spinBox_8.valueChanged.connect(self.updateNetProfitMargin)

    def refreshUI(self):
        self.update_AddItem()
        self.update_EditDeleteUI()
        self.textEdit.blockSignals(True)
        self.update_CreateOrderUI()
        self.textEdit.blockSignals(False)

    def update_AddItem(self):
        self.resetItems(self.item_to_clear_addItem)
        self.current_materials_AddItemsUI = self.data.getMaterials()
        self.materialComboBox_3.insertItems(0,[x[0] for x in self.current_materials_AddItemsUI])

    def update_CreateOrderUI(self):
        self.resetItems(self.items_to_clear_createOrder)
        
        self.prippComboBox.blockSignals(True)
        self.current_printers_CreateOrderUI = self.data.getPrinters()[1:]
        self.prippComboBox.insertItems(0,[x[1] for x in self.current_printers_CreateOrderUI])
        self.prippComboBox.blockSignals(False)

        self.materialComboBox.blockSignals(True)
        self.current_materials_CreateOrderUI = self.data.getMaterials()
        self.materialComboBox.insertItems(0,[x[0] for x in self.current_materials_CreateOrderUI])
        self.materialComboBox.blockSignals(False)
        self.update_CreateOrderUI_Filaments()

        self.current_customers_CreateOrderUI = self.data.getCustomers()
        self.customers_comboBox.insertItems(0,[x[1] for x in self.current_customers_CreateOrderUI])

        create_order_flag = (self.prippComboBox.count() == 0 or self.materialComboBox.count() == 0 or self.filament_comboBox.count() == 0 or\
            self.customers_comboBox.count() == 0)
        
        self.pushButton_2.setEnabled(not(create_order_flag))

        self.update_CreateOrderUI_Filaments()

    def update_CreateOrderUI_Filaments(self,i=0,e=0):
        self.filament_comboBox.clear()
        current_material = self.current_materials_CreateOrderUI[self.materialComboBox.currentIndex()][0]
        self.current_filaments_CreateOrderUI = self.data.getFilaments(where='material_name="{}"'.format(current_material))

        self.filament_comboBox.insertItems(0,[x[1] for x in self.current_filaments_CreateOrderUI])
        
        create_order_flag = (self.prippComboBox.count() == 0 or self.materialComboBox.count() == 0 or self.filament_comboBox.count() == 0 or\
            self.customers_comboBox.count() == 0)
        
        self.pushButton_2.setEnabled(not(create_order_flag))
    
    def update_EditDeleteUI(self):
        self.materialComboBox_9.blockSignals(True)
        self.impresoraComboBox.blockSignals(True)
        self.resetItems(self.items_to_clear_editDelete)
        self.current_materials_EditDeleteUI = self.data.getMaterials()
        self.materialComboBox_9.insertItems(0,[x[0] for x in self.current_materials_EditDeleteUI])
        self.current_printers_EditDeleteUI = self.data.getPrinters()[1:]
        self.impresoraComboBox.insertItems(0,[x[1] for x in self.current_printers_EditDeleteUI])
        self.materialComboBox_9.blockSignals(False)
        self.impresoraComboBox.blockSignals(False)
        self.refresh_EditDeleteUI()

    def refresh_EditDeleteUI(self,index=0):
        material_name = self.current_materials_EditDeleteUI[self.materialComboBox_9.currentIndex()][0]
        
        if(len(self.current_printers_EditDeleteUI) > 0):
            printer_id = self.current_printers_EditDeleteUI[self.impresoraComboBox.currentIndex()][0]        
            existing_records = self.data.getMaterialsConsumptions(where=f'material_name="{material_name}" AND printer_id={printer_id}')                
            if len(existing_records) == 1:
                self.costoDeElectricidadSpinBox.setValue(existing_records[0][0])
                self.cambiarCostoDeElectricidadASpinBox.setValue(existing_records[0][0])
            else:
                current_cost = 0
                for i in self.current_printers_EditDeleteUI:
                    if i[0] == printer_id:
                        current_cost = i[3]
                        break
                self.costoDeElectricidadSpinBox.setValue(current_cost)
                self.cambiarCostoDeElectricidadASpinBox.setValue(current_cost)



    def createMaterialConsumption_EditDeleteUI(self):
        material_name = self.current_materials_EditDeleteUI[self.materialComboBox_9.currentIndex()][0]
        printer_id = self.current_printers_EditDeleteUI[self.impresoraComboBox.currentIndex()][0]     

        self.data.setMaterialConsumption(self.cambiarCostoDeElectricidadASpinBox.value(),material_name,printer_id)
        self.refresh_EditDeleteUI()
    
    def resetItems(self, qobjects):
        
        try:
            for iter in qobjects['spinBox']:
                iter.setValue(0)
        except TypeError:
            qobjects['spinBox'].setValue(0)

        try:
            for iter in qobjects['textEdit']:
                iter.clear()
        except TypeError:
            qobjects['textEdit'].clear()

        try:
            for iter in qobjects['comboBox']:
                iter.clear()
        except TypeError:
            qobjects['comboBox'].clear()
        

    def addItem(self):
        currentRow = self.listWidget_SelectNewItem.currentRow()
        if currentRow==1:
            material = self.materialComboBox_3.currentText()
            name = self.nameLineEdit_2.text().strip()
            cost = self.costoDelCarreteSpinBox.value()
            grams = self.spinBox_2.value()
            if len(name.replace(' ','')) > 0:
                self.data.insertFilament(name,material,cost,grams)
                self.resetItems(self.item_to_clear_addItem)
                self.refreshUI()
        elif currentRow == 0:
            name = self.nameLineEdit.text().strip()
            consumption = self.spinBox.value()
            electric_consumption = self.consumoDeElectricidadSpinBox.value()
            if len(name.replace(' ','')) > 0:
                self.data.insertPrinter(name,consumption,electric_consumption)
                self.resetItems(self.item_to_clear_addItem)
                self.refreshUI()
        elif currentRow==2:
            name = self.nameLineEdit_3.text().strip()
            last_name = self.lastNameLineEdit.text().strip().lower()
            phone_number = self.phoneNumberLineEdit.text().replace(' ', '').replace('-','')
            self.data.insertCustomer(name, last_name, phone_number)
            self.resetItems(self.item_to_clear_addItem)
            self.refreshUI()


    def getOrderInfo(self):
        print(self.prippComboBox.currentIndex())
        customer_id = self.current_customers_CreateOrderUI[self.customers_comboBox.currentIndex()][0]

        net_cost = self.doubleSpinBox.value()
        customer_cost = self.spinBox_8.value()
        description = self.textEdit.toPlainText()
        return (customer_id,net_cost,customer_cost,description)
    
    def getHumanLaborInfo(self):
        slicing_time = self.slicing_time_SpinBox.value()/60
        print_removal_time = self.removerImpresiNSpinBox.value()/60
        support_removal_time = self.spinBox_9.value()/60
        set_up_printer_time = self.setUpPrinterSpinBox.value()/60
        return (slicing_time,print_removal_time,support_removal_time,set_up_printer_time)
    
    def getFabricationCost(self):
        human_time_cost = self.data.getPrinters('deprecation','name="human" AND id=1')[0][0]
        human_time = sum(self.getHumanLaborInfo())
        printer = self.current_printers_CreateOrderUI[self.prippComboBox.currentIndex()]
        material_name = self.current_materials_CreateOrderUI[self.materialComboBox.currentIndex()][0]
        printing_time = (self.spinBox_5.value() + self.spinBox_4.value()/60)
        filament = self.current_filaments_CreateOrderUI[self.filament_comboBox.currentIndex()]
        try:
            electricity_cost_per_hour = self.data.getMaterialsConsumptions('consumption',f'printer_id={printer[0]} AND material_name="{material_name}"')[0][0]
        except IndexError:
            electricity_cost_per_hour = printer[3]
        printer_operation_cost = printer[2]*printing_time
        material_cost_per_gram = filament[3]/filament[4]
        material_cost = material_cost_per_gram*self.spinBox_6.value()
        electricity_cost = printing_time*electricity_cost_per_hour

        return (printer_operation_cost + material_cost + electricity_cost + human_time*human_time_cost)

            
    def createWholeOrder(self):
        printer_id = self.current_printers_CreateOrderUI[self.prippComboBox.currentIndex()][0]
        filament_id = self.current_filaments_CreateOrderUI[self.filament_comboBox.currentIndex()][0]
        grams_of_material = self.spinBox_6.value()
        printing_time = self.spinBox_5.value() + self.spinBox_4.value()/60
        order_id = self.data.insertOrder(*self.getOrderInfo())

        self.data.insertHuman_labor(order_id,*self.getHumanLaborInfo())
        self.data.insertFilament_order(filament_id,order_id,grams_of_material,printing_time,printer_id)

        self.update_CreateOrderUI()


    def updateFabricationCost(self,*args):
        list_check_to_calculate_order = (self.current_printers_CreateOrderUI,self.current_filaments_CreateOrderUI,\
            self.current_customers_CreateOrderUI,self.current_materials_CreateOrderUI)
        flag = True
        for iter in list_check_to_calculate_order:
            if len(iter) == 0:
                flag = False
                break
        if flag:
            self.doubleSpinBox.setValue(self.getFabricationCost())


    def updateClientCost(self):
        self.spinBox_8.blockSignals(True)
        fabrication_cost = float(self.doubleSpinBox.value())
        self.spinBox_8.setValue(fabrication_cost*self.spinBox_7.value()/100 + fabrication_cost)
        self.spinBox_8.blockSignals(False)

    def updateNetProfitMargin(self,i=None,e=None):
        self.spinBox_7.blockSignals(True)
        fabrication_cost = self.doubleSpinBox.value()

        if(fabrication_cost != 0):
            net_profit = (self.spinBox_8.value()/fabrication_cost -1)*100
            self.spinBox_7.setValue(net_profit)
        self.spinBox_7.blockSignals(False)

        
    def select_add(self, i):
        self.stackedWidget_2.setCurrentIndex(i + 1)

    def select_edit(self, i):
        self.stackedWidget_3.setCurrentIndex(i)

    def swTo_NewOrder (self):
        self.stackedWidget.setCurrentWidget(self.new_order)

    def swTo_Start(self):
        self.stackedWidget.setCurrentWidget(self.start)

    def swTo_EditInventory(self):
        self.stackedWidget.setCurrentWidget(self.edit_inventory)

    def swTo_AddItem(self):
        self.stackedWidget.setCurrentWidget(self.edit_inventory)

    def swTo_AddEdit_delete(self):
        self.stackedWidget.setCurrentWidget(self.edit_delete)

def main():
    
    app = QApplication([])
    tmp = Window()
    win = QMainWindow()

    tmp.setupUi(win)
    win.show()

    app.exec_()


if __name__ == '__main__':
    main()