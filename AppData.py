import sqlite3

sql_script = None
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
        cursor_db.execute('ALTER TABLE printers_consumption_by_material ADD COLUMN ' + name.lower() + ' INTEGER')
        con_db.commit()

    def filament(name, material, length, cost):
        '''agrega nuevo filamento a base de datos'''
        cursor_db = con_db.cursor()
        cursor_db.execute('INSERT INTO filaments (name, )')
        con_db.commit()

for iter in getCreateScript():
    con_db.execute(iter)