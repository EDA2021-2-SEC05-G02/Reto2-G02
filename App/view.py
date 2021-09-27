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


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Req 1: Listar cronológicamente los artistas")
    print("3- Req 2: Listar cronológicamente las adquisiciones")
    print("4- Req 3: Clasificar obras de un artista por técnica")
    print("5- Req 4: Clasificar obras por la nacionalidad de sus creadores")
    print("6- Req 5: Transportar obras de un departamento")
    print("7- Req 6: Encontrar los artistas más prolíficos del museo")

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


catalog = None


# Menu principal

while True:
    printMenu()
    inputs = int(input('Seleccione una opción para continuar\n'))
    if inputs == 1:
        print("Inicializando Catálogo ....")
        catalog = controller.initCatalog()
        print("Cargando información de los archivos ....")
        controller.loadData(catalog)

    elif inputs == 2:
        pass

    else:
        sys.exit(0)
sys.exit(0)
