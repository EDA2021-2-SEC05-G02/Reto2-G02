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
    catalog['DatesAcquired'] = mp.newMap(5591,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareMapYear)
    
    #Este indice crea un map cuya llave es el departamento al que pertenece la obra.
    catalog['Departments'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtworkByDepartment)
    
    #Este indice crea un map cuya llave es la fecha de nacimiento del artista.
    catalog['BeginDates'] = mp.newMap(1009,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareMapYear)
        
    #Este indice crea un map cuya llave es el la nacionalidad de la obra.
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
    info["BeginDate"] = artist['BeginDate']
    info["EndDate"] = artist['EndDate']
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
    addArtistBeginDate(catalog, info)
    
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
        if key == 'Date':
            if info[key] == "":
                info[key] = 5000
                continue
            info[key] = int(info[key])
        
        elif key == 'DateAcquired':
            if info[key] == '':
                info[key] = dt.date.today()
                continue
            date = info[key].split("-")
            info[key] = dt.date(int(date[0]),int(date[1]),int(date[2]))
        
        elif key == 'Circumference (cm)' or key == 'Depth (cm)' or key == 'Diameter (cm)' \
            or key == 'Height (cm)' or key == 'Length (cm)' or key == 'Weight (kg)' or  key == 'Width (cm)':
            if info[key] == "":
                info[key] = float(0)
                continue
            info[key] = float(info[key])

        elif info[key] == "":
            info[key] = "Unknown"
    
    #Calcular el costo de transporte
    Weight = info['Weight (kg)']
    Length = info['Length (cm)']
    Width = info['Width (cm)']
    Height = info['Height (cm)']
    Radius = (info['Diameter (cm)'] / 2) / 100

    m2 = (Height*Width)/10000
    m3 = (Height*Width*Length)/1000000
    m2_v2 = math.pi * (Radius**2)
    m3_v2 =  (4/3)*(math.pi)*(Radius**3)

    mayor = max(m2,m3,m2_v2,m3_v2,Weight)
    cost = 48
    if mayor != 0:
        cost = round(72*mayor, 3)

    info['TransCost'] = cost

    for artist in info["ConstituentID"]:
        addArtistWork(catalog, artist, info)
        addArtworkNationality(catalog, info, artist) #lab
    lt.addLast(catalog['Artworks'], info)
    addArtworkDepartment(catalog, info)
    addArtworkDateAcquired(catalog, info)

def addArtistWork(catalog, artistId, info):
    artists = catalog['ArtistsWorks']
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

def addArtworkDepartment(catalog, info):
    departments = catalog['Departments']
    artDepartment = info['Department'].lower()
    existdepartment= mp.contains(departments, artDepartment)
    if existdepartment:
        entry = mp.get(departments, artDepartment)
        department = me.getValue(entry)
    else:
        department = newDepartment(artDepartment)
        mp.put(departments, artDepartment, department)

    lt.addLast(department['artworks'], info)
    department['cost'] += info['TransCost']
    department['weight'] += info['Weight (kg)']
    department["size"] += 1

def addArtworkDateAcquired (catalog, info):
    years = catalog['DatesAcquired']
    pubyear = info['DateAcquired']
    existyear = mp.contains(years, pubyear)
    if existyear:
        entry = mp.get(years, pubyear)
        year = me.getValue(entry)
    else:
        year = newDateAcquired(pubyear)
        mp.put(years, pubyear, year)
    lt.addLast(year['artworks'], info)
    year['size'] += 1
    if "purchase" in info['CreditLine'].lower():
        year['purchase'] += 1


def addArtistBeginDate(catalog, info):
    years = catalog['BeginDates']
    if (info['BeginDate'] != ''):
        pubyear = info['BeginDate']
        pubyear = int(float(pubyear))
    else:
        pubyear = 2021
    existyear = mp.contains(years, pubyear)
    if existyear:
        entry = mp.get(years, pubyear)
        year = me.getValue(entry)
    else:
        year = newBeginDate(pubyear)
        mp.put(years, pubyear, year)
    lt.addLast(year['artists'], info)
    year['size']+=1

    
def addArtworkNationality (catalog, info, id):
    nationalities = catalog['Nationality']

    ltArtist = mp.get(catalog['ArtistsId'], id)["value"]   
    artnationality = ltArtist['Nationality'].lower()
    
    existnationality = mp.contains(nationalities, artnationality)
    if existnationality:
        entry = mp.get(nationalities, artnationality)
        nationality = me.getValue(entry)
    else:
        nationality = newNationality(artnationality)
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
    entry = {'department': "", "artworks":None, "cost": 0, "weight":0, "size":0}
    entry['department'] = artDepartment.lower()
    entry['artworks'] = lt.newList('ARRAY_LIST')
    return entry

def newDateAcquired (artDate):
    entry = {'year': "", "artworks": None, "size": 0, "purchase": 0}
    entry['year'] = artDate
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

def getCronologicalArtist(catalog, beginDate, endDate):
    """
    Req 1:
    Recorre las llaves del indice de BeginDates (llave=año, valor=lista de artistas)
    Agrega a una lista los artistas nacidos en el rango 
    param:
        -catalog: Catalogo MoMA
        -beginDate: Fecha de nacimiento inicial
        -endDate: Fecha de nacimiento final
    return:
        -tuple: 
            - ADT list: lista de artistas que nacieron en el rango de años 
            - Int: el total de artistas nacidos en el rango dado.
    """
    InRange = lt.newList('ARRAY_LIST')

    keys = mp.keySet(catalog['BeginDates'])
    contador = 0

    for key in lt.iterator(keys):
        if int(key) >= int(beginDate) and int(key) <= int(endDate):
            año = mp.get(catalog['BeginDates'], key)
            value = me.getValue(año)
            contador += value['size']
            for artist in lt.iterator(value['artists']):
                lt.addLast(InRange,artist)

    InRangeSorted = mer.sort(InRange, cmpArtistByBeginDate)  #n*log(n)
    return InRangeSorted, contador

