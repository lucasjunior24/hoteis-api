from flask_restful import Resource, reqparse
from models.site import SiteModel
from flask_jwt_extended import jwt_required


class Sites(Resource):
    def get(self):
        query = SiteModel.query
        return {"sites": [site.json() for site in query.all()], "total": len(query.all())}

class Site(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("url", type=str, required=True, help="The field 'url' cannot be left blank.")


    def get(self, name):
        site = SiteModel.find_site(name)
        if site:
            return site.json()
        return {"message": "Site not found."}, 404 #not found


    # @jwt_required()
    def post(self, name):
        if SiteModel.find_site(name):
            return {"message": f"The Site '{name}' already exists."}, 400
        dados = self.argumentos.parse_args()
        site = SiteModel(name, **dados)
        try:
            site.save_site()
        except:
            return {"message": "An internal error ocurred trying to save site."}, 500
        return site.json(), 201


    # @jwt_required()
    def delete(self, name):
        site = SiteModel.find_site(name)
        if site:
            try:
                site.delete_site()
            except:
                return {"message": "An internal error ocurred trying to save site."}, 500
            return {"message": "Hotel deleted."}
        return {"message": "Hotel not found."}, 404