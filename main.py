from UI.MainW import Ui_MainWindow
from UI import settings, init_dialog, _3dpricing_dialog, licence_dialog, source_code_dialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QFileDialog
from PyQt5.QtGui import QIntValidator

import AppData


class Init_window(init_dialog.Ui_Form, QDialog):
    def __init__ (self, add_object, mainw, parent = None):
        super().__init__(parent)
        self.setupUi(add_object = add_object, mainw = mainw)
        print('init')

    def setupUi(self, add_object, mainw):
        super().setupUi(self)
        self.connect_all()
        self.data = add_object
        self.mainW = mainw

        self.config = self.data.getConfig()
        self.label_3.setText(self.config['path_to_data_base'])
        self.label_4.setText(self.config['path_to_files_storage'])

        
        
    def connect_all(self):
        self.pushButton.clicked.connect(self.save_config)
        self.toolButton.clicked.connect(self.select_db_path)
        self.toolButton_2.clicked.connect(self.select_order_files_path)
        self.finished.connect(self.close_dialog)

    def save_config(self):
        self.data.changeConfig(self.config)
        self.accept()

    def select_db_path(self):
        dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if dir != '':
            self.label_3.setText(dir)
            self.config['path_to_data_base'] = dir


    def select_order_files_path(self):
        dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if dir != '':
            self.label_4.setText(dir)
            self.config['path_to_files_storage'] = dir

    def close_dialog(self):
        
        config = self.data.getConfig()
        config['init'] = not(self.checkBox.isChecked())

        if self.result == 1:
            config['path_to_data_base'] = self.label_3.text()
            config['path_to_files_storage'] = self.label_4.text()
            self.mainW.refreshUI()
        
        self.data.changeConfig(config)
        self.data.setUp()



