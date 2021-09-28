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
    print("2- Lab5: las n obras más antiguas para un medio específico")
    # print("2- Req 1: Listar cronológicamente los artistas")
    # print("3- Req 2: Listar cronológicamente las adquisiciones")
    # print("4- Req 3: Clasificar obras de un artista por técnica")
    # print("5- Req 4: Clasificar obras por la nacionalidad de sus creadores")
    # print("6- Req 5: Transportar obras de un departamento")
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

# Funciones para la impresión de resultados

def printArtistTable(artist):
    x = PrettyTable(hrules=prettytable.ALL)
    x.field_names = ["ConstituentID", "DisplayName",
                    "BeginDate", "Nationality", 
                    "Gender", "ArtistBio", 
                    "Wiki QID", "ULAN"]

    x._max_width = {"DisplayName":18}

    for i in lt.iterator(artist):
        x.add_row([ i["ConstituentID"], i["DisplayName"], 
                    i["BeginDate"], i["Nationality"], 
                    i["Gender"], i["ArtistBio"], 
                    i["Wiki QID"], i["ULAN"]])
    x.align = "l"
    x.align["ConstituentID"] = "r"
    x.align["BeginDate"] = "r"
    print(x)

def printArtworkTable(artwork):
    x = PrettyTable(hrules=prettytable.ALL)
    x.field_names = ["ObjectID", "Title", 
                    "ConstituentID", "Medium", 
                    "Dimensions", "Date", 
                    "Date Acquired", "URL"]

    x._max_width = {"Title":18,"ConstituentID":18, "Medium":18, "Dimensions":18, "URL":15}

    for i in lt.iterator(artwork):
        if i["Date"] == 0:
            x.add_row([ i["ObjectID"], i["Title"], 
                        i["ConstituentID"], i["Medium"], 
                        i["Dimensions"], "Unknown", 
                        i["DateAcquired"], i["URL"]])
        else:
            x.add_row([ i["ObjectID"], i["Title"], 
                        i["ConstituentID"], i["Medium"], 
                        i["Dimensions"], i["Date"], 
                        i["DateAcquired"], i["URL"]])
    x.align = "l"
    x.align["ObjectID"] = "r"
    x.align["Date"] = "r" 
    print(x)



# Funciones para el laboratorio

def PrintLab5 (art, num):
    if art:
        print("Se encontraton",lt.size(art),"obras creadas con el medio ingresado")
        if lt.size(art) > num:
            print("Las", num, "obras mas antiguas son:")
            antiguas = controller.getLast(art, num)
            printArtworkTable(antiguas)
        else:
            print("Las obras creadas con el medio ingresado son:")
            printArtworkTable(art)

    else:
        print("No se encontraton obras.\n")




# Menu principal

catalog = None
while True:
    printMenu()
    inputs = int(input('Seleccione una opción para continuar\n'))
    if inputs == 1:
        print("Inicializando Catálogo ....")
        catalog = controller.initCatalog()
        print("Cargando información de los archivos ....")
        controller.loadData(catalog)

    elif inputs == 2:
        medio = input("Escriba el medio especifico que quiere consultar: ")
        num = int(input("Escriba el número de obras que quiere imprimir: "))
        ArtworksByMedium = controller.getMedium(catalog, medio)
        PrintLab5(ArtworksByMedium, num)

    else:
        sys.exit(0)
sys.exit(0)
