﻿"""
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
    """ 
    Inicializa el catálogo de libros
    Crea una lista vacia para guardar todos las obras.
    Crea una lista vacia para guardar todos los artistas.
    Se crean indices (Maps) por los siguientes criterios:
        -Nombre del artista
        -Id Artistas 
        -Medio o técnica con la que se creo la obra.
        -Año en que se creo la obra.
        -Fecha de adquisición de la obra.
        -Departamento al que pertenece la obra
        -Fecha de nacimiento del artista.
    Retorna el catalogo inicializado.
    """
    catalog = {'Artworks': None,
               'Artists': None,
               'ArtistsNames':None,
               'ArtistsWorks':None,
               'DatesAcquired': None,
               'Departments': None,
               'BeginDates': None,
               'Mediums': None,
               'Nationality':None}

    catalog['Artworks'] = lt.newList('ARRAY_LIST')
    catalog['Artists'] = lt.newList('ARRAY_LIST')

    #Este indice crea un map cuya llave es el nombre del artista.
    catalog['ArtistsNames'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtistByName)
    
    #Este indice crea un map cuya llave es el id del artista.
    catalog['ArtistsId'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtistIds)
    
    #Este indice crea un map cuya llave es el id del artista.
    catalog['ArtistsWorks'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtistIds)
    
    #Este indice crea un map cuya llave es la fecha de adquisición de la obra.
    catalog['DatesAcquired'] = mp.newMap(435,
                                   maptype='CHAINING',
                                   loadfactor=8.0,
                                   comparefunction=compareMapYear)
    
    #Este indice crea un map cuya llave es el departamento al que pertenece la obra.
    catalog['Departments'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtworkByDepartment)
    
    #Este indice crea un map cuya llave es la fecha de nacimiento del artista.
    catalog['BeginDates'] = mp.newMap(479,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareMapYear)
    
    #LAB Este indice crea un map cuya llave es el Medium de la obra.
    catalog['Mediums'] = mp.newMap(41,
                                 maptype='CHAINING',
                                 loadfactor=1.0,
                                 comparefunction=compareMapArtMedium)
    
    #LAB Este indice crea un map cuya llave es el la nacionalidad de la obra.
    catalog['Nationality'] = mp.newMap(41,
                                 maptype='CHAINING',
                                 loadfactor=1.0,
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
        if key == "Nationality" and info[key] == "":
            info[key] = "Nationality unknown"
        if info[key] == "":
            info[key] = "Unknown"

    lt.addLast(catalog['Artists'], info)
    mp.put(catalog['ArtistsNames'], info['DisplayName'].lower(), info)
    mp.put(catalog["ArtistsId"], info["ConstituentID"], info)
    addArtistBeginDate(catalog['BeginDates'], info)
    
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
    
    for artist in info["ConstituentID"]:
        addArtistWork(catalog['ArtistsWorks'], artist, info)
        addArtworkNationality(catalog, info, artist) #lab
    lt.addLast(catalog['Artworks'], info)
    addArtworkDepartment(catalog['Departments'], info)
    addArtworkDateAcquired(catalog['DatesAcquired'], info)
    addArtworkMedium(catalog['Mediums'], info) # lab

def addArtistWork(indice, artistId, info):
    artists = indice
    existartist = mp.contains(artists, artistId)
    if existartist:
        entry = mp.get(artists, artistId)
        artist = me.getValue(entry)
    else:
        artist = newArtistId(artistId)
        mp.put(artists, artistId, artist)
    
    addArtworkMedium(artist['mediums'], info)
    
def addArtworkMedium(indice, info):
    mediums = indice
    artMedium = info['Medium'].lower()
    existmedium = mp.contains(mediums, artMedium)
    if existmedium:
        entry = mp.get(mediums, artMedium)
        medium = me.getValue(entry)
    else:
        medium = newMedium(artMedium)
        mp.put(mediums, artMedium, medium)

    lt.addLast(medium['artworks'], info)
    medium['size']+=1

def addArtworkDepartment(indice, info):
    departments = indice
    artDepartment = info['Department'].lower()
    existdepartment= mp.contains(departments, artDepartment)
    if existdepartment:
        entry = mp.get(departments, artDepartment)
        department = me.getValue(entry)
    else:
        department = newDepartment(artDepartment)
        mp.put(departments, artDepartment, department)

    lt.addLast(department['artworks'], info)

def addArtworkDateAcquired (indice, info):
    dates = indice
    artDate = info['DateAcquired']
    existdate = mp.contains(dates, artDate)
    if existdate:
        entry = mp.get(dates, artDate)
        date = me.getValue(entry)
    else:
        date = newDateAcquired(artDate)
        mp.put(dates, artDate, date)

    lt.addLast(date['artworks'], info)

def addArtistBeginDate(indice, info):
    dates = indice
    artistDate = info['BeginDate']
    existdate = mp.contains(dates, artistDate)
    if existdate:
        entry = mp.get(dates, artistDate)
        date = me.getValue(entry)
    else:
        date = newBeginDate(artistDate)
        mp.put(dates, artistDate, date)

    lt.addLast(date['artists'], info)
    date['size']+=1

def addArtworkNationality (catalog, info, id):
    nationalities = catalog['Nationality']

    ltArtist = mp.get(catalog['ArtistsId'], id)["value"]   
    artnationality = ltArtist['Nationality'].lower()
    
    existnationality = mp.contains(nationalities, artnationality)
    if existnationality:
        entry = mp.get(nationalities, artnationality)
        nationality = me.getValue(entry)
    else:
        nationality = newDateAcquired(artnationality)
        mp.put(nationalities, artnationality, nationality)
    lt.addLast(nationality['artworks'], info)

        

# Funciones para creacion de datos

def newMedium (artMedium):
    entry = {'medium': "", "artworks": None, "size": 0}
    entry['medium'] = artMedium.lower()
    entry['artworks'] = lt.newList('ARRAY_LIST', cmpArtworksByMedium)
    return entry

def newArtistId (id):
    entry = {'id': "", "mediums":None}
    entry['id'] = id
    entry['mediums'] = mp.newMap(41,
                                 maptype='CHAINING',
                                 loadfactor=1.0,
                                 comparefunction=compareMapArtMedium)
    return entry

def newDepartment (artDepartment):
    entry = {'department': "", "artworks":None}
    entry['department'] = artDepartment.lower()
    entry['artworks'] = lt.newList('ARRAY_LIST')
    return entry

def newDateAcquired (artDate):
    entry = {'date': "", "artworks": None}
    entry['date'] = artDate
    entry['artworks'] = lt.newList('ARRAY_LIST', cmpArtworkByDate)
    return entry

def newBeginDate (artistDate):
    entry = {'begindate': "", "artists": None, "size": 0}
    entry['begindate'] = artistDate
    entry['artists'] = lt.newList('ARRAY_LIST', cmpArtworkByDate)
    return entry

def newNationality(nationality):
    entry = {'nationality': "", "artworks": None}
    entry['nationality'] = nationality.lower()
    entry['artworks'] = lt.newList('ARRAY_LIST', cmpArtworksByNationality)
    return entry

# Funciones de consulta

def getFirst(lista, num):
    """
    Retorna los primeros num elementos de una lista
    """
    lista = lt.subList(lista, 1, num)
    return lista

def getLast(lista, num):
    """
    Retorna los ultimos num elementos de una lista
    """
    lista = lt.subList(lista, lt.size(lista)-(num-1), num)
    return lista


def getArtist(catalog, name):
    """
    Req 3:
    Busca el nombre que ingresa por parametro en un map cuya llave = nombre del artista, 
    toma su id y lo busca en un map cuya llave = id del artista.
    param:
        -catalog: Catalgo del museo MoMA
        -name: Nombre del artista a consulta
    return:
        -None: Si no se encontro el artista
        -tuple: 
            - TAD map: llave = nombre del medio;  valor = Lista de obras que pertenecen a dicho medio 
            - Int: El id del artista
    """
    InfoArtist = mp.get(catalog['ArtistsNames'], name)
    
    if not InfoArtist:
        return None
    info = me.getValue(InfoArtist)
    id = info['ConstituentID']
    ltArtist = mp.get(catalog['ArtistsWorks'], id)
    art = None
    if ltArtist:
        art = me.getValue(ltArtist)['mediums']
    return art, id

def getMediumInfo(artistArt):
    """
    Req 3
    Por cada medio que existe toma la longitud de la lista de obras y las suma a un contador, 
    a la par va buscando cual es medio con mas cantidad de obras.

    param:
        -artistArt: TAD map: llave = nombre del medio;  valor = Lista de obras que pertenecen a dicho medio

    return:
        -tuple: 
            - Str: el medio con mas cantidad de obras 
            - Int: el numero total de obras
    """
    keys = mp.keySet(artistArt)

    top = 0
    topMedium = None
    artSize = 0

    for medium in lt.iterator(keys):
        medio = mp.get(artistArt, medium)["value"]
        artSize += lt.size(medio["artworks"])

        size = medio["size"]

        if size > top:
            top = size
            topMedium = medium
    
    return topMedium, artSize


def getCronologicalArtist(indice, beginDate, endDate):
    InRange = mp.newMap(479,
                        maptype='PROBING',
                        loadfactor=0.5,
                        comparefunction=compareMapYear)

    keys = mp.keySet(indice)
    contador = 0

    for key in lt.iterator(keys):
        if beginDate <= int(key) and endDate >= int(key):
            año = mp.get(indice, key)
            value = me.getValue(año)
            artistas = value['artists']
            size = value['size']
            mp.put(InRange, key, artistas)
            contador += size

    return InRange, contador


# Funciones de laboratorio

def getMedium(catalog, medio):
    ltMedium = mp.get(catalog['Mediums'], medio)
    art = None
    if ltMedium:
        art = me.getValue(ltMedium)['artworks']
        qui.sort(art, cmpArtworkByDate)
    return art

def getNationality(catalog, nacionalidad):
    ltNationality = mp.get(catalog['Nationality'], nacionalidad)
    art = None
    if ltNationality:
        art = me.getValue(ltNationality)['artworks']
    return art


# Funciones utilizadas para comparar elementos dentro de una lista
def compareMapArtMedium (medium, entry):
    MediumEntry = me.getKey(entry)
    if (medium == MediumEntry):
        return 0
    elif (medium > MediumEntry):
        return 1
    else:
        return -1

def compareMapYear (date, entry):
    DateEntry = me.getKey(entry)
    if (date == DateEntry):
        return 0
    elif (date > DateEntry):
        return 1
    else:
        return 0

def compareArtistIds (id, entry):
    """
    Compara dos ids de artistas, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1 

def compareArtistByName(keyname, artist):
    ArtistEntry = me.getKey(artist)
    if (keyname.lower() == ArtistEntry):
        return 0
    elif (keyname.lower() > ArtistEntry):
        return 1
    else:
        return -1

def compareArtworkByDepartment (department, entry):
    DepartEntry = me.getKey(entry)
    if (department.lower() == DepartEntry):
        return 0
    elif (department.lower() > DepartEntry):
        return 1
    else:
        return -1
    
def cmpArtworksByMedium (artwork1, artwork2):
    return artwork1['Medium'] < artwork2['Medium']

def cmpArtworksByNationality (artwork1, artwork2):
     return artwork1['Nationality'] < artwork2['Nationality']

def cmpArtworkByDate(artwork1, artwork2): 
    return artwork1['Date'] < artwork2['Date']

# Funciones de ordenamiento
