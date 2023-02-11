#Insertar masivamente
import boto3
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import uuid
from decimal import Decimal
import json


#item variables

#Creamos el client para conectaser a dynamodb
dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')
table = dynamodb.Table('Station')


a = [
  {'fecha':'2022-08-21','hora':'17:00','temp':28.5,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-08-22','hora':'17:00','temp':28.9,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-08-23','hora':'17:00','temp':28.11,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-08-24','hora':'17:00','temp':28.3,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-08-25','hora':'17:00','temp':28.2,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-08-26','hora':'17:00','temp':28.6,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-08-27','hora':'17:00','temp':28.1,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-08-28','hora':'17:00','temp':28.11,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-08-29','hora':'17:00','temp':28.9,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-08-30','hora':'17:00','temp':28,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-08-31','hora':'17:00','temp':28,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-09-01','hora':'17:00','temp':28,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-09-02','hora':'17:00','temp':28,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-09-03','hora':'17:00','temp':28,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-09-04','hora':'17:00','temp':28,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-09-05','hora':'17:00','temp':28,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-09-06','hora':'17:00','temp':28,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-09-07','hora':'17:00','temp':27,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-09-08','hora':'17:00','temp':28,'hum':30,'rad':15,'vel':5,'eto':6},
  {'fecha':'2022-09-08','hora':'17:00','temp':28,'hum':30,'rad':15,'vel':5,'eto':7},  
]

def insert_records():

    for item in a:
        identifier = str(uuid.uuid1())
        item.update({'id':identifier})
        item = json.loads(json.dumps(item), parse_float=Decimal)
        resp = table.put_item(Item = item)
        print(item)



insert_records()
    # #Inserted data on table on dynamodb
    # resp = table.put_item(Item = x)
    # return resp
