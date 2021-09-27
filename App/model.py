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
assert cf

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
    catalog = {'artworks': None,
               'artists': None,
               'medium': None,
               'artistWork':None,
               'years':None}

    catalog['artworks'] = lt.newList('ARRAY_LIST')
    catalog['artists'] = lt.newList('ARRAY_LIST')

    """
    Este indice crea un map cuya llave es el Medium de la obra
    """
    catalog['medium'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMapArtMedium)
    """
    Este indice crea un map cuya llave es el id del artista de la obra
    """
    catalog['artistWork'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtistById)
    
    """
    Este indice crea un map cuya llave es el año de publicacion de la obra
    """
    catalog['years'] = mp.newMap(40,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareMapYear)

    
    return catalog

# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    lt.addLast(catalog['artists'], artist)

def addArtwork(catalog, artwork):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    lt.addLast(catalog['artworks'], artwork)
    mp.put(catalog['medium'], artwork['Medium'], artwork)
    constID_str = artwork['ConstituentID'].replace('[', '').replace(']','').split(",")
    artists = [int(x) for x in constID_str]

    for artist in artists:
        addArtworkArtist(catalog, artist, artwork)
    addArtworkYear(catalog, artwork)
    addArtworkMedium(catalog, artwork)


def addArtworkMedium(catalog, artwork):
    try:
        mediums = catalog['medium']
        if (artwork['Medium'] != ''):
            artMedium = artwork['Medium']
        else:
            artMedium = "Unknown"
        existmedium = mp.contains(mediums, artMedium)
        if existmedium:
            entry = mp.get(mediums, artMedium)
            medium = me.getValue(entry)
        else:
            medium = newMedium(artMedium)
            mp.put(mediums, artMedium, medium)
        lt.addLast(medium['artworks'], artwork)
    except Exception:
        return None


def addArtworkYear(catalog, artwork):
    try:
        years = catalog['years']
        if (artwork['Date'] != ''):
            pubyear = artwork['Date']
            pubyear = int(float(pubyear))
        else:
            pubyear = 2020
        existyear = mp.contains(years, pubyear)
        if existyear:
            entry = mp.get(years, pubyear)
            year = me.getValue(entry)
        else:
            year = newYear(pubyear)
            mp.put(years, pubyear, year)
        lt.addLast(year['artworks'], artwork)
    except Exception:
        return None

def newYear(pubyear):
    entry = {'year': "", "artworks": None}
    entry['year'] = pubyear
    entry['artworks'] = lt.newList('ARRAY_LIST', compareYears)
    return entry

def newMedium(artMedium):
    entry = {'medium': "", "artworks": None}
    entry['medium'] = artMedium
    entry['artworks'] = lt.newList('ARRAY_LIST', compareMediums)
    return entry


def addArtworkArtist(catalog, artistid, artwork):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    artists = catalog['artistWork']
    existartist = mp.contains(artists, artistid)
    if existartist:
        entry = mp.get(artists, artistid)
        artist = me.getValue(entry)
    else:
        artist = newArtistId(artistid)
        mp.put(artists, artistid, artist)

    lt.addLast(artist['artworks'], artwork)
    artist['Total_artworks'] = lt.size(artist['artworks'])

# Funciones para creacion de datos

def newArtistId(artistid):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    Artist_id = {'ConstituentID': "",
              "artworks": None,
              "Total_artworks": 0}

    Artist_id['ConstituentID'] = artistid
    Artist_id['artworks'] = lt.newList('ARRAY_LIST', compareArtistById)
    return Artist_id

# Funciones de consulta

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

def compareArtistById(id, artist):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    artistentry = me.getKey(artist)
    if (int(id) == int(artistentry)):
        return 0
    elif (int(id) > int(artistentry)):
        return 1
    else:
        return -1

def compareMapYear(id, tag):
    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
        return 1
    else:
        return 0

def compareYears(year1, year2):
    if (int(year1) == int(year2)):
        return 0
    elif (int(year1) > int(year2)):
        return 1
    else:
        return 0

def compareMediums (medium1, medium2):
    if (medium1 == medium2):
        return 0
    elif (medium1 > medium2):
        return 1
    else:
        return 0

# Funciones de ordenamiento
