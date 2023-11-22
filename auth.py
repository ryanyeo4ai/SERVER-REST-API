from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import jwt
import bcrypt
from flask_restx import Resource, Api, Namespace, fields
from datetime import datetime
from datetime import timedelta
import time
from db_connect import *
from otp import *
from timestamp import *

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

# mail.init_app(app)

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'paul.yeo94@gmail.com'
# app.config['MAIL_PASSWORD'] = 'kissme!004'
# app.config['MAIL_USER_TLS'] = False
# app.config['MAIL_USER_SSL'] = True
# mail = Mail(app)

users_info = get_all_user_info_from_db()
users_token = {}
users_expiration_time = {}
created_otp = {}

Auth = Namespace(
    name="Auth",
    description="사용자 관리를 위한 API",
)


user_fields = Auth.model('User', {  # Model 객체 생성
    'email': fields.String(description='email address', required=True, example="ryan@gmail.com")
})

user_reward_fields = Auth.model('User', {  # Model 객체 생성

})

user_token_fields = Auth.model('User Token', {
    'token': fields.String(description='put autorization token into HTTP header', required=True, example="XXXXXX")
})

user_fields_auth = Auth.inherit('User Auth', user_fields, {
    'password': fields.String(description='Password', required=True, example="password")
})

user_fields_paypal_venmo = Auth.inherit('User Auth', user_fields, {
    'p_account': fields.String(description='paypal account', required=True, example="xxx@xxx.xxx"),
    'v_account': fields.String(description='venmo account', required=True, example="xxx-xxx-xxxx")
})

user_fields_req_reward_admin = Auth.inherit('User Auth', user_fields, {
    'p_account': fields.String(description='paypal account', required=True, example="xxx@xxx.xxx"),
    'v_account': fields.String(description='venmo account', required=True, example="xxx-xxx-xxxx"),
    'reward': fields.String(description='grade', required=True, example="5")
})

user_payment_request_history = Auth.model('User Token', {
    'token': fields.String(description='put autorization token into HTTP header', required=True, example="XXXXXX")
})

user_payment_request_history_by_email = Auth.model('User Token', {
    'token': fields.String(description='put autorization token into HTTP header', required=True, example="XXXXXX")
})

user_fields_pin_auth = Auth.inherit('User Pin', user_fields_auth, {
    'pin': fields.String(description='PIN CODE', required=True, example="123456")
})

jwt_fields = Auth.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})

user_info_fields_auth = Auth.inherit('User Info', jwt_fields, {
    'role': fields.String(description='role', required=True, example="student : 0, solver : 1, both : 2"),
    'grade': fields.String(description='grade', required=True, example="11"),
    'schoolName': fields.String(description='School Name', required=True, example="Albertville Middle School"),
    'schoolCode': fields.String(description='School Code', required=True, example="100870")
})

user_info_fields_auth_v2 = Auth.inherit('User Info', jwt_fields, {
    'role': fields.String(description='role', required=True, example="student : 0, solver : 1, both : 2"),
    'nickname': fields.String(description='nickname', required=True, example="Tiger"),
    'grade': fields.String(description='grade', required=True, example="11"),
    'schoolName': fields.String(description='School Name', required=True, example="Albertville Middle School"),
    'schoolCode': fields.String(description='School Code', required=True, example="100870")
})

# @Auth.route('/send_email')
# class send_email(Resource):
#     @Auth.expect(user_fields)
#     @Auth.doc(responses={200: 'Return sent email'})
#     def post(self):

#         data = request.data
#         params = json.loads(data)
#         num_params = len(params)
#         required_params = 1
#         if num_params < required_params:
#             return {
#                 "message": "lack of parameters",
#                 "return_code": "0"
#             }, 200

#         email = request.json['email']
#         otp_data = generate_otp()
#         msg = Message('SOLPLE Register PIN CODE',
#                       sender='paul.yeo94@gmail.com', recipients=[email])        # 메일 세팅
#         msg.body = 'This email address is verified ' + otp_data         # text body
#         # msg.html = '<H1> CODE : ' + otp_data + '</H1>'        # html body
#         # msg.html = '<a href= "solple://user/create?pin=' + otp_data + '">CODE</a>'
#         # msg.html = 'solple://user/create?pin=' + otp_data
#         # msg.html = 'solple://user/create?pin='+otp_data
#         mail.send(msg)      # 메일 발송
#         return {
#             "message": "Sent email",
#             "return_code": "1",
#             "code": created_otp
#         }, 200


