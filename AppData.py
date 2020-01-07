import sqlite3
import time

class Add:
    '''Esta clase contiene funciones para agregar impresora, filamentor e impresiones a la base de datos'''

    def __init__(self, database_name='database.sqlite3'):
        self.con_db = sqlite3.connect(database_name)
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
            cur.execute('SELECT {} FROM {}'.format(columns,table))
        else:
            cur.execute('SELECT {} FROM {} WHERE {}'.format(columns,table,where))

        result = cur.fetchall()
        cur.close()
        return result

    def updateRecords(self,table,values,where):
        cur = self.getCursor()
        a = f'UPDATE {table} SET {values} WHERE {where}'
        print(a)
        cur.execute(a)
        self.con_db.commit()
        

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
        cursor_db = self.getCursor()
        cursor_db.execute('INSERT INTO customers (name, last_name, phone_number) VALUES("{}","{}",{})'\
            .format(name,last_name,phone_number))
        self.con_db.commit()
        cursor_db.close()

    def insertMaterial_consumption(self, material_name, printer_id, consumption):
        '''agrega información de consumo sobre material en cierta impresora a base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute('INSERT INTO materials_consumptions (material_name, printer_id, consumption) VALUES("{}",{},{})'\
            .format(material_name,printer_id,consumption))
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

    def insertFilament_order(self, filament_id,order_id,length,printing_time,printer_id):
        '''agrega consumo de filamente a orden en base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute('INSERT INTO filament_order (filament_id,order_id,length,printing_time,printer_id) VALUES({},{},{},{},{})'\
            .format(filament_id,order_id,length,printing_time,printer_id))
        self.con_db.commit()
        cursor_db.close()

    def insertHuman_labor(self, order_id, slicing,print_removal=0, support_removal=0,set_up_printer=0):
        '''agrega horas de trabajo (humano) de una cierta orden a la base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute(f'INSERT INTO human_time (order_id, slicing,print_removal, support_removal, \
            set_up_printer) VALUES({order_id},{slicing},{print_removal},{support_removal},{set_up_printer})')
        self.con_db.commit()
        cursor_db.close()


    def getMaterials(self,columns='*',where=None):
        '''retorna una lista de las columnas especificadas de todos los records de la tabla materials'''
        return self.getRecords('materials',columns,where)

    def getPrinters(self,columns='*',where=None):
        '''retorna un tuple con los nombres de los impresoras existentes'''
        return self.getRecords('printers',columns,where)

    def getCustomers(self,columns='*',where=None):
        '''retorna un tuple con los nombres de los clientes existentes'''
        return self.getRecords('customers',columns,where)

    def getFilaments(self,columns='*',where=None):
        '''retorna un tuple con los nombres de los clientes existentes'''
        return self.getRecords('filaments',columns,where)

    def getMaterialsConsumptions(self,columns='*',where=None):
        '''retorna una lista con los records que cumplen con la condicion dada con where, si no hay condicion
        se retornan todos los record'''
        return self.getRecords('materials_consumptions',columns,where)

    def setMaterialConsumption(self,consumption,material_name,printer_id):
        '''crea un records en la tabla materials_consumptions, si el records ya existe, entonces lo modifica'''
        if(len(self.getMaterialsConsumptions(where=f'printer_id={printer_id} AND material_name="{material_name}"')) == 0):
            self.insertMaterial_consumption(material_name,printer_id,consumption)
        else:
            self.updateRecords('materials_consumptions',f'consumption={consumption}',f'printer_id={printer_id} AND material_name="{material_name}"')
