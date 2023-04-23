import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["weather_project"]

db_data_collections = mydb['weather_variables']
db_configuration_collections = mydb['configuration_station']



