#Calculo de la Eto
from ast import Import, parse
from cmath import pi, tan
import json as js
import math
import datetime



angulo_solar_puesta_sol = 0.0
array_temperaturas = [28.0,30.0,29.0,32.6,31.2] # °C
array_humedad = [24,23,67,56,43,25] # %
array_velocidad_viento = [60, 56, 47, 50, 45]

# def calculoEto(variables):
#     temperaturaMax = 0
#     temperaturaMin = 1
#     presionVapor = 1
    
#     return 0




def julian_day():
    today = datetime.datetime.now()
    julian = (today - datetime.datetime(today.year,1,1)).days + 1
    return julian


def radiacion_extraterrestre():#data, dia_juliano
    constante_solar = 0.082
    coordenadas = {'ltd':{'grados':2,'minutos':55,'segundos':39,'orientacion':'N'},
                   'lng':{'grados':75,'minutos':17,'segundos':15,'orientacion':'W'}
                   }
    ltd_lng_dec = {'ltd':2.9275, 'lng':-75.2875}
    ltd_lng_rad={'ltd':0.05109451385, 'lng':-1.314014761}
    fraccion_tiempo_sensado = 1 # duración del periodo considerado [horas]
    global angulo_solar_puesta_sol;

    # info = js.loads(data)

    # hora_inicio = info["sensado"]["horainicio"]
    # hora_fin = info["sensado"]["horafin"]
    # hora_media = (hora_inicio + hora_fin) / 2
    # grades = info["altura"]["grades"]
    # minutes = info["altura"]["minutes"]
    # latitud_radianes = 0.0
    # distancia_tierra_sol = 0.0
    # declinacion_solar = 0.0
    # angulo_solar_medio = 0.0
    # grados_greenwich = info["longitud"]["grados"]
    # correcion_estacional = 0.0
    # fraccion_tiempo_sensado = info["sensado"]["fraccion"]

    # if info["altura"]["orientation"] == 'N' :
    #     grades_decimal = grades + (minutes/60)
    #     latitud_radianes = round((math.pi/180) * grades_decimal, 2)
    # else:
    #     grades_decimal = grades + (minutes/60)
    #     latitud_radianes = round((math.pi/180) * grades_decimal, 2)

    #Calculamos la longitud oeste de greenwich
    # longitud_oeste_greenwith = (((info["longitud"]["segundos"] / 60) + (info["longitud"]["minutos"]))/60) + info["longitud"]["grados"]

    #Calculamos la   distancia relativa inversa Tierra-Sol(formula 23)
    distancia_tierra_sol = 1 + 0.033 * math.cos((2*math.pi*julian_day())/365)
    
    #Calculamos la declinación solar (formula 24)
    declinacion_solar = 0.409 * math.sin(((2*math.pi*julian_day())/365) - 1.39)
    
    #Calculamos el angulo solar en el punto medio del periodo (ω) (formula 31)
    hora_actual = datetime.datetime.now().hour
    Lz = coordenadas['lng']['minutos']  #longitud del centro de la zona de tiempo local [grados oeste de Greenwich]
    Lm = math.fabs(ltd_lng_dec['lng']) #longitud de la zona de medición [grados oeste de Greenwich]
    #Calculamos la constante b para la correcion estacional (formula 33)
    b = (2 * math.pi * (julian_day() - 81)) / 364
    #Calculamos la correción estacional (formula 32)
    correcion_estacional = (0.1645 * math.sin(2 * b)) - (0.1255 * math.cos(b)) - (0.025 * math.sin(b))
    # ángulo solar a la hora de la puesta del sol (ωs) (formula 25)
    angulo_solar_puesta_sol = math.acos(-math.tan(ltd_lng_rad['ltd']) * math.tan(distancia_tierra_sol))
    # ángulo solar medio (ω)
    angulo_solar_medio = (math.pi / 12) * (((hora_actual + 0.5) + 0.06667 * (Lz - Lm) + correcion_estacional) - 12) 

    #Calculamos el angulo solar medio ω1 (formula 29)
    angulo_solar_medio1 = angulo_solar_medio - ((math.pi * fraccion_tiempo_sensado) / 24)
    #Calculamos el angulo solar medio ω2 (formula 30)
    angulo_solar_medio2 = angulo_solar_medio + ((math.pi * fraccion_tiempo_sensado) / 24)

    #Calculamos la radiacion extraterrestre (formula 28)
    radicion_extraterrestre = (((12*60)/ math.pi) * constante_solar * distancia_tierra_sol * (((angulo_solar_medio2 - angulo_solar_medio1) * (math.sin(ltd_lng_rad['ltd'])) * (math.sin(declinacion_solar))) + ((math.cos(ltd_lng_rad['ltd']) * math.cos(declinacion_solar) * (math.sin(angulo_solar_medio2) - math.sin(angulo_solar_medio1))))))
    return radicion_extraterrestre


