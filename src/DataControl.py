import json
import datetime

print_job = {}
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
            [hh,mm] = input("*Tiempo de trabajo (humano) (format: hh:mm) > ").split(':')
            print_job["human time"] = int(hh) + int(mm)/60
        except ValueError:
            print("Formato incorrecto, ¿olvidaste poner :?")
            nextData()
    nextData()

    def nextData():
        try:
            print_job["filament lenght"] = float(input("Ingrese los metros de filamento > "))
        except ValueError:
            print("Formato incorrecto. Solo números")
            nextData()
    nextData()


    def nextData():
        try:
            inn = input("Ingrese el material > ").lower()
            if len(pam["materials"][inn]) == 1:
                print_job["material"] = pam["materials"][inn][0]
            else:
                def getMat():
                    try:
                        print('Listas de carretes de', inn, ':')
                        for iter in pam["materials"][inn]:
                            print('->', iter['name'])
                        carrete = input('Espefique el carrete > ')

                        print_job["material"] = next(item for item in pam['materials'][inn] if item['name'].lower() == carrete.lower())
                    except StopIteration:
                        print("Carrete <", carrete, "> no existente")
                        getMat()
                getMat()

        except KeyError:
            print("Material inexistente")
            nextData()
    nextData()

    calculatePrice()

def calculatePrice():
    global print_job
    print_job["pricing"] = {}
    try:
        print_job['pricing']['electricity cost'] = print_job["material"]["printers consumptions"][print_job["printer"]["name"]]*print_job["printing time"]
    except KeyError:
        print_job['pricing']['electricity cost'] = print_job["printer"]["default consumption"]*print_job["printing time"]


    print_job['pricing']['profit margin'] = 1 
    print_job['pricing']['human labor'] = print_job['human time']*pam['human time price']
    print_job['pricing']['filament cost'] = print_job['material']['cost']*print_job['filament lenght']
    print_job['pricing']['printer operation cost'] = print_job["printer"]["operation cost"]*print_job["printing time"]
    print_job['pricing']['net cost'] = print_job['pricing']['human labor']\
        + print_job['pricing']['filament cost']\
        + print_job['pricing']['printer operation cost']\
        + print_job['pricing']['printer operation cost']\
        + print_job['pricing']['electricity cost']

    print_job['pricing']['date'] = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    print_job['pricing']['client cost'] = (print_job["pricing"]['profit margin'] + 1)*print_job['pricing']['net cost']

    print()
    print()
    print()
    for iter in print_job['pricing']:
        print()
        print(iter,':', print_job['pricing'][iter])