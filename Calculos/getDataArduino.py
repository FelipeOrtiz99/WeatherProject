import serial
import time
import requests
from Calculos import calculoEto,radiacion_extraterrestre,radiacion_solar,N

serialArduino = serial.Serial("COM4",9600)
time.sleep(1)

def EnviarData(data):
    url = "http://ec2-50-18-36-25.us-west-1.compute.amazonaws.com:5000/" 

    response = requests.post(url, json=data)

    # Verificar el estado de la respuesta
    if response.status_code == 200:  # El código 200 indica éxito en la solicitud
        print("Solicitud POST exitosa")
        print("Respuesta:", response.json())  # La respuesta de la API en formato JSON
    else:
        print("Error en la solicitud POST. Código de estado:", response.status_code)
        
while serialArduino.is_open:
    cadena = serialArduino.readline().decode('ascii')
    objVariables = {}
    if cadena != '' and cadena != None:
        arrayVariables = cadena.split(' ')
        for variable in arrayVariables:
            valor = variable.split(':')
            objVariables[valor[0]] = list(map(float, valor[1].split(',')))
        arrayVariables = calculoEto(arrayVariables)
        
        EnviarData(arrayVariables)


# while serialArduino.is_open:
#     cadena = serialArduino.readline().decode('ascii')
#     objVariables = {}
#     if cadena != '' and cadena != None:
#         if 'eto' in cadena:    
#             arrayVariables = cadena.split(' ')
#             for variable in arrayVariables:
#                 valor = variable.split(':')
#                 if valor[0] == 'eto':
#                     objVariables[valor[0]] = valor[1]
#                     continue
#                 objVariables[valor[0]] = valor[1].split(',')
#             arrayVariables = calculoEto(arrayVariables)
#         else:
#             arrayVariables = cadena.split(' ')
#             for variable in arrayVariables:
#                 valor = variable.split(':')
#                 if valor[0] == 'rad':
#                     rExt = radiacion_extraterrestre(0.083)
#                     insolacionMax = N * 0.083
#                     insolacion = int(valor[1]) / 3600
#                     rSolar = radiacion_solar(rExt,insolacionMax,insolacion)
#                     objVariables[valor[0]] = rSolar
#                     continue
#                 objVariables[valor[0]] = float(valor[1])
        
#         EnviarData(arrayVariables)
        


