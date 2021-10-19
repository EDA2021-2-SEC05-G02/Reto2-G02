"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf
import datetime as dt
import prettytable
from prettytable import PrettyTable
import time as tm

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
# Menu de opciones

def printMenu():
    print("\nBienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Req 1: Listar cronológicamente los artistas")
    print("3- Req 2: Listar cronológicamente las adquisiciones")
    print("4- Req 3: Clasificar obras de un artista por técnica")
    print("5- Req 4: Clasificar obras por la nacionalidad de sus creadores")
    print("6- Req 5: Transportar obras de un departamento")
    print("0- Salir")
    # print("7- Req 6: Encontrar los artistas más prolíficos del museo")

# Funciones de inicializacion

def initCatalog():
    """
    Inicializa el catalogo del museo MoMA
    """
    return controller.initCatalog()

def loadData(catalog):
    """
    Carga los artistas y obras en el catalogo
    """
    controller.loadData(catalog)

# Funciones para la impresión de tablas

def printArtistTable(info):
    x = PrettyTable(hrules=prettytable.ALL)
    x.field_names = ["ConstituentID", "DisplayName",
                    "BeginDate", "Nationality", 
                    "Gender", "ArtistBio", 
                    "Wiki QID", "ULAN"]

    x._max_width = {"DisplayName":18}

    for i in lt.iterator(info):
        x.add_row([ i["ConstituentID"], i["DisplayName"], 
                    i["BeginDate"], i["Nationality"], 
                    i["Gender"], i["ArtistBio"], 
                    i["Wiki QID"], i["ULAN"]])
    x.align = "l"
    x.align["ConstituentID"] = "r"
    x.align["BeginDate"] = "r"
    print(x)
 
def printArtworkTable(info):
    x = PrettyTable(hrules=prettytable.ALL)
    x.field_names = ["ObjectID", "Title", 
                    "ConstituentID", "Medium", 
                    "Dimensions", "Date", 
                    "Date Acquired", "TransCost (USD)","URL"]

    x._max_width = {"Title":18,"ConstituentID":18, "Medium":18, "Dimensions":18, "URL":15}

    for i in lt.iterator(info):
        if i["Date"] == 5000:
            x.add_row([ i["ObjectID"], i["Title"], 
                        i["ConstituentID"], i["Medium"], 
                        i["Dimensions"], "Unknown", 
                        i["DateAcquired"], i["TransCost"], i["URL"]])
        else:
            x.add_row([ i["ObjectID"], i["Title"], 
                        i["ConstituentID"], i["Medium"], 
                        i["Dimensions"], i["Date"], 
                        i["DateAcquired"],i["TransCost"], i["URL"]])
    x.align = "l"
    x.align["ObjectID"] = "r"
    x.align["Date"] = "r" 
    print(x)

def PrintArtistMedium (info):
    x = PrettyTable(hrules=prettytable.ALL)
    x.field_names = ["Medium Name", "Count"]
    keys = mp.keySet(info)
    for key in lt.iterator(keys):
        count = mp.get(info, key)['value']['size']
        x.add_row([key, count])
    x.sortby = "Count"
    x.reversesort = True
    x.align["Medium Name"] = "l"
    x.align["Count"] = "r"
    if lt.size(keys) > 5:
        print("Her/his top 5 Medium/Technique are")
        print(x.get_string(start=0, end=5))
    else:
        print("Her/his Medium/Technique are:")
        print(x)


# Funciones para impresion de resultados
def PrintReq1 (beginDate, endDate, InRange):
    print("="*15, " Req No. 1 Inputs ", "="*15)
    print("Artist born between" , beginDate, "and" , endDate, "\n")
    print("="*15, " Req No. 1 Answer ", "="*15)
    print("There are", InRange[1], "artist born between", beginDate, "and" , endDate,"\n")
    if InRange[1] !=0:
        if InRange[1] >=6:
            print("The first 3 artist in the range are...")
            primeros = controller.getFirst(InRange[0], 3)
            ultimos = controller.getLast(InRange[0], 3)
            printArtistTable(primeros)
            print("The last 3 artist in the range are...")
            printArtistTable(ultimos)
        else:
            print("The artist in the range are...")
            printArtistTable(InRange[0])
    
