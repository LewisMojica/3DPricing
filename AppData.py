import sqlite3
import time

con_db = sqlite3.connect('database.sqlite3')


def getCreateScript():
    ''' retorna los los comandos a ejecutar para crear las tablas'''
    with open('createTables.sqlite.sql', 'r') as file:
        data = file.read().split(';')
    return data

def createTables():
    '''Esta función crea la base de datos y las tablas.'''
    sql_script = getCreateScript()
    try:
        for iter in sql_script:
            con_db.execute(iter)
        print('tabla creada')
    except sqlite3.OperationalError:
        print('tabla ya existe')
def getCursor():
    return con_db.execute('PRAGMA foreign_keys = ON;')


class Add:
    '''Esta clase contiene funciones para agregar impresora, filamentor e impresiones a la base de datos'''
    def printer(name, depracation):
        '''agrega nueva impresora a base de datos'''
        cursor_db = getCursor()
        cursor_db.execute('INSERT INTO printers (name, depracation) VALUES ("{}",{})'.format(name,str(depracation)))
        con_db.commit()
        cursor_db.close()

    def material(name):
        '''agrega nuevo material a base de datos'''
        cursor_db = getCursor()
        cursor_db.execute('INSERT INTO materials (name) VALUES ("{}")'.format(name))
        con_db.commit()
        cursor_db.close()

    def filament(name, material, total_cost, length, actual_length='NULL'):
        '''agrega nuevo filamento a base de datos'''
        cursor_db = getCursor()
        cursor_db.execute('INSERT INTO filaments (name, material_name, total_cost, length, actual_length)\
             VALUES("{}","{}",{},{},{})'.format(name,material,total_cost,length,actual_length))
        con_db.commit()
        cursor_db.close()

    def customer(name, last_name, phone_number='NULL'):
        '''agrega nuevo cliente a base de datos'''
        cursor_db = getCursor()
        cursor_db.execute('INSERT INTO customers (name, last_name, phone_number) VALUES("{}","{}",{})'\
            .format(name,last_name,phone_number))
        con_db.commit()
        cursor_db.close()

    def material_consumption(material_name, printer_id, consumption):
        '''agrega información de consumo sobre material en cierta impresora a base de datos'''
        cursor_db = getCursor()
        cursor_db.execute('INSERT INTO materials_consumptions (material_name, printer_id, consumption) VALUES("{}",{},{})'\
            .format(material_name,printer_id,consumption))
        con_db.commit()
        cursor_db.close()

    def order(customer_id, printer_id, net_cost, customer_cost, description='NULL'):
        '''agrega nueva orden a base de datos'''
        cursor_db = getCursor()
        cursor_db.execute('INSERT INTO orders (customer_id, printer_id, net_cost, customer_cost, description, unix_time) VALUES({},{},{},{},"{}",{})'\
            .format(customer_id, printer_id, net_cost, customer_cost, description, int(time.time())))
        con_db.commit()
        cursor_db.close()
