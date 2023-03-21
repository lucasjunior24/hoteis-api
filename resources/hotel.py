from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        "hotel_id": "alpha",
        "nome": "Alpha Hotel",
        "estrelas": 4.4,
        "diaria": 320.34,
        "cidade": "Santa Catarina"
    },
    {
        "hotel_id": "bravo",
        "nome": "Alpha Hotel",
        "estrelas": 4.4,
        "diaria": 320.34,
        "cidade": "Santa Catarina"
    }
]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}
    

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome")
    argumentos.add_argument("estrelas")
    argumentos.add_argument("diaria")
    argumentos.add_argument("cidade")


    def find_hotel(self, hotel_id):
        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return hotel
            
        return None
    

    def get(self, hotel_id):
        hotel = self.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {"message": "Hotel not found."}, 404 #not found

    def post(self, hotel_id):
        dados = self.argumentos.parse_args()
        hotel_object = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_object.json()
        hoteis.append(novo_hotel)
        return novo_hotel, 200

    def put(self, hotel_id):
        dados = self.argumentos.parse_args()
        hotel_object = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_object.json()
        hotel = self.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 201
        
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel["hotel_id"] != hotel_id]
        return {"message": "Hotel deleted."}
    