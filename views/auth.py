from . import auth_bp
from flask import Flask, request, render_template, jsonify,abort
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import connections

mongo = connections.get_mongo_db()

@auth_bp.route('/login', methods = ['POST'])
@cross_origin()
def login():

    data = request.get_json()
    email = data['email']
    password = data['password']
    
    user = mongo['users'].find_one({"email": email, "password": password, "status": True})

    if not user:
         return abort(404)
    
    result = {'name': user['name'], 'email': user['email']}

    return jsonify(result)


@auth_bp.route('/createuser', methods = ['POST'])
@cross_origin()
def create_user():
     
    data = request.get_json()

    user = {
        "name": data['name'],
        "email": data['email'],
        "password": data['password'],
        "location": data['location'],
        "status": True
    }

    user_inserted = mongo['users'].insert_one(user)

    return jsonify({'message': 'Usuario creado', 'inserted_id': str(user_inserted.inserted_id)})



    