def PrintReq2 (first, last, InRange):
    print("="*15, " Req No. 2 Inputs ", "="*15)
    print("Artwork aquired between", first ,"and", last ,"\n")
    print("="*15, " Req No. 2 Answer ", "="*15)
    print("The MoMA acquired", InRange[1] ,"unique pieces between", first, "and" , last)
    print("Of which", InRange[2], "were purchased\n")
    if InRange[1]!= 0:
        if InRange[1] >= 6:
            print("The first 3 artworks in the range are...")
            primeros = controller.getFirst(InRange[0], 3)
            printArtworkTable(primeros)

            print("\nThe last 3 artworks in the range are...")  
            ultimos = controller.getLast(InRange[0], 3)
            printArtworkTable(ultimos)  
        else:
            print("The artworks in the range are...")
            printArtworkTable(InRange[0])

def PrintReq3 (mediumMap, mediumTop, size, id, artistName):
    print("="*15, " Req No. 3 Inputs ", "="*15)
    print("Examine the work of the artist named: "+artistName+"\n")
    print("="*15, " Req No. 3 Answer ", "="*15)
    print(artistName, "with MoMA ID",id, "has", size, "pieces in her/his name at the museum.")
    if size != 0:
        print("There are" ,mp.size(mediumMap), "different mediums/techniques in her/his work.\n")
        PrintArtistMedium(mediumMap)

        numPieces = mp.get(mediumMap, mediumTop)['value']['size']
        print("\nHis/her most used Medium/Technique is:", mediumTop , "with", numPieces, "pieces.")
        artistArt = mp.get(mediumMap, mediumTop)['value']['artworks']

        if numPieces >=6:
            first = controller.getFirst(artistArt,3)
            last = controller.getLast(artistArt,3)
            print("The first 3 works of",mediumTop,"from the collection are:")
            printArtworkTable(first)
            print("The last 3 works of",mediumTop,"from the collection are:")
            printArtworkTable(last)
        else:
            print("The",numPieces,"works of",mediumTop,"from the collection are:")
            printArtworkTable(artistArt)

def PrintReq4 (nacionalidad, First, Last, Top, Nat):
    print("="*15, " Req No. 4 Inputs ", "="*15)
    print("Ranking countries by their number of artworks in the MoMA...")
    print("="*15, " Req No. 4 Answer ", "="*15)
    print("The TOP 10 Countries in the MoMA are:")
    x = PrettyTable(hrules=prettytable.ALL)
    x.field_names = ["Artworks", "Nationality"]
    for value in lt.iterator(nacionalidad):
        x.add_row([value['Longitud'], value['Nacionalidad']])
    print(x)
    print("The TOP nationality in the museum is " + str(Nat) + " with " + str(Top) + " unique pieces")
    print("The first and last 3 objects in the " + str(Nat) + " artwork list are:")
    printArtworkTable(First)
    printArtworkTable(Last)

def PrintReq5 (departamento, ArtworkDepartment):
    print("="*15, " Req No. 5 Inputs ", "="*15)
    print("Estimate the cost to transport all artifacts in " + departamento + " MoMA's Departament")
    print("="*15, " Req No. 5 Answer ", "="*15)
    print("The MoMA is going to transport", ArtworkDepartment[1], "from the",departamento)
    print("REMEMBER! NOT all MoMA's data is complete !!! .... These are estimates.")
    print("Estimated cargo weight (kg):", round(ArtworkDepartment[3],3))
    print("Estimated cargo cost (USD):", round(ArtworkDepartment[2],3))

    print("\nThe TOP 5 oldest items to transport are:")
    printArtworkTable(ArtworkDepartment[0])
    print("\nThe TOP 5 most expensive items to transport are:")
    printArtworkTable(ArtworkDepartment[4])

