from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

app = Flask(__name__)
app.config["SQL_ALCHEMY_DATABASE_URI"] = 'sqlite:///banco.db'
api = Api(app)

@app.brefore_first_request
def cria_banco():
    banco.create_all()

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')



if __name__ == "__main__":
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)