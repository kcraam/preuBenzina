# -*- coding: utf-8 -*-

import urllib, json
from operator import itemgetter


url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
response = urllib.urlopen(url)
data = json.loads(response.read())


print "\nActualitzat el :" + data['Fecha']
print str(len(data["ListaEESSPrecio"])) + " Estacions de servei trobades"
print "=" * 50
#print json.dumps(filter(lambda ES: ES['IDEESS'] == '2836', data["ListaEESSPrecio"]))
# REPSOL Santa Rosa ""IDEESS": "2836""
# PETROPRIX "IDEESS": "12913"

ben_id = ['2836', '12913', '10141']

def search(list, key, value):
    for item in list:
        if item[key] == value:
            return item

ben_list = list()

for item in ben_id:
    ben_list.append(search(data["ListaEESSPrecio"], 'IDEESS', item))

ben_sort = sorted(ben_list, key=itemgetter('Precio Gasoleo A'))

for item in ben_sort:
    print item[u'R\xf3tulo'] + " Precio Gasoleo A:\t\t" + item[u'Precio Gasoleo A']