horas_insolacion = (24/math.pi) * angulo_solar_puesta_sol


#Metodó para calcula la insolación maxima del día
# def insolacion_maxima(radiacion_extraterrestre):
#     return (24/math.pi) * radiacion_extraterrestre


# def radiacion_solar(radiacion_extraterrestre):


#     radiacion_onda_corta = 0.0
#     duracion_real_insolacion = 0



# def radicion_onda_corta(radiacion_extraterrestre):
#     #Calculamos la radición de onda corta, usando de referencia un albedo (formula 38)
#     return (1 - 0.23) * radiacion_extraterrestre

#Calculamos la densidad del flujo del calor del suelo (G) [MJ m-2 hora-1] (Formulas 45 y 46)
def flujo_calor_suelo(radiacion_neta):
    flujo_calor=0.0
    time_noche=datetime.datetime.strptime("18:30:00", "%H:%M:%S")
    time_dia=datetime.datetime.strptime("06:30:00", "%H:%M:%S")
    time_ahora=datetime.datetime.now()
    if time_ahora > time_dia and time_ahora < time_noche:
        flujo_calor = (0.1 * radiacion_neta) #Formula 45
        return flujo_calor
    else:
        flujo_calor = (0.5 * radiacion_neta) #Formula 46
        return flujo_calor

#Calculamos la media de los sensores (temperatura del aire (Thr), Humedad Relativa, _Velocidad del viento
def media(array_medidas_sensadas):
    media = math.fsum(array_medidas_sensadas) / len(array_medidas_sensadas)
    return media

    
#Calculamos pendiente de la curva de presión de saturación de vapor en Thr (∆)[kPa °C-1] (Formula 13)
def pendiente_presion_saturacion_vapor(temperatura_media):
    pendiente = (4098 * presion_saturacion_vapor(temperatura_media)) / math.pow(temperatura_media + 237.3 , 2)
    return pendiente

#Calculamos la constante psicrométrica [kPa °C-1] (Formula 8),
def constante_psicrometrica(z):
    #Se calcula la presion atmosferica [kPa] donde z = altura sobre el nivel de mar
    presion_atmosferica = 101.3 * math.pow(((293 - (0.0065 * z)) / 293) , 5.26 ) 
    calor_especifico = 1.013 * math.pow(10, -3) #calor específico a presión constante (Cp) [ MJ kg-1 °C-1], 
    peso_vapor = 0.622 #cociente del peso molecular de vapor de agua /aire seco (E)
    calor_latente = 2.45 #calor latente de vaporización[ MJ kg-1] 
    const_psicrometrica = (calor_especifico * presion_atmosferica) / (peso_vapor * calor_latente)
    return const_psicrometrica

#presión de saturación de vapor a temperatura del aire Thr [kPa]  (e°(Thr) ) (Formula 11),
def presion_saturacion_vapor(temperatura_media): 
    presion = 0.6108 * math.exp((17.27 * temperatura_media) / (temperatura_media + 237.3))
    return presion

#Calculamos promedio horario de la presión real de vapor [kPa] (Formula 54)
def presion_real_vapor(presion_saturacion_vapor, humedad_media):
    presion_real = presion_saturacion_vapor * (humedad_media / 100)
    return presion_real


