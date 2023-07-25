#Calculo de la Eto
from ast import Import, parse
from cmath import pi, tan
import json as js
import math
import datetime



array_temperaturas = [38,38] # °C
array_humedad = [52,52] # %
array_velocidad_viento = [3.3,3.3]
hora_actual = datetime.datetime.now().hour
año_actual = datetime.datetime.now().year
mes_actual = 10
coordenadas = {'ltd':{'grados':16,'minutos':13,'segundos':0,'orientacion':'N'},
                   'lng':{'grados':16,'minutos':15,'segundos':0,'orientacion':'W'}
                   }
#Datos promedios de horas reales de insolacion de la ciudad de Neiva, referencia:atlas.ideam.gov.co/visorAtlasRadiacion.html
insolacion_real ={'1':6.5,'2':5.5,'3':4.5,'4':4.5,'5':5.5,'6':5.5,'7':5.5,
                  '8':5.5,'9':5.5,'10':8.5,'11':5.5,'12':5.5}
altura = 8 # altura sobre el nivel del mar de la ciudad de Neiva


def sexagesimal_decimal(coordenadas):
    grados_ltd = coordenadas['ltd']['grados']
    minutos_ltd = coordenadas['ltd']['minutos']
    segundos_ltd = coordenadas['ltd']['segundos']
    orientacion_ltd= coordenadas['ltd']['orientacion']
    grados_lng = coordenadas['lng']['grados']
    minutos_lng = coordenadas['lng']['minutos']
    segundos_lng  = coordenadas['lng']['segundos']
    orientacion_lng = coordenadas['lng']['orientacion']
    ltd = grados_ltd + (minutos_ltd / 60) + (segundos_ltd / 60)
    ltd = ltd if (orientacion_ltd == 'N') else -ltd
    
    lng = grados_lng + (minutos_lng / 60) + (segundos_lng / 60)
    lng = lng if (orientacion_lng == 'E') else -lng
    return {'ltd':ltd, 'lng':lng}

def decimal_radianes(coordenadas):
    ltd = coordenadas['ltd'] * math.pi/180
    lng = coordenadas['lng'] * math.pi/180
    return {'ltd':ltd, 'lng':lng}

def julian_day():
    today = datetime.datetime.now()
    julian = (today - datetime.datetime(today.year,1,1)).days + 1
    return julian

#Calculamos la radiacion extraterrestres para periodos horarios (Ra) (Formula 28)
def radiacion_extraterrestre():
    constante_solar = 0.082 # MJ m^(-2) min^(-1)
    julian = 274
    global angulo_solar_puesta_sol
    
    ltd_lng_dec = sexagesimal_decimal(coordenadas)
    ltd_lng_rad= decimal_radianes(ltd_lng_dec)
    fraccion_tiempo_sensado = 1 # duración del periodo considerado [horas]


    #Calculamos la   distancia relativa inversa Tierra-Sol(formula 23)
    distancia_tierra_sol = 1 + (0.033 * math.cos((2*math.pi*julian)/365))
    
    #Calculamos la declinación solar (formula 24)
    declinacion_solar = 0.409 * math.sin(((2*math.pi*julian)/365) - 1.39)
    
    #Calculamos el angulo solar en el punto medio del periodo (ω) (formula 31)
    Lz = 15  #longitud del centro de la zona de tiempo local (Colombia) [grados oeste de Greenwich]
    Lm = math.fabs(ltd_lng_dec['lng']) #longitud de la zona de medición (Neiva) [grados oeste de Greenwich]
    #Calculamos la constante b para la correcion estacional (formula 33)
    b = (2 * math.pi * (julian - 81)) / 364
    #Calculamos la correción estacional (formula 32)
    correcion_estacional = (0.1645 * math.sin(2 * b)) - (0.1255 * math.cos(b)) - (0.025 * math.sin(b))
    # ángulo solar a la hora de la puesta del sol (ωs) (formula 25)
    angulo_solar_puesta_sol = math.acos(-math.tan(ltd_lng_rad['ltd']) * math.tan(declinacion_solar))
    # ángulo solar medio (ω)
    angulo_solar_medio = (math.pi / 12) * (((14 + 0.5) + 0.06667 * (Lz - Lm) + correcion_estacional) - 12) 
    
    if angulo_solar_medio < -angulo_solar_puesta_sol or angulo_solar_medio > angulo_solar_puesta_sol :
        return 0
    
    #Calculamos el angulo solar medio ω1 (formula 29)
    angulo_solar_medio1 = angulo_solar_medio - ((math.pi * fraccion_tiempo_sensado) / 24)
    #Calculamos el angulo solar medio ω2 (formula 30)
    angulo_solar_medio2 = angulo_solar_medio + ((math.pi * fraccion_tiempo_sensado) / 24)

    #Calculamos la radiacion extraterrestre (formula 28)
    radicion_extraterrestre = (((12*60)/ math.pi) * constante_solar * distancia_tierra_sol * (((angulo_solar_medio2 - angulo_solar_medio1) * (math.sin(ltd_lng_rad['ltd'])) * (math.sin(declinacion_solar))) + ((math.cos(ltd_lng_rad['ltd']) * math.cos(declinacion_solar) * (math.sin(angulo_solar_medio2) - math.sin(angulo_solar_medio1))))))
    return radicion_extraterrestre