class Settings_window(settings.Ui_Form, QDialog):
    def __init__(self, add_object, mainW, parent = None):
        super().__init__(parent)
        self.setupUi(add_object, mainW)

    def setupUi(self, add_object, mainW):
        super().setupUi(self)
        self.data = add_object
        self.mainW = mainW
        self.connect_all()
        self.updateValues()

    def updateValues(self):
        config = self.data.getConfig()
        self.label_2.setText(config['path_to_data_base'])
        self.label.setText(config['path_to_files_storage'])
        self.doubleSpinBox.setValue(config['electricity_cost'])
        self.precioDeTrabajoHumanoDoubleSpinBox.setValue(config['human_time_cost'])
        

    def connect_all(self):
        self.pushButton_2.clicked.connect(self.accept)
        self.pushButton.clicked.connect(self.reject)

        self.toolButton_2.clicked.connect(self.show_file_dialog_db)
        self.toolButton.clicked.connect(self.show_file_dialog_orders_files)

        self.finished.connect(self.close_dialog)


    def save_changes(self):
        config = self.data.getConfig()
        config['electricity_cost'] = round(self.doubleSpinBox.value(), 2) 
        config['path_to_data_base'] = self.label_2.text()
        config['path_to_files_storage'] = self.label.text()
        config['human_time_cost'] = round(self.precioDeTrabajoHumanoDoubleSpinBox.value(), 2)
        self.data.changeConfig(config)
        self.data.setUp()
        self.mainW.refreshUI()
    

        

    '''dialog para buscar carpeta de la base de datos'''
    def show_file_dialog_db(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.label_2.setText(str(dir))

    def show_file_dialog_orders_files(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.label.setText(str(dir))

    def close_dialog(self):
        result = self.result()
        if  result == 1:
            self.save_changes()
        else:
            self.updateValues()

    def open(self):
        self.updateValues()
        super().open()


class Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        only_int = (self.nMeroTelefNicoLineEdit, self.phoneNumberLineEdit)
        for i in only_int:
            i.setValidator(QIntValidator())


        self.data = AppData.Add()


        #dialogs
        self._3dpricing_dialog = QDialog(MainWindow)
        _3dpricing_dialog.Ui_Dialog().setupUi(self._3dpricing_dialog)
        self.licence_dialog = QDialog(MainWindow)
        licence_dialog.Ui_Dialog().setupUi(self.licence_dialog)
        self.source_code_dialog = QDialog(MainWindow)
        source_code_dialog.Ui_Dialog().setupUi(self.source_code_dialog)
        
        self.init_dialog = Init_window(parent= MainWindow, add_object = self.data, mainw = self)
        self.settings_window = Settings_window(add_object = self.data, mainW = self, parent = MainWindow)

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
        self.current_customers_EditDeleteUI = ()
        self.current_filaments_EditDeleteUI = ()



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
            'spinBox':(self.costoDeElectricidadSpinBox, self.cambiarCostoDeElectricidadASpinBox, self.iDSpinBox_2,\
                self.spinBox_3, self.consumoElCtricoPorDefectoSpinBox, self.costoDeUsoDepreciaciNDoubleSpinBox),
            'textEdit':(self.nombreLineEdit_3, self.apellidoLineEdit, self.nMeroTelefNicoLineEdit, self.nombreLineEdit),
            'comboBox':(self.materialComboBox_9,self.impresoraComboBox, self.clienteComboBox, self.impresoraComboBox_2\
                ),
            }
        self.connect_all()


        self.refreshUI()
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_3.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(1)

    def run_init_config(self):
        if self.data.getConfig()['init'] == True:
            self.init_dialog.open()

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

        self.pushButton.clicked.connect(self.saveChanges_EditDeleteUI)

        self.but_add.clicked.connect(self.addItem)
        self.pushButton_2.clicked.connect(self.createWholeOrder)
        
        self.materialComboBox.currentIndexChanged.connect(self.update_CreateOrderUI_Filaments)

        
        self.materialComboBox_9.currentIndexChanged.connect(self.refresh_EditDeleteUI)
        self.impresoraComboBox.currentIndexChanged.connect(self.refresh_EditDeleteUI)
        self.clienteComboBox.currentIndexChanged.connect(self.refresh_EditDeleteUI)
        self.impresoraComboBox_2.currentIndexChanged.connect(self.refresh_EditDeleteUI)

        to_connect = (self.slicing_time_SpinBox,self.setUpPrinterSpinBox,\
            self.removerImpresiNSpinBox,self.spinBox_9,self.spinBox_5,self.spinBox_4,self.spinBox_6)
        for comboBox in to_connect:
            comboBox.valueChanged.connect(self.updateFabricationCost)      
        self.prippComboBox.currentIndexChanged.connect(self.updateFabricationCost)
        self.filament_comboBox.currentIndexChanged.connect(self.updateFabricationCost)
        self.doubleSpinBox.valueChanged.connect(self.updateClientCost)
        self.spinBox_7.valueChanged.connect(self.updateClientCost)
        self.spinBox_8.valueChanged.connect(self.updateNetProfitMargin)

        self.pushButton_5.clicked.connect(self.delete_EditDeleteUI)\

        self.carreteComboBox.currentIndexChanged.connect(self.refresh_EditDeleteUI)

        #menubar
        self.actionLicence.triggered.connect(self.licence_dialog.open)
        self.actionC_digo_Fuente.triggered.connect(self.source_code_dialog.open)
        self.action3DPricing.triggered.connect(self._3dpricing_dialog.open)

        self.actionImpresora_2.triggered.connect(self.show_add_printer_ui)
        self.actionCliente_2.triggered.connect(self.show_add_customer_ui)
        self.actionCarrete.triggered.connect(self.show_add_filament_ui)
        self.actionOrden.triggered.connect(self.show_new_order_ui)
        
        self.actionImpresora.triggered.connect(self.show_edit_printer_ui)
        self.actionCarretes.triggered.connect(self.show_edit_filament_ui)
        self.actionCliente.triggered.connect(self.show_edit_customer_ui)
        self.actionPreferencias.triggered.connect(self.settings_window.open)


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
        self.current_printers_CreateOrderUI = self.data.getPrinters()
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
        self.carreteComboBox

        def fillComboBox(comboBox, item_list):
            comboBox.blockSignals(True)
            comboBox.clear()
            comboBox.insertItems(0,item_list)
            comboBox.blockSignals(False)

        self.current_materials_EditDeleteUI = self.data.getMaterials()
        fillComboBox(self.materialComboBox_9,[x[0] for x in self.current_materials_EditDeleteUI])

        self.current_printers_EditDeleteUI = self.data.getPrinters()[1:]
        fillComboBox(self.impresoraComboBox_2,[x[1] for x in self.current_printers_EditDeleteUI])
        fillComboBox(self.impresoraComboBox,[x[1] for x in self.current_printers_EditDeleteUI])

        self.current_customers_EditDeleteUI = self.data.getCustomers()
        fillComboBox(self.clienteComboBox,[x[1] for x in self.current_customers_EditDeleteUI])

        self.current_filaments_EditDeleteUI = self.data.getFilaments()
        fillComboBox(self.carreteComboBox,[x[1] for x in self.current_filaments_EditDeleteUI])

        self.refresh_EditDeleteUI()

    def refresh_EditDeleteUI(self,index=0):
        if self.listWidget.currentRow() == 0:
            printer_exists = self.impresoraComboBox_2.count() != 0
            self.pushButton_5.setEnabled(printer_exists)
            self.pushButton.setEnabled(printer_exists)
            if printer_exists:
                current_printer = self.current_printers_EditDeleteUI[self.impresoraComboBox_2.currentIndex()]
                self.spinBox_3.setValue(current_printer[0])
                self.nombreLineEdit.setText(current_printer[1])
                self.consumoElCtricoPorDefectoSpinBox.setValue(current_printer[3])
                self.costoDeUsoDepreciaciNDoubleSpinBox.setValue(current_printer[2])

        elif self.listWidget.currentRow() == 1:
            self.pushButton_5.setEnabled(False)
            self.pushButton.setEnabled(self.impresoraComboBox.count() != 0)
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
        elif self.listWidget.currentRow() == 2:
            filaments_exists = self.carreteComboBox.count() != 0
            self.pushButton_5.setEnabled(filaments_exists)
            self.pushButton.setEnabled(filaments_exists)
            if filaments_exists:
                current_filament = self.current_filaments_EditDeleteUI[self.carreteComboBox.currentIndex()]
                self.iDSpinBox.setValue(current_filament[0])
                self.label_7.setText(current_filament[5])
                self.nombreLineEdit_2.setText(current_filament[1])
                self.costoTotalDoubleSpinBox.setValue(current_filament[3])
                self.gramosTotalesSpinBox.setValue(current_filament[4])

        elif self.listWidget.currentRow() == 3:
            customers_extists = self.clienteComboBox.count() != 0
            
            self.pushButton_5.setEnabled(customers_extists)
            self.pushButton.setEnabled(customers_extists)
            
            if customers_extists:
                current_customer = self.current_customers_EditDeleteUI[self.clienteComboBox.currentIndex()]
                self.iDSpinBox_2.setValue(current_customer[0])
                self.nombreLineEdit_3.setText(current_customer[1])
                self.apellidoLineEdit.setText(current_customer[2])
                self.nMeroTelefNicoLineEdit.setText(current_customer[3])
                
    
    def refresh_EditDeleteUI_customer(self):
        if len(self.current_customers_EditDeleteUI) > 0:
            customer = self.current_customers_EditDeleteUI[self.clienteComboBox.currentIndex()]
            self.iDSpinBox_2.setValue(customer[0])
            self.nombreLineEdit_3.setText(customer[1])
            self.apellidoLineEdit.setText(customer[2])
            if customer[3] == None:
                self.nMeroTelefNicoLineEdit.clear()
            else:
                self.nMeroTelefNicoLineEdit.setText(str(customer[3]))


    def saveChanges_EditDeleteUI(self):
        if self.listWidget.currentRow() == 0:
            self.data.updatePrinter(id = self.spinBox_3.value(), name = self.nombreLineEdit.text(),\
                depreciation = self.costoDeUsoDepreciaciNDoubleSpinBox.value(), consumption = self.consumoElCtricoPorDefectoSpinBox.value())
            self.refreshUI()
        elif self.listWidget.currentRow() == 1:
            material_name = self.current_materials_EditDeleteUI[self.materialComboBox_9.currentIndex()][0]
            printer_id = self.current_printers_EditDeleteUI[self.impresoraComboBox.currentIndex()][0]     

            self.data.setMaterialConsumption(self.cambiarCostoDeElectricidadASpinBox.value(),material_name,printer_id)
        elif self.listWidget.currentRow() == 2:
            self.data.updateFilament(id=self.iDSpinBox.value(),name = self.nombreLineEdit_2.text(),\
                total_cost = self.costoTotalDoubleSpinBox.value(), weight = self.gramosTotalesSpinBox.value())
            self.refreshUI()
        elif self.listWidget.currentRow() == 3:
            self.data.updateCustomer(id = self.iDSpinBox_2.value(), name = self.nombreLineEdit_3.text(),\
                last_name = self.apellidoLineEdit.text(), phone_number = self.nMeroTelefNicoLineEdit.text())
            self.refreshUI()
        self.refresh_EditDeleteUI()

    def delete_EditDeleteUI(self):
        if self.listWidget.currentRow() == 0:
            self.data.deletePrinter(self.spinBox_3.value())
            self.refreshUI()
        elif self.listWidget.currentRow() == 2:
            self.data.deleteFilament(self.iDSpinBox.value())
            self.refreshUI()
        elif self.listWidget.currentRow() == 3:
            self.data.deleteCustomer(self.iDSpinBox_2.value())
            self.refreshUI()
    
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
        human_time_cost = self.data.getConfig()['human_time_cost']
        human_time = sum(self.getHumanLaborInfo())
        printer = self.current_printers_CreateOrderUI[self.prippComboBox.currentIndex()]
        material_name = self.current_materials_CreateOrderUI[self.materialComboBox.currentIndex()][0]
        printing_time = (self.spinBox_5.value() + self.spinBox_4.value()/60)
        filament = self.current_filaments_CreateOrderUI[self.filament_comboBox.currentIndex()]
        electricity_cost_kw_per_hour = self.data.getConfig()['electricity_cost']
        try:
            electricity_consumption = self.data.getMaterialsConsumptions('consumption',f'printer_id={printer[0]} AND material_name="{material_name}"')[0][0]
        except IndexError:
            electricity_consumption = printer[3]
        printer_operation_cost = printer[2]*printing_time
        material_cost_per_gram = filament[3]/filament[4]
        material_cost = material_cost_per_gram*self.spinBox_6.value()
        electricity_cost = printing_time*electricity_consumption*electricity_cost_kw_per_hour

        return (printer_operation_cost + material_cost + electricity_cost + human_time*human_time_cost)

            
    def createWholeOrder(self):
        printer_id = self.current_printers_CreateOrderUI[self.prippComboBox.currentIndex()][0]
        filament_id = self.current_filaments_CreateOrderUI[self.filament_comboBox.currentIndex()][0]
        grams_of_material = self.spinBox_6.value()
        printing_time = self.spinBox_5.value() + self.spinBox_4.value()/60
        order_id = self.data.insertOrder(*self.getOrderInfo())

        self.data.insertHuman_labor(order_id,*self.getHumanLaborInfo())
        self.data.insertFilament_order(filament_id,order_id,grams_of_material,printing_time,printer_id, self.data.getConfig()['electricity_cost'])

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


    #menubar
    def show_new_order_ui(self):
        self.stackedWidget.setCurrentIndex(1)
    def show_add_ui(self):
        self.stackedWidget.setCurrentIndex(2)
    def show_edit_ui(self):
        self.stackedWidget.setCurrentIndex(3)
    
    def show_add_printer_ui(self):
        self.show_add_ui()
        self.listWidget_SelectNewItem.setCurrentRow(0)
    def show_add_filament_ui(self):
        self.show_add_ui()
        self.listWidget_SelectNewItem.setCurrentRow(1)
    def show_add_customer_ui(self):
        self.show_add_ui()
        self.listWidget_SelectNewItem.setCurrentRow(2)

    def show_edit_printer_ui(self):
        self.show_edit_ui()
        self.listWidget.setCurrentRow(0)
    def show_edit_material_ui(self):
        self.show_edit_ui()
        self.listWidget.setCurrentRow(1)
    def show_edit_filament_ui(self):
        self.show_edit_ui()
        self.listWidget.setCurrentRow(2)
    def show_edit_customer_ui(self):
        self.show_edit_ui()
        self.listWidget.setCurrentRow(3)

    

def main():
    
    app = QApplication([])
    tmp = Window()
    win = QMainWindow()

    tmp.setupUi(win)
    win.show()
    tmp.run_init_config()

    app.exec_()


if __name__ == '__main__':
    main()
