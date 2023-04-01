from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

class HoteisFiltro(Resource):
    # def get(self):
    #     return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}
    path_params = reqparse.RequestParser()
    path_params.add_argument("cidade",type=str, default="", location="args")
    path_params.add_argument("estrelas_min",type=float, default=0, location="args")
    path_params.add_argument("estrelas_max",type=float, default=99999, location="args")
    path_params.add_argument("diaria_min",type=float, default=0, location="args")
    path_params.add_argument("diaria_max",type=float, default=99999999999, location="args")
    path_params.add_argument("page",type=float, default=1, location="args")
    path_params.add_argument("per_page",type=float, default=100, location="args")
    path_params.add_argument('limit', type=float, location='args')
    path_params.add_argument('offset', type=float, location='args')
    def get(self, cidade):
        filters  = self.path_params.parse_args()

        query = HotelModel.query.filter(HotelModel.cidade == cidade)
        if filters["estrelas_min"]:
            query = query.filter(HotelModel.estrelas >= filters["estrelas_min"])
        if filters["estrelas_max"]:
            query = query.filter(HotelModel.estrelas <= filters["estrelas_max"])
        if filters["diaria_min"]:
            query = query.filter(HotelModel.diaria >= filters["diaria_min"])
        if filters["diaria_max"]:
            query = query.filter(HotelModel.diaria <= filters["diaria_max"])
        if filters["limit"]:
            query = query.limit(filters["limit"])
        if filters["offset"]:
            query = query.offset(filters["offset"])
        # hoteis = HotelModel.query.filter(
        #     HotelModel.estrelas > dados["estrelas_min"], 
        #     HotelModel.estrelas < dados["estrelas_max"]).paginate(
        #         page=dados["page"], per_page=dados["per_page"]
        #     )
        return {"hoteis": [hotel.json() for hotel in query]}

        
class Hoteis(Resource):
    # def get(self):
    #     return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}
    path_params = reqparse.RequestParser()
    path_params.add_argument("cidade",type=str, default="", location="args")
    path_params.add_argument("estrelas_min",type=float, default=0, location="args")
    path_params.add_argument("estrelas_max",type=float, default=99999, location="args")
    path_params.add_argument("diaria_min",type=float, default=0, location="args")
    path_params.add_argument("diaria_max",type=float, default=99999999999, location="args")
    path_params.add_argument("page",type=float, default=1, location="args")
    path_params.add_argument("per_page",type=float, default=100, location="args")
    path_params.add_argument('limit', type=float, location='args')
    path_params.add_argument('offset', type=float, location='args')
    def get(self):

        filters  = self.path_params.parse_args()
        query = HotelModel.query
        if filters["cidade"]:
            query = query.filter(HotelModel.cidade == filters["cidade"])
        if filters["estrelas_min"]:
            query = query.filter(HotelModel.estrelas >= filters["estrelas_min"])
        if filters["estrelas_max"]:
            query = query.filter(HotelModel.estrelas <= filters["estrelas_max"])
        if filters["diaria_min"]:
            query = query.filter(HotelModel.diaria >= filters["diaria_min"])
        if filters["diaria_max"]:
            query = query.filter(HotelModel.diaria <= filters["diaria_max"])
        if filters["limit"]:
            query = query.limit(filters["limit"])
        if filters["offset"]:
            query = query.offset(filters["offset"])
        
        if filters["page"]:
            query = query.paginate(
                page=filters["page"], per_page=filters["per_page"]
            )
        hoteis = [hotel.json() for hotel in query]
        return {"hoteis": hoteis, "total": query.total}
   
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