def getCronologicalArtwork (catalog, first, last):
    """
    Req 2:
    Recorre las llaves del indice de DatesAcquired (llave=año, valor=lista de obras)
    Agrega a una lista las obras adquiridas en el rango y de esas obras calcula cuantas
    fueron compradas (purchase) y la cantidad de obras en el rango.
    param:
        -catalog: Catalogo MoMA
        -first: Fecha de adquisicion inicial
        -last: Fecha de adquisicion final
    return:
        -tuple: 
            - ADT list: lista de obras adquiridas en el rango de años 
            - Int: el total de obras adquiridas en el rango dado
            - Int: el total de obras adquiridas en el rango dado que fueron compradas
    """
    InRange = lt.newList('ARRAY_LIST')

    keys = mp.keySet(catalog['DatesAcquired'])
    contador = 0
    purchased = 0

    for key in lt.iterator(keys):
        if key >= first and key <= last:
            año = mp.get(catalog['DatesAcquired'], key)
            value = me.getValue(año)
            contador += value['size']
            purchased += value['purchase']
            for art in lt.iterator(value['artworks']):
                lt.addLast(InRange,art)

    InRangeSorted = mer.sort(InRange, cmpArtworkByDateAcquired) #n*log(n)
    return InRangeSorted, contador, purchased

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

def getNationalityandArtwork(catalog):
    """
    Req 4:
    Recorre las llaves del indice de nacionalidad (llave=nacionalidad, valor=lista de obras).
     - Agrega a una lista las obras de cada nacionalidad y se cuenta la cantidad de obras de cada nacionalidad.
     - Organizar la lista por longitud de la lista de obras de cada nacionalidad.
     - Se crea una sublista con el top 10 nacionalidades con mayor cantidad de obras a partir de la lista previamente organizada.
     - Se retornma los elementos que se encuentran en "Obras" de la nacionalidad con mayor cantidad de obras.
     - Se crean dos sublistas una para  los tres primeros y otra para los ultimos elementos de la lista de "Obras" de la nacionalidad con mayor cantidad de obras.
    param:
        -catalog: Catalogo MoMA
    return:
        -tuple: 
            - Dict: Diccionario con el top 10 de nacionalidades con mas obras - Check
            - Dict: Diccionario con las tres primeras obras de la nacionalidad con mas obras - Check
            - Dict: Diccionario con las tres ultimas obras de la nacionalidad con mas obras - Check
            - Int: El total de obras de la nacionalidad con mas obras - Check
            - String: La nacionalidad con mas obras - Check

    """
    lista = lt.newList('ARRAY_LIST')
    keys = mp.keySet(catalog['Nationality'])
    for key in lt.iterator(keys):
        nacionalidad = mp.get(catalog['Nationality'], key)
        if nacionalidad:
            value = me.getValue(nacionalidad)['artworks']
            lt.addLast(lista, {'Longitud': lt.size(value), 'Nacionalidad': key, 'Obras': value})
    mer.sort(lista, cmpArtworkbyNationality)
    sorted_list = lt.subList(lista, 1, 10)
    top = lt.getElement(sorted_list, 1)['Obras']
    nat = lt.getElement(sorted_list, 1)['Nacionalidad']
    first = lt.subList(top, 1, 3)
    last = lt.subList(top, lt.size(top)-2, 3)
    return sorted_list, first, last, lt.size(top), nat
    

def getArworkByDepartment (catalog, departamento):
    """
    Req 5
    Se busca en el incide de Departments el departamento ingresado por parametro
    llave: departamento, valor: dict(lista de obras, suma del costo de transporte, suma de los pesos,
                                    cuantas obras hay en el departamento)
        

    param:
        -catalog: Catalogo del museo MoMA
    return:
        -tuple: 
            - TAD Lista: lista de obras pertenecientes al departamento
            - Int: el numero total de obras
            - Int: suma del costo de trasporte de cada obra
            - Int: suma de los pesos de las obras
    """
    depto = mp.get(catalog['Departments'],departamento)
    value = me.getValue(depto)
    ltArtworks = value['artworks']
    size = value['size']
    cost = value['cost']
    weight = value['weight']
    return ltArtworks, size, cost, weight

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
        return -1

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
    return artwork1['Medium'].lower() < artwork2['Medium'].lower()

def cmpArtworksByNationality (artwork1, artwork2):
     return artwork1['Nationality'].lower() < artwork2['Nationality'].lower()

def cmpArtworkByDate(artwork1, artwork2): 
    return int(artwork1['Date']) < int(artwork2['Date'])

def cmpArtworkbyNationality(artist1, artist2):
    return artist1['Longitud'] > artist2['Longitud']

def cmpArtistByBeginDate(Artist1, Artist2):
    return (int(Artist1['BeginDate']) < int(Artist2['BeginDate']))

def cmpArtworkByDateAcquired(artwork1, artwork2): 
    return artwork1['DateAcquired'] < artwork2['DateAcquired']

# Funciones de ordenamiento
