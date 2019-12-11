import sqlite3

con_db = sqlite3.connect('database.sqlite3')

def createDB():
    '''Esta función crear la base de datos y las tablas.'''
    try:
        con_db.execute('CREATE TABLE printers(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(42), depracation INTERGER,\
                    default_consumption INTERGER NOT NULL)')

        con_db.execute('CREATE TABLE filaments(id INTERGER PRIMARY KEY, material VARCHAR(6) NOT NULL,\
                    length INTERGER NOT NULL, name VARCHAR(42) NOT NULL, cost INTEGER NOT NULL, actual_length INTEGER)')
        
        con_db.execute('CREATE TABLE printers_consumption_by_material(printer_id INTEGER PRIMARY KEY)')
        
        con_db.execute('CREATE TABLE print_history(id INTERGER PRIMARY KEY, filament INTEGER NOT NULL,\
                    net_cost INTEGER NOT NULL, client_cost INTEGER NOT NULL)')

        print('tabla creada')
    except sqlite3.OperationalError:
        print('tabla ya existe')


class Add:
    '''Esta clase contiene funciones para agregar impresora, filamentor e impresiones a la base de datos'''
    def printer(name, depracation, default_consumption):
        '''agrega nueva impresora a base de datos'''
        cursor_db = con_db.cursor()
        cursor_db.execute('INSERT INTO printers (name, depracation, default_consumption) VALUES (?,?,?)', (name, depracation, default_consumption))
        con_db.commit()
        cursor_db.close()

    def material(name):
        '''agrega nuevo material a base de datos'''
        cursor_db = con_db.cursor()
        cursor_db.execute('ALTER TABLE printers_consumption_by_material ADD COLUMN ' + name + ' INTEGER')
        con_db.commit()
