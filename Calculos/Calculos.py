#Calculo de la Eto
from ast import Import, parse
from cmath import pi, tan
import json as js
import math


def calculoEto(variables):
    temperaturaMax = 0
    temperaturaMin = 1
    presionVapor = 1
    
    return 0

def calcular_radiacion_solar(data):








def radiacion_extraterrestre(data, dia_juliano):
    constante_solar = 0.082
    info = js.loads(data)

    hora_inicio = info["sensado"]["horainicio"]
    hora_fin = info["sensado"]["horafin"]
    hora_media = (hora_inicio + hora_fin) / 2
    grades = info["altura"]["grades"]
    minutes = info["altura"]["minutes"]
    latitud_radianes = 0.0
    distancia_tierra_sol = 0.0
    declinacion_solar = 0.0
    angulo_solar_medio = 0.0
    grados_greenwich = info["longitud"]["grados"]
    correcion_estacional = 0.0
    fraccion_tiempo_sensado = info["sensado"]["fraccion"]

    if info["altura"]["orientation"] == 'N' :
        grades_decimal = grades + (minutes/60)
        latitud_radianes = round((math.pi/180) * grades_decimal, 2)
    else:
        grades_decimal = grades + (minutes/60)
        latitud_radianes = round((math.pi/180) * grades_decimal, 2)

    #Calculamos la longitud oeste de greenwich
    longitud_oeste_greenwith = (((info["longitud"]["segundos"] / 60) + (info["longitud"]["minutos"]))/60) + info["longitud"]["grados"]

    #Calculamos la distancia inversa entre el sol y la tierra (formula 23)
    distancia_tierra_sol = 1 + 0.033 * math.cos((2*math.pi)*julian_day/365)
    
    #Calculamos la declinación solar (formula 24)
    declinacion_solar = 0.409 * math.sin((2*math.pi*julian_day)/365 - 1.39)

    #Calculamos la constante b para la correcion estacional (formula 33)
    b = (2 * math.pi * (julian_day - 81) / 364)
    #Calculamos la correción estacional (formula 32)
    correcion_estacional = (0.1645 * math.sin(2 * b)) - (0.1255 * math.cos(b)) - (0.025 * math.sin(b))
    
    #Calculamos el angulo solar medio (formula 31)
    angulo_solar_medio = (math.pi / 12) * ((hora_media * 0.06667 * (grados_greenwich - longitud_oeste_greenwich) + correcion_estacional) - 12)

    #Calculamos el angulo solar medio w1 (formula 29)
    angulo_solar_medio1 = angulo_solar_medio - (math.pi * fraccion_tiempo_sensado / 24)
    #Calculamos el angulo solar medio w1 (formula 30)
    angulo_solar_medio2 = angulo_solar_medio + (math.pi * fraccion_tiempo_sensado / 24)

    #Calculamos la radiacion extraterrestre (formula 28)
    radicion_extraterrestre = (((12*60)/ math.pi) * constante_solar * distancia_tierra_sol * ((angulo_solar_medio2 - angulo_solar_medio1) * (math.sin(latitud_radianes)) * (math.sin(declinacion_solar)) + (math.cos(latitud_radianes) * math.cos(declinacion_solar) * (math.sin(angulo_solar_medio2) - math.sin(angulo_solar_medio1)))))

    return radiacion_extraterrestre

RadiacionExtraterrestre('{"altura" : {"grades": 13,"minutes": 44, "orientation": "N"}}')
RadiacionExtraterrestre('{"altura" : {"grades": 22,"minutes": 54, "orientation": "S"}}')

#Metodó para calcula la insolación maxima del día
def insolacion_maxima(radiacion_extraterrestre):
    return (24/math.pi) * radiacion_extraterrestre


def radiacion_solar(radiacion_extraterrestre):


    radiacion_onda_corta = 0.0
    duracion_real_insolacion = 0



def radicion_onda_corta(radiacion_extraterrestre):
    #Calculamos la radición de onda corta, usando de referencia un albedo (formula 38)
    return (1 - 0.23) * radiacion_extraterrestre