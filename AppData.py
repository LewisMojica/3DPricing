import sqlite3
import time

con_db = sqlite3.connect('database.sqlite3')


def getCreateScript():
    ''' retorna los los comandos a ejecutar para crear las tablas'''
    with open('createTables.sqlite.sql', 'r') as file:
        data = file.read().split(';')
    return data

def createTables():
    '''Esta función crea la base de datos y las tablas.
    Retorna un 0 si se crean las tablas.
    Retorna 1 si previamente existían tablas pero hay no hay 8 tablas
    Retorna 2 previamente existían existen 8 tablas creadas'''
    sql_script = getCreateScript()
    cursor = getCursor()
    tables_list = list(cursor.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name'))
    tables_count = len(tables_list)

    if tables_count == 0:
        for iter in sql_script:
            con_db.execute(iter)
#            print(iter)
        return 0
    elif tables_count == 9:
        return 2
    else:
        return 1

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

    def filament_order(filament_id,order_id,length):
        '''agrega consumo de filamente a orden en base de datos'''
        cursor_db = getCursor()
        cursor_db.execute('INSERT INTO filament_order (filament_id,order_id,length) VALUES({},{},{})'\
            .format(filament_id,order_id,length))
        con_db.commit()
        cursor_db.close()

    def human_labor(order_id, slicing,print_removal=0, support_removal=0, filament_change=0, tool_change=0):
        '''agrega horas de trabajo (humano) de una cierta orden a la base de datos'''
        cursor_db = getCursor()
        cursor_db.execute('INSERT INTO human_time (order_id, slicing,print_removal, support_removal, \
                        filament_change, tool_change) VALUES({},{},{},{},{},{})'.format(order_id, slicing,print_removal,\
                                                                    support_removal,filament_change, tool_change))
        con_db.commit()
        cursor_db.close()
