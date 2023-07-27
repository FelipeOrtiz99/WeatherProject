from flask import Flask
from views.auth import auth_bp
from views.station import station_bp


app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(station_bp)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")








