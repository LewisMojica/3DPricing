import json

print_job = {}
pricing = {}
pam = None

def updatePam():
    global pam
    with open('appdata/pam.json','r') as file_pam:
        pam = json.load(file_pam)

def getPrintData():
    def nextData():
        try:
            inn = input("*Ingrese nombre de la impresora > ").lower()
            print_job["printer"] = pam["printers"][inn]
        except KeyError:
            print("La impresora <", inn, "> no existe, ingrese una impresora válida")
            nextData()

    nextData()
            
    print_job["description"] = input("Ingrese descripción de impresión > ")

    def nextData():
        try:
            [hh,mm] = input("*Tiempo de impresión (format: hh:mm) > ").split(':')
            print_job["printing time"] = int(hh) + int(mm)/60
        except ValueError:
            print("Formato incorrecto, ¿olvidaste poner :?")
            nextData()

    nextData()

    def nextData():
        try:
            [hh,mm] = input("*Tiempo de trabjo (humano) (format: hh:mm) > ").split(':')
            print_job["human time"] = int(hh) + int(mm)/60
        except ValueError:
            print("Formato incorrecto, ¿olvidaste poner :?")
            nextData()
        
    nextData()

    def nextData():
        try:
            print_job["material lenght"] = float(input("Ingrese los metros de filamento > "))
        except ValueError:
            print("Formato incorrecto. Solo números")
            nextData()

    nextData()


    def nextData():
        try:
            inn = input("Ingrese el material > ").upper()
            print_job["material"] = pam["materials"][inn][0]
        except KeyError:
            print("Material inexistente")
            nextData()

    nextData()

    print(print_job)

def calculatePrice(material,printer,job):
    pass

    

