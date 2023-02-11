import boto3
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin


#item variables

#Creamos el client para conectaser a dynamodb
dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')
table = dynamodb.Table('Station')

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def main():
    return render_template('swaggerui.html')


#TODO: debe recibir la informacion mediante protocolo https:POST
@app.route('/Inserted', methods = ['POST'])
@cross_origin()
def insert_records():
    if request.method == 'POST':
        x = request.get_json()
        print(type(x))
    
        #Inserted data on table on dynamodb
        resp = table.put_item(Item = x)
        return resp


@app.route('/get', methods = ['GET'])
@cross_origin()
def get_items():
    response = table.scan()
    data = response['Items']
    # print(data)
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    print(type(data))
    return data


if __name__ == '__main__':

    app.debug = True
    app.run(host="0.0.0.0")








