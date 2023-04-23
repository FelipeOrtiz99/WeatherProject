from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
import db_context as db
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/weather_project' 
mongo = PyMongo(app)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def main():
    return render_template('swaggerui.html')

@app.route('/Inserted', methods=['POST'])
@cross_origin()
def create():
    item = {}
    for data in request.json:
        item = {
        'date': datetime.now(),
        "grades": data["grades"],
        'hour': data['hour'],
        'humidity': data['humidity'],
        'julian_day': data['julian_day'],
        'latitude': data['latitude'],
        'temperature': data['temperature']
         }   
        mongo.db.weather_variables.insert_one(item)

    result = {'message': 'Registro creado exitosamente'}
    return jsonify(result)


@app.route('/get', methods=['GET'])
@cross_origin()
def get_all():
    items = mongo.db.weather_variables.find()
    result = []
    for item in items:
        result.append({'_id': str(item['_id']), 'date': item['date'],'grades': item['grades'], 'hour': item['hour'], 'humidity':item['humidity'], 'julian_day': item['julian_day'], 'latitude': item['latitude'], 'temperature': item['temperature']}) 
    return jsonify(result)


@app.route('/get/<id>', methods=['GET'])
@cross_origin
def get_one(id):
    item = mongo.db.weather_variables.find_one({'_id': ObjectId(id)})
    if item:
        result = {'_id': str(item['_id']), 'date': item['date'],'grades': item['grades'], 'hour': item['hour'], 'humidity': item['humidity'], 'julian_day': item['julian_day'], 'latitude': item['latitude'], 'temperature': item['temperature']} 
    else:
        result = {'message': 'Registro no encontrado'}
    return jsonify(result)

@app.route('/getbydate', methods=['GET'])
@cross_origin()
def filtrar_fecha():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    # Convertir las fechas de texto a objetos datetime
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

    # Filtrar los documentos que tienen una fecha dentro del rango
    resultados = mongo.db.weather_variables.find({"date": {"$gte": fecha_inicio, "$lte": fecha_fin}})

    # Crear una lista con los resultados y convertirla a JSON
    documents = []
    for resultado in resultados:
        documents.append(resultado)
    return jsonify(documents)


if __name__ == '__main__':

    app.debug = True
    app.run(host="0.0.0.0")








