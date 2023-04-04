from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import hmac


from blacklist import BLACKLIST
from models.user import UserModel


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {"message": "User not found."}, 404 #not found
    

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {"message": "An internal error ocurred trying to save user."}, 500
            return {"message": "User deleted."}
        return {"message": "User not found."}, 404
    
class UserRegister(Resource):
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument("nome", type=str, required=True, help="The field 'nome' cannot be left blank.")
        atributos.add_argument("email", type=str, required=True, help="The field 'e-mail' cannot be left blank.")
        atributos.add_argument("senha", type=str, required=True, help="The field 'senha' cannot be left blank.")
        dados = atributos.parse_args()

        if UserModel.find_by_email(dados["email"]):
            return {"message": "The User with e-mail '{}' already exists.".format(dados["email"])}, 404 #not found
        user = UserModel(**dados)
        try:
            user.save_user()
        except:
            return {"message": "An internal error ocurred trying to save user."}, 500
        return {"message": "User created successefully."}, 201
    

class UserLogin(Resource):
    @classmethod
    def post(cls):
        atributos = reqparse.RequestParser()
        atributos.add_argument("email", type=str, required=True, help="The field 'e-mail' cannot be left blank.")
        atributos.add_argument("senha", type=str, required=True, help="The field 'senha' cannot be left blank.")
        dados = atributos.parse_args()

        user = UserModel.find_by_email(dados["email"])
        if user and hmac.compare_digest(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {"acess_toekn": token_de_acesso}, 200 #not found
        return {"message": "The username or password is incorrect."}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_token = get_jwt()['jti']
        BLACKLIST.add(jwt_token)

        return {"message": "Logged out successefully."}, 200
