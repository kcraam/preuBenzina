#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Kcraam"
__date__ = "30/9/16"

import urllib, json
from operator import itemgetter
from functools import cmp_to_key

from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt


def search(list, key, value):
    for item in list:
        if item[key] == value:
            return item


def get_es(url):
    response = urllib.urlopen(url)
    return json.loads(response.read())


def multikeysort(items, columns):
    comparers = [
        ((i(col[1:].strip()), -1) if col.startswith('-') else (i(col.strip()), 1))
        for col in columns
    ]
    def comparer(left, right):
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))

def main():

    url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
    ben_id = ['2836', '12913', '10141','12368']
    ben_list = list()

    user_lat = 41.4850199
    user_lon = 2.1417081


    try:
        with open('EstacionesTerrestres.json') as json_data:
         data = json.load(json_data)
         if datetime.now() - datetime.strptime(data['Fecha'], "%d/%m/%Y %H:%M:%S") >= timedelta(days=1):
             print "Han pasat mes de 30' desde l'ultima actualitzacio"
             data = get_es(url)
             with open('EstacionesTerrestres.json', 'w') as outfile:
                  json.dump(data, outfile)
         else:
             print "La cache encara es valida: " + data['Fecha'],
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "No s'ha trobat cap cache"
        data = get_es(url)
        with open('EstacionesTerrestres.json', 'w') as outfile:
            json.dump(data, outfile)

    print "\nActualitzat el: " + data['Fecha']
    print str(len(data["ListaEESSPrecio"])) + " Estacions de servei a Espanya"

    """
    # print json.dumps(filter(lambda ES: ES['IDEESS'] == '2836', data["ListaEESSPrecio"]))
    # REPSOL Santa Rosa ""IDEESS": "2836""
    # PETROPRIX "IDEESS": "12913"

    for item in ben_id:
       ben_list.append(search(data["ListaEESSPrecio"], 'IDEESS', item))

    """
    for benzineres in data["ListaEESSPrecio"]:
        try:
            dist = haversine(user_lon, user_lat, float(benzineres['Longitud (WGS84)'].replace(",", ".")),
                         float(benzineres['Latitud'].replace(",", ".")))

            if dist <= 5 and benzineres[u'Precio Gasoleo A'] != None:
                benzineres[u'dist'] = str(round(dist,3))
                #print "Lon: " + benzineres[u'Longitud (WGS84)'].replace(",", ".") +" | "+ benzineres[u'Latitud'].replace(",", ".")
                ben_list.append(benzineres)
        except:
            pass


    #ben_sort = sorted(ben_list, key=itemgetter('Precio Gasoleo A'))

    print str(len(ben_list)) + " Estacions de servei a <= 5km"
    print "=" * 50
    ben_sort = sorted(ben_list, key=itemgetter('Precio Gasoleo A', 'dist'))
    #ben_sort = multikeysort(ben_list, 'Precio Gasoleo A', 'dist')
    #ben_sort = sorted(ben_list, key=lambda k: (k[u'Precio Gasoleo A'].lower(), k[u'dist']))

    for item in ben_sort:
        #dist = haversine(user_lon, user_lat,float(item['Longitud (WGS84)'].replace(",",".")), float(item['Latitud'].replace(",",".")))
        print item[u'R\xf3tulo'] + "\t " + item[u'Precio Gasoleo A'] + " a " + item[u'dist'] + " km",
        #https://www.google.es/maps/@41.485864,2.1422284,16z
        #https://www.google.es/maps/dir//41.4860551,2.1665237/@41.486028,2.166639,17z
        #https://www.google.es/maps/dir/41.4848907,2.1412331/41.4860551,2.1665237/@41.4849189,2.1415121,17z
        #https://www.google.es/maps/dir/Lon_Origen,Lat_origen/Lon_desti,Lat_desti/@41.4849189,2.1415121,17z
        print "https://www.google.es/maps/dir/" + str(user_lat) + "," + str(user_lon) + "/"\
              + item['Latitud'].replace(",",".") + "," \
              + item['Longitud (WGS84)'].replace(",",".") + "@" \
              + item['Latitud'].replace(",",".") + "," \
              + item['Longitud (WGS84)'].replace(",",".") + ",17z"



def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
    http://www.johndcook.com/blog/python_longitude_latitude/
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c # Radius of earth in kilometers. Use 3956 for miles
    # https://en.wikipedia.org/wiki/Earth_radius#Rectifying_radius
    return km

"""
            "Localidad": "CERDANYOLA DEL VALLES",
            "Latitud": "41,500278",
            "Longitud (WGS84)": "2,124972",
"""

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
    http://www.johndcook.com/blog/python_longitude_latitude/
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c # Radius of earth in kilometers. Use 3956 for miles
    # https://en.wikipedia.org/wiki/Earth_radius#Rectifying_radius
    return km

if __name__ == "__main__":
    main()