def PrintReq6 ():
    pass

# Menu principal

catalog = None

while True:
    printMenu()
    inputs = int(input('Seleccione una opción para continuar\n'))
    if inputs == 1:     #carga de datos
        start = tm.process_time()

        print("Inicializando Catálogo ....")
        catalog = controller.initCatalog()
        print("Cargando información de los archivos ....")
        controller.loadData(catalog)
        print('Obras de Arte cargadas:',lt.size(catalog['Artworks']))
        print('Artistas cargados:',lt.size(catalog['Artists']))

        end = tm.process_time()
        total_time = (end - start)
        print("The time it took to execute the requirement was:", total_time*1000 ,"mseg ->",total_time, "seg\n")

    elif inputs == 2:   #req 1
        start = tm.process_time()

        beginDate = int(input("Ingrese el año inicial: "))
        endDate = int(input("Ingrese el año final: "))

        InRange = controller.getCronologicalArtist(catalog,beginDate,endDate)
        PrintReq1(beginDate, endDate, InRange)

        end = tm.process_time()
        total_time = (end - start)
        print("The time it took to execute the requirement was:", total_time*1000 ,"mseg ->",total_time, "seg\n")
        
    elif inputs == 3:   #req 2
        start = tm.process_time()

        firstY=int(input("Año incial (AAAA): "))
        firstM=int(input("Mes incial: "))
        firstD=int(input("Dia inicial: "))
        first = dt.date(firstY,firstM,firstD)
        
        lastY=int(input("Año final (AAAA): "))
        lastM=int(input("Mes final: "))
        lastD=int(input("Dia final: "))
        last=dt.date(lastY,lastM,lastD)

        InRange = controller.getCronologicalArtwork(catalog, first, last)
        PrintReq2(first, last, InRange)

        end = tm.process_time()
        total_time = (end - start)
        print("The time it took to execute the requirement was:", total_time*1000 ,"mseg ->",total_time, "seg\n")

    elif inputs == 4:   #req 3
        start = tm.process_time()

        artistName= input("Ingrese el nombre de la/el artista: ")
        artistInfo = controller.getArtist(catalog, artistName.lower())
        if not artistInfo:
            print("El/la artista no se encontro")
            continue
        if not artistInfo[0]:
            print("El/la artista con id", artistInfo[1], "no tiene obras a su nombre")
            continue

        mediumTop, size = controller.getMediumInfo(artistInfo[0])
        PrintReq3(artistInfo[0], mediumTop, size, artistInfo[1], artistName)

        end = tm.process_time()
        total_time = (end - start)
        print("The time it took to execute the requirement was:", total_time*1000 ,"mseg ->",total_time, "seg\n")

    elif inputs == 5:   #req 4
        start = tm.process_time()

        nacionalidad = controller.getNationalityandArtwork(catalog)
        List_Nationality = nacionalidad[0]
        First = nacionalidad[1]
        Last = nacionalidad[2]
        Top = nacionalidad[3]
        Nat = nacionalidad[4]
        PrintReq4(List_Nationality, First, Last, Top, Nat)

        end = tm.process_time()
        total_time = (end - start)
        print("The time it took to execute the requirement was:", total_time*1000 ,"mseg ->",total_time, "seg\n")
        
    elif inputs == 6:   #req 5
        start = tm.process_time()

        departamento = input("Ingrese el nombre del departamento del museo: ")
        ArtworkDepartment = controller.getArworkByDepartment(catalog, departamento.lower())
        PrintReq5(departamento, ArtworkDepartment)

        end = tm.process_time()
        total_time = (end - start)
        print("The time it took to execute the requirement was:", total_time*1000 ,"mseg ->",total_time, "seg\n")

    elif inputs == 7:   #req 6
        
        pass

    else:
        sys.exit(0)
sys.exit(0)