@Auth.route('/verify_email')
class verify_email(Resource):
    @Auth.expect(user_fields)
    @Auth.doc(responses={200: 'Return Check Verified email'})
    def post(self):
        global created_otp

        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 1
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        users_info = get_all_user_info_from_db()
        print(f'users_info : {users_info}')
        email = request.json['email']
        created_otp["OTP"] = generate_otp()  # email
#        if email in users_info:
        return {
            "message": "Sent email",
            "return_code": "1",
            "code": created_otp
        }, 200
        # else:
        #     return {
        #         "message": "Not Verified email",
        #         "return_code" : "0"
        #     }, 200


@Auth.route('/reward')
class user_reward(Resource):
    @Auth.expect(user_reward_fields)
    @Auth.doc(responses={200: 'Return Check Verified email'})
    def post(self):
        users_reward_info_list = []
        users_reward_info_list = get_user_reward_from_db()
        print(f'users_info : {users_reward_info_list}')

        return {
            "reward list": users_reward_info_list
        }, 200


@Auth.route('/register')
class AuthRegister(Resource):
    @Auth.expect(user_fields_pin_auth)
    @Auth.doc(responses={200: 'Return Register Status'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 2
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        users_info = get_all_user_info_from_db()
        email = request.json['email']
        password = request.json['password']
        pin_no = request.json['pin']

        if email in users_info:
            return {
                "message": "[ Register Failed ] the email already exists",
                "return_code": "0"
            }, 200
        else:
            # if pin_no != created_otp["OTP"]:
            #     return {
            #         "message": " [ Register Failed ] PIN CODE doen't match",
            #         "return_code" : "1"
            #     }, 200
            # else:
            users_info[email] = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt())  # 비밀번호 저장
            print(f'encoded password: {users_info[email]}')
            users_expiration_time[email] = get_expiration_endtime()
            expiration_datetime = get_expiration_datetime()
            insert_user_db(email, users_info[email])

            return {
                # str으로 반환하여 return
                "Authorization": jwt.encode({'email': email}, "secret", algorithm="HS256").decode("UTF-8"),
                "Expiration": expiration_datetime,
                "return_code": "2"
            }, 200


@Auth.route('/register_v2')
class AuthRegister_v2(Resource):
    @Auth.expect(user_fields_pin_auth)
    @Auth.doc(responses={200: 'Return Register Status'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 3
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        users_info = get_all_user_info_from_db()
        email = request.json['email']
        password = request.json['password']
        pin_no = request.json['pin']
        nickname = request.json['nickname']
        if email in users_info:
            return {
                "message": "[ Register Failed ] the email already exists",
                "return_code": "0"
            }, 200
        else:
            # if pin_no != created_otp["OTP"]:
            #     return {
            #         "message": " [ Register Failed ] PIN CODE doen't match",
            #         "return_code" : "1"
            #     }, 200
            # else:
            users_info[email] = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt())  # 비밀번호 저장
            print(f'encoded password: {users_info[email]}')
            users_expiration_time[email] = get_expiration_endtime()
            expiration_datetime = get_expiration_datetime()
            duplicate_check = insert_user_db_v2(
                email, users_info[email], nickname)
            if duplicate_check == False:
                return {
                    "message": "[ Register Failed ] nickname already exists",
                    "return_code": "0"
                }, 200
            else:
                return {
                    # str으로 반환하여 return
                    "Authorization": jwt.encode({'email': email}, "secret", algorithm="HS256").decode("UTF-8"),
                    "Expiration": expiration_datetime,
                    "return_code": "2"
                }, 200


@Auth.route('/login')  # @@ryan : 비밀번호 체크 기능 복원
class AuthLogin(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Return Login Status'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 2
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        # header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        # print(f'header : {header}')
        # if header == None:
        #     return {
        #         "message": "Please login first",
        #         "update": "0"
        #     }, 200
        # token_data = jwt.decode(header, "secret", algorithm="HS256")
        # print(f'token_data : {token_data}')
        # email = token_data['email']#request.json['email']
        # users_info = get_all_user_info_from_db()
        email = request.json['email']
        password = request.json['password']
        print(f'email : {email}, passwd : {password}')
        encoded_pass = password.encode('utf-8')
        # print(f'encoded_pass : {encoded_pass}')
        # print(f'db_password : {users_info[email]}')
        print(bcrypt.checkpw(password.encode('utf-8'),
              users_info[email].encode('utf-8')))
        if email not in users_info:
            return {
                "message": "Email Not Found",
                "return_code": "0"
            }, 200
        # 비밀번호 일치 확인
        elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):
            return {
                "message": "Auth Failed",
                "return_code": "1"
            }, 200
        else:
            token = jwt.encode({'email': email}, "secret",
                               algorithm="HS256").decode("UTF-8")
            users_token[email] = token
            print(f'token : {token}')
            # if users_expiration_time[email] == '':
            #    users_expiration_time[email] = get_expiration_endtime()
            #    expiration_datetime = get_expiration_datetime()
            # else :
            expiration_datetime = get_expiration_datetime()
            print(f'expiration_datetime :{expiration_datetime}')
            return {
                "Authorization": token,
                "Expiration": expiration_datetime,
                "return_code": "2"
            }, 200


@Auth.route('/request_payment')  # @@ryan : 비밀번호 체크 기능 복원
class Auth_request_payment(Resource):
    @Auth.expect(user_fields_req_reward_admin)
    @Auth.doc(responses={200: 'Return request reward to admin'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 1
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # password = request.json['password']
        print(request.json)
        req_reward = request.json['amount']
        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
        #     return {
        #         "message": "password mismatch",
        #         "return_code": "1"
        #     }, 200
        # elif token_data['email'] != email:
        #     return {
        #         "message": "token mismatch",
        #         "return_code": "2"
        #     }, 200
        else:
            status = request_reward_to_admin(email, req_reward)
            if status == True:
                return {
                    "message": "Request for reward success!!",
                    "processing": req_reward,
                    "return_code": "1"
                }, 200
            else:
                return {
                    "message": "Insufficient reward",
                    "return_code": "0"
                }, 200

@Auth.route('/payment_request_history')  
class Auth_request_payment(Resource):
    @Auth.expect(user_payment_request_history)
    @Auth.doc(responses={200: 'Return payment request history'})
    def post(self):
        # data = request.data
        # params = json.loads(data)
        # num_params = len(params)
        # required_params = 1
        # if num_params < required_params:
        #     return {
        #         "message": "lack of parameters",
        #         "return_code": "0"
        #     }, 200

        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # password = request.json['password']
        print(request.json)

        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
        #     return {
        #         "message": "password mismatch",
        #         "return_code": "1"
        #     }, 200
        # elif token_data['email'] != email:
        #     return {
        #         "message": "token mismatch",
        #         "return_code": "2"
        #     }, 200
        else:
            
            reward_list = []
            status, reward_list = payment_request_history(email)
            print(f'reward_list : {reward_list}')
            if status == True:
                return reward_list, 200
            else:
                return {
                    "message": "no payment reward",
                    "return_code": "0"
                }, 200            

@Auth.route('/payment_request_history_by_email')  
class Auth_request_payment_by_email(Resource):
    @Auth.expect(user_payment_request_history_by_email)
    @Auth.doc(responses={200: 'Return payment request history'})
    def post(self):
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # password = request.json['password']
        print(request.json)

        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
        #     return {
        #         "message": "password mismatch",
        #         "return_code": "1"
        #     }, 200
        # elif token_data['email'] != email:
        #     return {
        #         "message": "token mismatch",
        #         "return_code": "2"
        #     }, 200
        else:    
            reward_list = []
            status, reward_list = payment_request_history(email)
            print(f'reward_list : {reward_list}')
            if status == True:
                return reward_list, 200
            else:
                return {
                    "message": "no payment reward",
                    "return_code": "0"
                }, 200  
            
@Auth.route('/register_payment_account')  # @@ryan : 비밀번호 체크 기능 복원
class Auth_register_payment_account(Resource):
    @Auth.expect(user_fields_paypal_venmo)
    @Auth.doc(responses={200: 'Return register payal Info'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 2
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # password = request.json['password']
        print(request.json)
        payment_account = request.json['account']
        payment_option = request.json['option']
        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
        #     return {
        #         "message": "password mismatch",
        #         "return_code": "1"
        #     }, 200
        # elif token_data['email'] != email:
        #     return {
        #         "message": "token mismatch",
        #         "return_code": "2"
        #     }, 200
        else:
            append_payment_info_db(
                email, payment_account, payment_option)
            return {
                "message": "Append paypal/venmo account success!!",
                "return_code": "1"
            }, 200


@Auth.route('/update_payment_info')  # @@ryan : 비밀번호 체크 기능 복원
class Auth_update_payment_info(Resource):
    @Auth.expect(user_fields_paypal_venmo)
    @Auth.doc(responses={200: 'Return register payal Info'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 2
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # password = request.json['password']
        print(request.json)
        payment_account = request.json['account']
        payment_option = request.json['option']
        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
        #     return {
        #         "message": "password mismatch",
        #         "return_code": "1"
        #     }, 200
        # elif token_data['email'] != email:
        #     return {
        #         "message": "token mismatch",
        #         "return_code": "2"
        #     }, 200
        else:
            update_payment_info_db(
                email, payment_account, payment_option)
            return {
                "message": "Update paypal/venmo account success!!",
                "return_code": "1"
            }, 200


@Auth.route('/payment_info')  # @@ryan : 비밀번호 체크 기능 복원
class Auth_payment_info(Resource):
    @Auth.expect(user_fields_paypal_venmo)
    @Auth.doc(responses={200: 'Return register payal Info'})
    def post(self):
        # data = request.data
        # params = json.loads(data)

        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        # print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # password = request.json['password']
        # print(request.json)

        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
        #     return {
        #         "message": "password mismatch",
        #         "return_code": "1"
        #     }, 200
        # elif token_data['email'] != email:
        #     return {
        #         "message": "token mismatch",
        #         "return_code": "2"
        #     }, 200
        else:
            payment_account, payment_option,  user_reward = get_payment_info_db(email)
            return {
                "account": payment_account,
                "option": payment_option,
                "reward": user_reward
            }, 200
# 회웡 탈퇴
# 2022.01.09


@Auth.route('/withdraw')
class AuthLogin(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Return Login Status'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 2
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        # header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        # print(f'header : {header}')
        # if header == None:
        #     return {
        #         "message": "Please login first",
        #         "update": "0"
        #     }, 200
        # token_data = jwt.decode(header, "secret", algorithm="HS256")
        # print(f'token_data : {token_data}')
        # email = token_data['email']#request.json['email']
        # users_info = get_all_user_info_from_db()
        email = request.json['email']
        password = request.json['password']
        print(f'email : {email}, passwd : {password}')
        encoded_pass = password.encode('utf-8')
        # print(f'encoded_pass : {encoded_pass}')
        # print(f'db_password : {users_info[email]}')
        print(bcrypt.checkpw(password.encode('utf-8'),
              users_info[email].encode('utf-8')))
        if email not in users_info:
            return {
                "message": "Email Not Found",
                "return_code": "0"
            }, 200
        # 비밀번호 일치 확인
        elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):
            return {
                "message": "Auth Failed",
                "return_code": "1"
            }, 200
        else:
            token = jwt.encode({'email': email}, "secret",
                               algorithm="HS256").decode("UTF-8")
            users_token[email] = token
            print(f'token : {token}')
            # if users_expiration_time[email] == '':
            #    users_expiration_time[email] = get_expiration_endtime()
            #    expiration_datetime = get_expiration_datetime()
            # else :
            withdrawal_status = withdraw_user_db()
            print(f'withdrawal_status :{withdrawal_status}')
            return {
                "message": "withdraw user",
                "return_code": "2"
            }, 200


@ Auth.route('/update_user_info')
class update_user_info(Resource):
    @ Auth.expect(user_info_fields_auth)
    @ Auth.doc(responses={200: 'Return Update User Info'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 4
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # password = request.json['password']
        print(request.json)
        role = request.json['role']
        school_name = request.json['schoolName']
        school_code = request.json['schoolCode']
        grade = request.json['grade']
        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
        #     return {
        #         "message": "password mismatch",
        #         "return_code": "1"
        #     }, 200
        # elif token_data['email'] != email:
        #     return {
        #         "message": "token mismatch",
        #         "return_code": "2"
        #     }, 200
        else:
            update_user_info_db(
                email, users_info[email], role, school_name, school_code, grade)
            return {
                "message": "update success!!",
                "return_code": "1"
            }, 200


@ Auth.route('/update_user_info_v2')
class update_user_info_v2(Resource):
    @ Auth.expect(user_info_fields_auth_v2)
    @ Auth.doc(responses={200: 'Return Update User Info'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 5
        print(params)
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # password = request.json['password']
        print(request.json)
        role = request.json['role']
        school_name = request.json['schoolName']
        school_code = request.json['schoolCode']
        grade = request.json['grade']
        nickname = request.json['nickname']
        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
        #     return {
        #         "message": "password mismatch",
        #         "return_code": "1"
        #     }, 200
        # elif token_data['email'] != email:
        #     return {
        #         "message": "token mismatch",
        #         "return_code": "2"
        #     }, 200
        else:
            check_nickname = update_user_info_db_v2(
                email, users_info[email], role, school_name, school_code, grade, nickname)
            if check_nickname == False:
                return {
                    "message": "nickname already exists",
                    "return_code": "0"
                }, 200
            else:
                return {
                    "message": "update success!!",
                    "return_code": "1"
                }, 200


@ Auth.route('/get_user_info')
class get_user_info(Resource):
    @ Auth.expect(jwt_fields)
    @ Auth.doc(responses={200: 'Return User Info'})
    def post(self):
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        print(f'header : {header}')
        if header == None:
            return {
                "message": "Please login first",
                "update": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # password = request.json['password']
        # role = request.json['role']
        # school_name = request.json['schoolName']
        # school_code = request.json['schoolCode']
        # grade = request.json['grade']
        if email not in users_info:
            print(f'{email} not in users_info')
            return {
                "message": "Email Not Found",
                "return_code": "0"
            }, 200
        # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
        #     return {
        #         "message": "password mismatch",
        #         "return_code": "1"
        #     }, 200
        # elif token_data['email'] != email:
        #     return {
        #         "message": "token mismatch",
        #         "return_code": "2"
        #     }, 200
        else:
            role, school_name, school_code, grade,nickname = get_user_info_db(
                email, users_info[email])
            return {
                "message": "get info success!!",
                "return_code": "1",
                "role": role,
                "schoolName": school_name,
                "schoolCode": school_code,
                "grade": grade,
                "nickname": nickname
            }, 200

@ Auth.route('/get_user_info_v2')
class get_user_info_v2(Resource):
    @ Auth.expect(jwt_fields)
    @ Auth.doc(responses={200: 'Return User Info'})
    def post(self):
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        print(f'header : {header}')
        if header == None:
            return {
                "message": "Please login first",
                "update": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # password = request.json['password']
        # role = request.json['role']
        # school_name = request.json['schoolName']
        # school_code = request.json['schoolCode']
        # grade = request.json['grade']
        if email not in users_info:
            print(f'{email} not in users_info')
            return {
                "message": "Email Not Found",
                "return_code": "0"
            }, 200
        # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
        #     return {
        #         "message": "password mismatch",
        #         "return_code": "1"
        #     }, 200
        # elif token_data['email'] != email:
        #     return {
        #         "message": "token mismatch",
        #         "return_code": "2"
        #     }, 200
        else:
            role, school_name, school_code, grade, nickname = get_user_info_db_v2(
                email, users_info[email])
            return {
                "message": "get info success!!",
                "return_code": "1",
                "role": role,
                "schoolName": school_name,
                "schoolCode": school_code,
                "grade": grade,
                "nickname": nickname
            }, 200

@ Auth.route('/get_user_reward')
class get_user_reward(Resource):
    @ Auth.expect(jwt_fields)
    @ Auth.doc(responses={200: 'Return User Reward'})
    def post(self):
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        print(f'header : {header}')
        if header == None:
            return {
                "message": "Please login first",
                "update": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # password = request.json['password']
        # role = request.json['role']
        # school_name = request.json['schoolName']
        # school_code = request.json['schoolCode']
        # grade = request.json['grade']
        if email not in users_info:
            print(f'{email} not in users_info')
            return {
                "message": "Email Not Found",
                "return_code": "0"
            }, 200
        # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
        #     return {
        #         "message": "password mismatch",
        #         "return_code": "1"
        #     }, 200
        # elif token_data['email'] != email:
        #     return {
        #         "message": "token mismatch",
        #         "return_code": "2"
        #     }, 200
        else:
            reward = get_user_reward_db(email)
            return {
                "message": "get user reward success!!",
                "return_code": "1",
                "reward": reward
            }, 200