#Calculo de radiacion solar (Rs) (Formula 35) Formula de Angstrom
As = 0.25  #Constantes de regresion para nublados y despejados
bs = 0.5 
def radiacion_solar(radiacion_extraterrestre, max_insolacion):
    As = 0.25  #Constantes de regresion para nublados y despejados
    bs = 0.5 
    n = insolacion_real[str(mes_actual)] #horas reales de insolacion
    N = max_insolacion #horas maximas de insolacion
    Rs = (As + bs * n/N) * radiacion_extraterrestre
    return Rs

#Calculo de radiacion solar de un dia despejado (Rso) (Formula 37)
def radiacion_solar_despejado(radiacion_extraterrestre, altura):
    Rso = (0.75 + (2 * math.pow(10,-5) * altura)) * radiacion_extraterrestre
    return Rso

#Calculo de radiacion neta solar o de onda corta (Rns) (Formula 38)
def radiacion_neta_corta(radiacion_solar):
    #0.23=coeficiente de reflexion del cultivo hipotetico de referencia 
    Rns = (1 - 0.23) * radiacion_solar
    return Rns

#Calculo de radiacion neta de onda larga (Rnl) (Formula 39)
def radiacion_neta_larga(temperatura_media,radiacion_solar,radiacion_solar_despejado,presion_real_vapor):
    constStefan = 2.043 * math.pow(10,-10) #constante de Stefan-Boltzmann
    ea = presion_real_vapor#Presion real del vapor (presion_saturacion_vapor, humedad_media)
    Rs = radiacion_solar#Radiacion solar(radiacion_extraterrestre)
    Rso = radiacion_solar_despejado#radiacion solar de un dia despejado(radiacion_extraterrestre, altura)
    if (Rs == 0.0 and Rso == 0.0):
        if (presion_real_vapor > 3.16):
            R = 0.75 #valor de relacion de nubosidad en horas de la noche para climas humedos 
        elif (presion_real_vapor > 1.7):
            R = 0.5
        else:
            R = 0.3
    else:
        R = Rs / Rso
    Rnl = constStefan * math.pow(temperatura_media + 273.16,4) * (0.34 - (0.14 * math.sqrt(ea))) * ((1.35 * (R)) - 0.35)
    return Rnl

#Calculo de Radiacion neta (Rn) (Formula 40)  
def radiacion_neta(presion_real_vapor,temperatura_media):
    Ra = radiacion_extraterrestre()
    N = (24/math.pi) * angulo_solar_puesta_sol #Horas maximas de insolacion (Formula 34)
    Rs = radiacion_solar(Ra, N)
    Rso = radiacion_solar_despejado(Ra, altura)
    Rns = radiacion_neta_corta(Rs)
    Thr = temperatura_media
    Rnl = radiacion_neta_larga(Thr,Rs,Rso,presion_real_vapor)
    return (Rns - Rnl)



#Calculamos la densidad del flujo del calor del suelo (G) [MJ m-2 hora-1] (Formulas 45 y 46)
def flujo_calor_suelo(radiacion_neta):
    flujo_calor=0.0
    time_ahora=datetime.datetime.now().time()
    time_noche=datetime.datetime.now().strptime("18:30:00", "%H:%M:%S").time()
    time_dia=datetime.datetime.now().strptime("06:30:00", "%H:%M:%S").time()
    # if time_ahora > time_dia and time_ahora < time_noche:
    flujo_calor = (0.1 * radiacion_neta) #Formula 45
    return flujo_calor
    # else:
    #     flujo_calor = (0.5 * radiacion_neta) #Formula 46
    #     return flujo_calor

#Calculamos la media de los sensores (temperatura del aire (Thr), Humedad Relativa, _Velocidad del viento
def media(array_medidas_sensadas):
    media = math.fsum(array_medidas_sensadas) / len(array_medidas_sensadas)
    return media

    
#Calculamos pendiente de la curva de presión de saturación de vapor en Thr (∆)[kPa °C-1] (Formula 13)
def pendiente_presion_saturacion_vapor(presion_saturacion_vapor,temperatura_media):
    pendiente = (4098 * presion_saturacion_vapor) / math.pow(temperatura_media + 237.3 , 2)
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


def calculoEto():
    r = constante_psicrometrica(altura)
    Thr = media(array_temperaturas)
    u2 = media(array_velocidad_viento)
    HRhr = media(array_humedad)
    eThr = presion_saturacion_vapor(Thr)
    ea = presion_real_vapor(eThr,HRhr)
    A = pendiente_presion_saturacion_vapor(eThr,Thr)
    Rn = radiacion_neta(ea,Thr)
    G = flujo_calor_suelo(Rn)
    
    ETo = (0.408*A*(Rn-G))/( A + r*(1+(0.34*u2))) + (r*(37/(Thr+273))*u2*(eThr-ea))/ (A + r*(1+(0.34*u2)))    
    return ETo

calculoEto()