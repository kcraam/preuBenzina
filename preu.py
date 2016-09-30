#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Kcraam"
__date__ = "30/9/16"

import urllib, json
from operator import itemgetter
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt

url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
ben_id = ['2836', '12913', '10141']
ben_list = list()

def search(list, key, value):
    for item in list:
        if item[key] == value:
            return item


def get_es(url):
    response = urllib.urlopen(url)
    return json.loads(response.read())

def main():
    try:
        with open('EstacionesTerrestres.json') as json_data:
         data = json.load(json_data)
         if datetime.now() - datetime.strptime(data['Fecha'], "%d/%m/%Y %H:%M:%S") >= timedelta(seconds=1800):
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
    print str(len(data["ListaEESSPrecio"])) + " Estacions de servei trobades"
    print "=" * 50
# print json.dumps(filter(lambda ES: ES['IDEESS'] == '2836', data["ListaEESSPrecio"]))
# REPSOL Santa Rosa ""IDEESS": "2836""
# PETROPRIX "IDEESS": "12913"


    for item in ben_id:
       ben_list.append(search(data["ListaEESSPrecio"], 'IDEESS', item))

    ben_sort = sorted(ben_list, key=itemgetter('Precio Gasoleo A'))

    for item in ben_sort:
        print item[u'R\xf3tulo'] + " Precio Gasoleo A:\t\t" + item[u'Precio Gasoleo A']


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