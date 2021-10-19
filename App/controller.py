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
 """

import config as cf
import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo del museo MoMA

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para agregar informacion al catalogo

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos.
    """
    loadArtist(catalog)
    loadArtwork(catalog)
    
def loadArtwork(catalog):
    """
    Carga las obras del archivo. Por cada obra se indica al
    modelo que debe adicionarla al catalogo.
    """
    Artworkfile = cf.data_dir + 'Artworks-utf8-large.csv'
    input_file = csv.DictReader(open(Artworkfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)

def loadArtist(catalog):
    """
    Carga los artistas del archivo. Por cada artista se indica al
    modelo que debe adicionarlo al catalogo.
    """
    Artistfile = cf.data_dir + 'Artists-utf8-large.csv'
    input_file = csv.DictReader(open(Artistfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)

# Funciones de ordenamiento

def SortbyDate (lista):
    """
    Retorna la lista ordenada por 'Date'
    """
    return model.SortbyDate(lista)

def SortbyCost (lista):
    """
    Retorna la lista ordenada por 'TransCost'
    """
    return model.SortbyCost(lista)

# Funciones de consulta sobre el catálogo

def getLast(catalog, num):
    """
    Retorna los ultimos 'num' elementos de una lista.
    """
    return model.getLast(catalog, num)

def getFirst(catalog, num):
    """
    Retorna los primeros 'num' elementos de una lista.
    """
    return model.getFirst(catalog, num)

def getCronologicalArtist(indice, beginDate, endDate):
    """
    Req 1
    """
    return model.getCronologicalArtist(indice, beginDate, endDate)

def getCronologicalArtwork (indice, first, last):
    """
    Req 2
    """
    return model.getCronologicalArtwork(indice, first, last)

def getArtist(catalog, name):
    """
    Req 3
    """
    return model.getArtist(catalog, name)

def getMediumInfo(artistArt):
    """
    Req 3
    """
    return model.getMediumInfo(artistArt)

def getNationalityandArtwork(catalog):
    return model.getNationalityandArtwork(catalog)


def getArworkByDepartment (catalog, departamento):
    """
    Req 5
    """
    return model.getArworkByDepartment(catalog, departamento)
