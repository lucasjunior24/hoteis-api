from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3


def normalize_path_params(cidade=None, 
                          estrelas_min = 0, 
                          estrelas_max = 5, 
                          diaria_min = 0,
                          diaria_max = 10000,
                          limit = 50,
                          offset = 0, **dados):
    if cidade:
        return {
                    'estrelas_min': estrelas_min,
                    'estrelas_max': estrelas_max,
                    'diaria_min': diaria_min,
                    'diaria_max': diaria_max,
                    'cidade': cidade,
                    'limit': limit,
                    'offset': offset
                }
    return {
                'estrelas_min': estrelas_min,
                'estrelas_max': estrelas_max,
                'diaria_min': diaria_min,
                'diaria_max': diaria_max,
                'limit': limit,
                'offset': offset
            }




class Hoteis(Resource):
    # def get(self):
    #     return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}
    params = reqparse.RequestParser()
    params.add_argument('cidade', type=str, location='args')
    params.add_argument('estrelas_min', type=float, location='args')
    params.add_argument('estrelas_max', type=float, location='args')
    params.add_argument('diaria_min', type=float, location='args')
    params.add_argument('diaria_max', type=float, location='args')
    params.add_argument('limit', type=float, location='args')
    params.add_argument('offset', type=float, location='args')
    def get(self):
        connection = sqlite3.connect('banco2.db')
        cursor = connection.cursor()
        
        dados = self.params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            consulta = "SELECT * FROM hoteis\
            WHERE (estrelas >= ? and estrelas <= ?) \
            and (diaria >= ? and diaria <= ?) \
            LIMIT ? OFFSET ?"

            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)

        else:
            consulta = "SELECT * FROM hoteis\
            WHERE (estrelas >= ? and estrelas <= ?) \
            and (diaria >= ? and diaria <= ?) \
            and cidade = ? LIMIT ? OFFSET ?"

            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
            "hotel_id": linha[1],
            "nome": linha[2],
            "estrelas": linha[3],
            "diaria": linha[4],
            "cidade": linha[5]
        })

        return {'hoteis': hoteis}
    

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="The field 'name' cannot be left blank.")
    argumentos.add_argument("estrelas", type=float, required=True, help="The field 'estrelas' cannot be left blank.")
    argumentos.add_argument("diaria")
    argumentos.add_argument("cidade")


    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "Hotel not found."}, 404 #not found


    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel id '{hotel_id}' already exists."}, 400
        dados = self.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500
        return hotel.json(), 201


    @jwt_required()
    def put(self, hotel_id):
        dados = self.argumentos.parse_args()
        hotel_model = HotelModel.find_hotel(hotel_id)
        if hotel_model:
            hotel_model.update_hotel(**dados)
            try:
                hotel.save_hotel()
            except:
                return {"message": "An internal error ocurred trying to save hotel."}, 500
            return hotel_model.json(), 200
        
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500
        return hotel.json(), 201


    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {"message": "An internal error ocurred trying to save hotel."}, 500
            return {"message": "Hotel deleted."}
        return {"message": "Hotel not found."}, 404