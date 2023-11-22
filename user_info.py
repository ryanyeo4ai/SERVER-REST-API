from flask import Flask, request
from flask_cors import CORS
import jwt
import bcrypt
from flask_restx import Resource, Api, Namespace, fields
from db_connect import *

app = Flask(__name__)
CORS(app)

#users = {}
users_info = get_all_user_info_from_db()

UserInfo = Namespace(
    name="Info",
    description="사용자 정보 및 학교 정보 조회를 위한 API",
)

user_info_fields = UserInfo.model('User', {  # Model 객체 생성
    'email': fields.String(description='email address', required=True, example="ryan@gmail.com")
})

user_fields_auth = UserInfo.inherit('User Auth', user_info_fields, {
    'password': fields.String(description='Password', required=True, example="password")
})

jwt_fields = UserInfo.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})


# @api.route('/login') #100870 #OK
# @api.doc(params={'email': 'user email', 'password' : 'user password'})
# class login(Resource):
#     def post(self):
#         param = request.get_json()
#         print(f'response json : {param}')
#         for key in param:
#             if key == "email":
#                 print(f'email : {param["email"]}')
#                 user_email = param["email"]
#             elif key == "password":
#                 print(f'password : {param["password"]}')
#                 user_passwd = param["password"]

#         check_user = True #  DB에 아이디 비번 탐색하고 로그인진행하는 과정
#         jwt_token = jwt.encode(param, app.config['JWT_SECRET_KEY'], algorithm)
#         check_user = check_password(user_email, user_passwd)
#         if check_user :
#             return jsonify(jwt_token.decode('utf-8'))
#         else:
#             return jsonify('fail')

           
# @api.route('/create_user') #OK
# @api.doc(params={'email': 'user email', 'password' : 'user password'})
# class create_user(Resource):
#     def post(self):
#         param = request.get_json()
#         print(f'response json : {param}')
#         for key in param:
#             if key == "email":
#                 print(f'email : {param["email"]}')
#                 user_email = param["email"]
#             elif key == "password":
#                 print(f'password : {param["password"]}')
#                 user_passwd = param["password"]
#         pw_hash = bcrypt.generate_password_hash(user_passwd)
        
#         if insert_user_db(user_email, pw_hash) == True:
#             return jsonify('Success !!!')
#         else:
#             return jsonify('fail')

# @api.route('/update_user_info')
# @api.doc(params={'email': 'user email', 'password' : 'user password'})
# class create_user(Resource):
#     def post(self):
#         param = request.get_json()
#         print(f'response json : {param}')
#         return param

# @api.route('/get_user_info/<string:user_email>')
# class get_user_info(Resource):
#     def get(self, user_email):
#         check_user = True #  DB에 아이디 비번 탐색하고 로그인진행하는 과정
#         check_user, user_info = check_user_email(user_email)
#         if check_user :
#             return user_info
#         else:
#             return jsonify('fail')


# @api.route('/school_code/<int:school_code>') #100870
# class school_code(Resource):
#     def get(self, school_code):
#         check_schoo_code = True #  DB에 아이디 비번 탐색하고 로그인진행하는 과정
#         check_schoo_code = check_school_code(school_code)
#         if check_schoo_code :
#             return jsonify('Success !!!')
#         else:
#             return jsonify('fail')

#     # def put(self, member_id):
#     #     school[member_id] = request.json.get('data')
#     #     return {
#     #         'member_id': member_id,
#     #         'data': school[member_id]
#     #     }
    
#     # def delete(self, member_id):
#     #     del school[member_id]
#     #     return {
#     #         "delete" : "success"
#     #     }
# @api.route('/school_name/<string:school_name>')
# class school_name(Resource):
#     def get(self, school_name):
#      def get(self, school_name):
#         check_schoo_name = True #  DB에 아이디 비번 탐색하고 로그인진행하는 과정
#         check_schoo_name = check_school_code(school_name)
#         if check_schoo_name :
#             return jsonify('Success !!!')
#         else:
#             return jsonify('fail')


# @app.route('/echo_call/<param>') #get echo api
# def get_echo_call(param):
#     return jsonify({"param": param})

# @app.route('/echo_call', methods=['POST']) #post echo api
# def post_echo_call():
#     param = request.get_json()
#     print(param)
#     for key in param:
#         if key == "email":
#             print(f'email : {param["email"]}')
#         elif key == "password":
#             print(f'password : {param["password"]}')
#     return jsonify(param)