from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message
from flask_sslify import SSLify
from flask_cors import CORS
from flask_restx import Resource, Api, Namespace, fields
from flask_bcrypt import Bcrypt
from flask import jsonify
import pymysql
from werkzeug.utils import secure_filename
import pandas as pd
#import sqlalchemy as db
import json
import jwt
import os
#import pandas as pd
from auth import Auth
from qa import QuestionAnswer
from user_info import UserInfo
from db_connect import *

app = Flask(__name__)
CORS(app)
sslify = SSLify(app)
mail = Mail()
mail.init_app(app)

api = Api(
    app,
    version='1.8',
    title='Solple REST API',
    description='REST API for Solple app (Updated \'Similarity\' feature, 10.12.2022)',
    terms_url="/",
    contact="solpledev@gmail.com",
    license="MIT"
)
#mail = Mail()

api.add_namespace(Auth, '/auth')
api.add_namespace(QuestionAnswer, '/qa')
bcrypt = Bcrypt(app)

#app.config['JWT_SECRET_KEY'] = '12345'
#algorithm = 'HS256'

school = {}
count = 1

# @app.route('/fileUpload', methods = ['GET', 'POST'])
# def file_upload():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save('static/uploads/' + secure_filename(f.filename))
#         files = os.listdir("static/uploads")

#         conn,cursor  = db_connect()
#         # 파일명과 파일경로를 데이터베이스에 저장함
#         sql = "INSERT INTO image (image_name, image_dir) VALUES ('%s', '%s')" % (secure_filename(f.filename), 'static/uploads/'+secure_filename(f.filename))
#         cursor.execute(sql)
#         data = cursor.fetchall()

#         if not data:
#             conn.commit()
#             return redirect(url_for("main"))

#         else:
#             conn.rollback()
#             return 'upload failed'

#         cursor.close()
#         conn.close()


@app.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        #f.save('web/api_server/static/uploads/1.png' + secure_filename(f.filename))
        f.save('web/api_server/static/uploads/1.png')
        return 'uploads 디렉토리 -> 파일 업로드 성공!'

@app.route('/paypal_file_upload', methods=['GET', 'POST'])
def paypal_file_upload():
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        #f.save('web/api_server/static/uploads/1.png' + secure_filename(f.filename))
        f.save('static/paypal/' + f.filename)
        #return render_template('paypal_upload.html')
        process_paypal_result('static/paypal/' + f.filename)
        return render_template('paypal_upload.html')
    else:
        return render_template('paypal_upload.html')


# @app.route('/view', methods = ['GET', 'POST'])
# def view():
#    conn,cursor  = db_connect()  # connection으로부터 cursor 생성 (데이터베이스의 Fetch 관리)
#    sql = "SELECT image_name, image_dir FROM image"  # 실행할 SQL문
#    cursor.execute(sql)  # 메소드로 전달해 명령문을 실행
#    data = cursor.fetchall()  # 실행한 결과 데이터를 꺼냄

#    data_list = []

#    for obj in data:  # 튜플 안의 데이터를 하나씩 조회해서
#        data_dic = {  # 딕셔너리 형태로
#            # 요소들을 하나씩 넣음
#            'name': obj[0],
#            'dir': obj[1]
#        }
#        data_list.append(data_dic)  # 완성된 딕셔너리를 list에 넣음

#    cursor.close()
#    conn.close()

#    return render_template('view.html', data_list=data_list)  # html을 렌더하며 DB에서 받아온 값들을 넘김


@app.route('/upload')
def image_upload():
    return render_template('upload.html')

@app.route('/paypal_upload')
def paypal_upload():
    return render_template('paypal_upload.html')

# engine = db.create_engine('mysql+pymysql://deepbackend:kissme!004@db.deepbackend.gabia.io/dbdeepbackend')
# connection = engine.connect()

#metadata = db.MetaData()


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
