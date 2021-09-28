"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import quicksort as qui
from DISClib.Algorithms.Sorting import mergesort as mer
assert cf
import datetime as dt
import time
import math

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el catálogo de libros
    Crea una lista vacia para guardar todos los libros
    Se crean indices (Maps) por los siguientes criterios:
    Autores
    ID libros
    Tags
    Año de publicacion
    Retorna el catalogo inicializado.
    """
    catalog = {'Artworks': None,
               'Artists': None,
               'Mediums': None}

    catalog['Artworks'] = lt.newList('ARRAY_LIST')
    catalog['Artists'] = lt.newList('ARRAY_LIST')

    """
    Este indice crea un map cuya llave es el Medium de la obra
    """
    catalog['Mediums'] = mp.newMap(100,
                                 maptype='CHAINING',
                                 loadfactor=2.0,
                                 comparefunction=compareMapArtMedium)
        
    return catalog



# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    info = {}
    info["ConstituentID"] = int(artist['ConstituentID'])
    info["DisplayName"] = artist['DisplayName']
    info["ArtistBio"] = artist['ArtistBio']
    info["Nationality"] = artist['Nationality']
    info["Gender"] = artist['Gender']
    info["BeginDate"] = int(artist['BeginDate'])
    info["EndDate"] = int(artist['EndDate'])
    info["Wiki QID"] = artist['Wiki QID']
    info["ULAN"] = artist['ULAN']

    for key in info:
        if info[key] == "":
            info[key] = "Unknown"


    lt.addLast(catalog['Artists'], info)

def addArtwork(catalog, artwork):
    info ={}
    info["ObjectID"] = int(artwork['ObjectID'])
    info["Title"] = artwork['Title']

    constID_str = artwork['ConstituentID'].replace('[', '').replace(']','').split(",")
    info["ConstituentID"] = [int(x) for x in constID_str]

    info["Date"] = artwork['Date']
    info["Medium"] = artwork['Medium']
    info["Dimensions"] = artwork['Dimensions']
    info["CreditLine"] = artwork['CreditLine']
    info["AccessionNumber"] = artwork['AccessionNumber']
    info["Classification"] = artwork['Classification']
    info["Department"] = artwork['Department']
    info["DateAcquired"] = artwork['DateAcquired']
    info["Cataloged"] = artwork['Cataloged']
    info["URL"] = artwork['URL']
    info["Circumference (cm)"] = artwork['Circumference (cm)']
    info["Depth (cm)"] = artwork['Depth (cm)']
    info["Diameter (cm)"] = artwork['Diameter (cm)']
    info["Height (cm)"] = artwork['Height (cm)']
    info["Length (cm)"] = artwork['Length (cm)']
    info["Weight (kg)"] = artwork['Weight (kg)']
    info["Width (cm)"] = artwork['Width (cm)']
    info["Seat Height (cm)"] = artwork['Seat Height (cm)']
    info['Duration (sec.)'] = artwork['Duration (sec.)']

    for key in info:
        if key == 'DateAcquired':
            if info[key] == "":
                info[key] = dt.date.today()
                continue
            date = info[key].split("-")
            info[key]=dt.date(int(date[0]),int(date[1]),int(date[2]))
        
        elif key == 'Date':
            if info[key] == "":
                info[key] = 5000
                continue
            info[key] = int(info[key])
        
        elif key == 'Circumference (cm)' or key == 'Depth (cm)' or key == 'Diameter (cm)' \
            or key == 'Height (cm)' or key == 'Length (cm)' or key == 'Weight (kg)' or  key == 'Width (cm)':
            if info[key] == "":
                info[key] = float(0)
                continue
            info[key] = float(info[key])

        elif info[key] == "":
            info[key] = "Unknown"
    
    lt.addLast(catalog['Artworks'], info)
    
    addArtworkMedium(catalog, info)


def addArtworkMedium(catalog, info):
    mediums = catalog['Mediums']
    artMedium = info['Medium']
    existmedium = mp.contains(mediums, artMedium)
    if existmedium:
        entry = mp.get(mediums, artMedium)
        medium = me.getValue(entry)
    else:
        medium = newMedium(artMedium)
        mp.put(mediums, artMedium, medium)

    lt.addLast(medium['artworks'], info)

# Funciones para creacion de datos

def newMedium (artMedium):
    entry = {'medium': "", "artworks": None}
    entry['medium'] = artMedium
    entry['artworks'] = lt.newList('ARRAY_LIST', compareMediums)
    return entry

# Funciones de consulta
def getFirst(catalog, num):
    """
    Retorna los primeros num elementos de una lista
    """
    first = lt.newList('ARRAY_LIST')
    rangmax = num +1
    for i in range(1, rangmax):
        element = lt.getElement(catalog, i)
        lt.addLast(first, element)
    return first

def getLast(catalog, num):
    """
    Retorna los ultimos num elementos de una lista
    """
    last = lt.newList('ARRAY_LIST')
    rangmin = num-1
    for i in range((lt.size(catalog)-rangmin),lt.size(catalog)+1):
        element = lt.getElement(catalog, i)
        lt.addLast(last, element)
    return last


# Funciones de laboratorio

def getMedium(catalog, medio):
    ltMedium = mp.get(catalog['Mediums'], medio)
    art = None
    if ltMedium:
        art = me.getValue(ltMedium)['artworks']
        qui.sort(art, cmpArtworkByDate)
    return art



# Funciones utilizadas para comparar elementos dentro de una lista
def compareMapArtMedium (medium, entry):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (medium == identry):
        return 0
    elif (medium > identry):
        return 1
    else:
        return -1

def compareMediums (medium1, medium2):
    if (medium1 == medium2):
        return 0
    elif (medium1 > medium2):
        return 1
    else:
        return -1

def cmpArtworkByDate(artwork1, artwork2): 
    return artwork1['Date'] < artwork2['Date']

# Funciones de ordenamiento
