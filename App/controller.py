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
    Artworkfile = cf.data_dir + 'Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(Artworkfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)

def loadArtist(catalog):
    """
    Carga los artistas del archivo. Por cada artista se indica al
    modelo que debe adicionarlo al catalogo.
    """
    Artistfile = cf.data_dir + 'Artists-utf8-small.csv'
    input_file = csv.DictReader(open(Artistfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)

# Funciones de ordenamiento

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

def GetElements(valueset):
    return model.GetElements(valueset)

def GetMoreElements(mapa, beginDate, endDate):
    return model.GetMoreElements(mapa, beginDate, endDate)

def getCronologicalArtist(indice, beginDate, endDate):
    """
    Req 1
    """
    return model.getCronologicalArtist(indice, beginDate, endDate)

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

# Funciones de laboratorio
def getMedium(catalog, medio):
    """
    Retorna la lista de obras que fueron creadas con el 
    medio dado.
    """
    return model.getMedium(catalog, medio)

def getNationality(catalog, nacionalidad):
    return model.getNationality(catalog, nacionalidad)