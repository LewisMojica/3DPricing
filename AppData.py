import sqlite3
import time

class Add:
    '''Esta clase contiene funciones para agregar impresora, filamentor e impresiones a la base de datos'''

    def __init__(self, database_name='database.sqlite3'):
        global con_db
        con_db = sqlite3.connect(database_name)


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
            for iter in sql_script:
                print(iter)
                con_db.execute(iter)
            return 0
        elif tables_count == 9:
            return 2
        else:
            return 1

    def getCursor(self):
        return con_db.execute('PRAGMA foreign_keys = ON;')


    def printer(self, name, depracation):
        '''agrega nueva impresora a base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute('INSERT INTO printers (name, depracation) VALUES ("{}",{})'.format(name,str(depracation)))
        con_db.commit()
        cursor_db.close()

    def material(self, name):
        '''agrega nuevo material a base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute('INSERT INTO materials (name) VALUES ("{}")'.format(name))
        con_db.commit()
        cursor_db.close()

    def filament(self, name, material, total_cost, length, actual_length='NULL'):
        '''agrega nuevo filamento a base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute('INSERT INTO filaments (name, material_name, total_cost, length, actual_length)\
             VALUES("{}","{}",{},{},{})'.format(name,material,total_cost,length,actual_length))
        con_db.commit()
        cursor_db.close()

    def customer(self, name, last_name, phone_number='NULL'):
        '''agrega nuevo cliente a base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute('INSERT INTO customers (name, last_name, phone_number) VALUES("{}","{}",{})'\
            .format(name,last_name,phone_number))
        con_db.commit()
        cursor_db.close()

    def material_consumption(self, material_name, printer_id, consumption):
        '''agrega información de consumo sobre material en cierta impresora a base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute('INSERT INTO materials_consumptions (material_name, printer_id, consumption) VALUES("{}",{},{})'\
            .format(material_name,printer_id,consumption))
        con_db.commit()
        cursor_db.close()

    def order(self, customer_id, printer_id, net_cost, customer_cost, description='NULL'):
        '''agrega nueva orden a base de datos y retorna el id de la orden creada'''
        cursor_db = self.getCursor()
        cursor_db.execute('INSERT INTO orders (customer_id, printer_id, net_cost, customer_cost, description, unix_time) VALUES({},{},{},{},"{}",{})'\
            .format(customer_id, printer_id, net_cost, customer_cost, description, int(time.time())))
        
        order_id = tuple(cursor_db.execute('SELECT last_insert_rowid()'))[0][0]
        con_db.commit()
        cursor_db.close()
        return order_id

    def filament_order(self, filament_id,order_id,length,printing_time):
        '''agrega consumo de filamente a orden en base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute('INSERT INTO filament_order (filament_id,order_id,length,printing_time) VALUES({},{},{},{})'\
            .format(filament_id,order_id,length,printing_time))
        con_db.commit()
        cursor_db.close()

    def human_labor(self, order_id, slicing,print_removal=0, support_removal=0, filament_change=0, tool_change=0):
        '''agrega horas de trabajo (humano) de una cierta orden a la base de datos'''
        cursor_db = self.getCursor()
        cursor_db.execute('INSERT INTO human_time (order_id, slicing,print_removal, support_removal, \
                        filament_change, tool_change) VALUES({},{},{},{},{},{})'.format(order_id, slicing,print_removal,\
                                                                    support_removal,filament_change, tool_change))
        con_db.commit()
        cursor_db.close()

    def getMaterialsName(self):
        '''retorna un tuple con los nombres de los materiales creados'''
        cursor_db = self.getCursor()
        result = ()
        for iter in cursor_db.execute('SELECT name FROM materials'):
            result += iter
        cursor_db.close()
        return result

    def getPrintersName(self):
        '''retorna un tuple con los nombres de los impresoras existentes'''
        cursor_db = self.getCursor()
        result = ()
        for iter in cursor_db.execute('SELECT name FROM printers'):
            result += iter
        cursor_db.close()
        return result[1:]

    def getCustomersName(self):
        '''retorna un tuple con los nombres de los clientes existentes'''
        cursor_db = self.getCursor()
        result = ()
        for iter in cursor_db.execute('SELECT name FROM customers'):
            result += iter
        cursor_db.close()
        return result

    def getFilamentsID(self,material='*'):
        '''retorna un tuple con los nombres de los clientes existentes'''
        cursor_db = self.getCursor()
        result = ()
        for iter in cursor_db.execute('SELECT id FROM filaments WHERE material_name="{}"'.format(material)):
            result += iter
        cursor_db.close()
        return result

    def getFilamentsName(self,ids):
        '''retorna un tuple con los nombres los carretes que correspondes a los IDs especificados'''
        cursor_db = self.getCursor()
        if type(ids) == int:
            ids = (ids,ids)

        if ids == ():
            return ()
        result = ()
        command = 'SELECT name FROM filaments WHERE'
        for iter in ids:
            command += 'OR id={} '.format(iter)

        for iter in cursor_db.execute(command.replace('OR','',1)):
            result += iter
        cursor_db.close()
        return result

    def getPrinterDepracation(self,id):
        '''retorna el consumo de la impresora especificada'''
        cursor_db = self.getCursor()
        result = 0
        for iter in cursor_db.execute('SELECT depracation FROM printers WHERE id="{}"'.format(id)):
            result = iter
        cursor_db.close()
        result = result[0]
        return result
    
    def getFilamentCostPerGram (self,id):
        '''retorna el precio de cada gramo del filamento especificado'''
        cursor_db = self.getCursor()
        result = ()
        tup = ()
        for iter in cursor_db.execute('SELECT total_cost,length FROM filaments WHERE id="{}"'.format(id)):
            tup += iter
        cursor_db.close()
        result = tup[0]/tup[1]
        return result

    def getHumanTimeCost(self):
        '''retorna el costo por hora de la persona'''
        
        return self.getPrinterDepracation(1)
