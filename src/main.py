import json

print_job = {}
pricing = {}

def updatePam():
    with open('appdata/pam.json','r') as file_pam:
        return json.load(file_pam)

def getPrintData():
    def getPrinterName():
        try:
            printer_name = input("Ingrese nombre de la impresora > ").lower()
            print_job["printer"] = pam["printers"][printer_name]
        except KeyError:
            print("La impresora <", printer_name, "> no existe, ingrese una impresora válida")
            getPrinterName()

    getPrinterName()
            
        
    print_job["description"] = input("Ingrese descripción del trabajo > ")


    [hh,mm] = input("*Tiempo de impresión (format: hh:mm) > ").split(':')
    print_job["printing time"] = int(hh) + int(mm)/60

    [hh,mm] = input("*Tiempo de incio de impresión, quitar soportes, etc (format: hh:mm) > ").split(':')
    print_job["human time"] = int(hh) + int(mm)/60

    print_job["material lenght"] = float(input("Ingrese el los metros de filamento > "))

    material = input("Ingrese el material > ").upper()
    print_job["material"] = pam["materials"][material][0]
    print(print_job)

def calculatePrice(material,printer,job):
    pass

    

pam = updatePam()
getPrintData()
