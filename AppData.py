import sqlite3, json, time

class Add:
    '''Esta clase contiene funciones para agregar impresora, filamentor e impresiones a la base de datos'''

    def __init__(self):
        self.config = json.load(open('config.json'))
        self.con_db = sqlite3.connect(self.config['path_to_data_base'])
        self.createTables()


    def getCreateScript(self):
        ''' retorna los los comandos a ejecutar para crear las tablas'''
        with open('createTables.sqlite.sql', 'r') as file:
            data = file.read().split(';')
        return data

    def createTables(self):
        '''Esta función crea la base de datos y las tablas.
        Retorna un 0 si se crean las tablas.
        Retorna 1 si previamente existían tablas pero hay no hay 8 tablas
        Retorna 2 previamente existían existen 8 tablas creadas'''
        sql_script = self.getCreateScript()
        cursor = self.getCursor()
        tables_list = list(cursor.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name'))
        tables_count = len(tables_list)

        if tables_count == 0:
            for _iter in sql_script:
                print(_iter)
                self.con_db.execute(_iter)
            return 0
        elif tables_count == 9:
            return 2
        else:
            return 1

    def getCursor(self):
        return self.con_db.execute('PRAGMA foreign_keys = ON;')

    def getRecords(self, table, columns, where=None):
        cur = self.getCursor()

        if where == None:
            cur.execute(f'SELECT {columns} FROM {table}')
        else:
            cur.execute(f'SELECT {columns} FROM {table} WHERE {where}')

        result = cur.fetchall()
        cur.close()
        return result

    def getConfig (self):
        '''retorna el dict generado apartir de config.json'''
        return self.config

    def changeConfig(self, new_config):
        with open('config.json','w') as config_file:
            json.dump(new_config, config_file, indent=4, sort_keys=True)

    def updateRecords(self,table,values,where):
        cur = self.getCursor()
        a = f'UPDATE {table} SET {values} WHERE {where}'
        print(a)
        cur.execute(a)
        self.con_db.commit()

    def deleteRecords(self,table,where):
        self.updateRecords(table, 'deleted=1', f'{where}')


    def insertPrinter(self, name, deprecation, electric_consumption):
        '''agrega nueva impresora a base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute(f'INSERT INTO printers (name, deprecation, default_electric_consumption) VALUES ("{name}",{deprecation},{electric_consumption})')

        self.con_db.commit()
        cursor_db.close()

    def insertMaterial(self, name):
        '''agrega nuevo material a base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute(f'INSERT INTO materials (name) VALUES ("{name}")')
        self.con_db.commit()
        cursor_db.close()

    def insertFilament(self, name, material, total_cost, length):
        '''agrega nuevo filamento a base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute(f'INSERT INTO filaments (name, material_name, total_cost, length)\
             VALUES("{name}","{material}",{total_cost},{length})')
        self.con_db.commit()
        cursor_db.close()

    def insertCustomer(self, name, last_name, phone_number='NULL'):
        '''agrega nuevo cliente a base de datos'''
        if phone_number == '':
            phone_number = 'NULL'
        cursor_db = self.getCursor()
        cursor_db.execute(f'INSERT INTO customers (name, last_name, phone_number) VALUES("{name}","{last_name}","{phone_number}")')
        self.con_db.commit()
        cursor_db.close()

    def insertMaterial_consumption(self, material_name, printer_id, consumption):
        '''agrega información de consumo sobre material en cierta impresora a base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute(f'INSERT INTO materials_consumptions (material_name, printer_id, consumption) VALUES("{material_name}",{printer_id},{consumption})')
        self.con_db.commit()
        cursor_db.close()

    def insertOrder(self, customer_id, net_cost, customer_cost, description='NULL'):
        '''agrega nueva orden a base de datos y retorna el id de la orden creada'''
        cursor_db = self.getCursor()
        cursor_db.execute(f'INSERT INTO orders (customer_id, net_cost, customer_cost, description, unix_time)\
             VALUES({customer_id},{net_cost},{customer_cost},"{description}",{int(time.time())})')
        
        order_id = tuple(cursor_db.execute('SELECT last_insert_rowid()'))[0][0]
        self.con_db.commit()
        cursor_db.close()
        return order_id

    def insertFilament_order(self, filament_id,order_id,length,printing_time,printer_id, electricity_cost):
        '''agrega consumo de filamente a orden en base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute(f'INSERT INTO filament_order (filament_id,order_id,length,printing_time,printer_id, electricity_cost) \
            VALUES({filament_id},{order_id},{length},{printing_time},{printer_id}, {electricity_cost})')
        self.con_db.commit()
        cursor_db.close()

    def insertHuman_labor(self, order_id, slicing,print_removal=0, support_removal=0,set_up_printer=0):
        '''agrega horas de trabajo (humano) de una cierta orden a la base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute(f'INSERT INTO human_time (order_id, slicing,print_removal, support_removal, \
            set_up_printer) VALUES({order_id},{slicing},{print_removal},{support_removal},{set_up_printer})')
        self.con_db.commit()
        cursor_db.close()


    def getMaterials(self, columns = '*', where = None):
        '''retorna una lista de las columnas especificadas de todos los records de la tabla materials'''
        return self.getRecords('materials', columns, where)

    def getPrinters(self, columns = '*', where = None, show_deleted=False):
        '''retorna un tuple con los nombres de los impresoras existentes'''
        if where == None:
            return self.getRecords('printers', columns,f'deleted={int(show_deleted)}')
        else:
            return self.getRecords('printers', columns, where + f' AND deleted={int(show_deleted)}')

    def getCustomers(self, columns = '*', where = None, show_deleted = False):
        '''retorna un tuple con los nombres de los clientes existentes'''
        if where == None:
            return self.getRecords('customers', columns, f'deleted={int(show_deleted)}')
        else:
            return self.getRecords('customers', columns, where + f' AND deleted={int(show_deleted)}')

    def getFilaments(self, columns = '*', where = None, show_deleted = False):
        '''retorna un tuple con los nombres de los clientes existentes'''
        if where == None:
            return self.getRecords('filaments', columns, f'deleted={int(show_deleted)}')    
        else:
            return self.getRecords('filaments', columns,where + f' AND deleted={int(show_deleted)}')

    def getMaterialsConsumptions(self, columns='*', where=None):
        '''retorna una lista con los records que cumplen con la condicion dada con where, si no hay condicion
        se retornan todos los record'''
        return self.getRecords('materials_consumptions', columns,where)

    def getOrders(self,columns='*', where=None):
        '''retorna una lista con los records que cumplen con la condicion dada con where, si no hay condicion
        se retornan todos los record'''
        return self.getRecords('orders',columns,where)

    def setMaterialConsumption(self,consumption,material_name,printer_id):
        '''crea un records en la tabla materials_consumptions, si el records ya existe, entonces lo modifica'''
        if(len(self.getMaterialsConsumptions(where=f'printer_id={printer_id} AND material_name="{material_name}"')) == 0):
            self.insertMaterial_consumption(material_name,printer_id,consumption)
        else:
            self.updateRecords('materials_consumptions',f'consumption={consumption}',f'printer_id={printer_id} AND material_name="{material_name}"')
    
    def updateCustomer(self,id,name,last_name,phone_number):
        '''modifica a un record de la tabla customers'''
        self.updateRecords('customers',f'name="{name}", last_name="{last_name}", phone_number="{phone_number}"',f'id={id}')
    
    def updatePrinter(self, id, name, depreciation, consumption):
        '''modifica a un record de la tabla printers'''
        self.updateRecords('printers',f'name="{name}", deprecation={depreciation}, default_electric_consumption={consumption}',f'id={id}')
    
    def updateFilament(self, id, name, total_cost, weight):
        '''modifica a un record de la tabla printers'''
        self.updateRecords('filaments',f'name="{name}", total_cost={total_cost}, length={weight}',f'id={id}')

    def deleteCustomer(self,id):
        self.deleteRecords('customers',f'id={id}')

    def deletePrinter(self,id):
        self.deleteRecords('printers',f'id={id}')
    
    def deleteFilament(self,id):
        self.deleteRecords('filaments',f'id={id}')

if __name__ == '__main__':
    pass
    