from flask import Flask, request
from flask_cors import CORS
from flask_restx import Resource, Api
import sqlalchemy as db
#import pandas as pd

app = Flask(__name__)
CORS(app)
api = Api(app)

school = {}
count = 1

engine = db.create_engine('')
connection = engine.connect()
metadata = db.MetaData()

@api.route('/school')
class memberPost(Resource):
    def post(self):
        global count
        global school
        
        # result_sql_df = pd.read_sql_query("select * from school", engine)

        # idx = count
        # count += 1

        # result_json = result_sql_df.to_json(orient = 'columns')
        # #school[idx] = request.json.get('data')
        # return result_json
        return {
            'member_id': idx,
            'data': school[idx]
        }


@api.route('/school_code/<int:school_code>')
class school_code(Resource):
    def get(self, school_code):
        #print(f'school_code : {school_code}, {type(school_code)}')
        result_sql_df = pd.read_sql_query("select * from school where schoolCode = " + str(school_code), engine)
        print(result_sql_df)
        result_json = result_sql_df.to_json(orient = 'columns')
        return result_json
        # return {
        #     'school_code': member_id,
        #     'data': school[member_id]
        # }

    # def put(self, member_id):
    #     school[member_id] = request.json.get('data')
    #     return {
    #         'member_id': member_id,
    #         'data': school[member_id]
    #     }
    
    # def delete(self, member_id):
    #     del school[member_id]
    #     return {
    #         "delete" : "success"
    #     }
@api.route('/school_name/<string:school_name>')
class school_name(Resource):
    def get(self, school_name):
        print(f'school_name : {school_name}, {type(school_name)}')
        result_sql_df = pd.read_sql_query("select * from school where schoolName = " + "'" + school_name + "'", engine)
        print(result_sql_df)
        result_json = result_sql_df.to_json(orient = 'columns')
        return result_json

@api.route('/state_name/<string:state_name>')
class state_name(Resource):
    def get(self, state_name):
        print(f'state_name : {state_name}, {type(state_name)}')
        result_sql_df = pd.read_sql_query("select * from school where stateName = " + "'" + state_name + "'", engine)
        print(result_sql_df)
        result_json = result_sql_df.to_json(orient = 'columns')
        return result_json

@api.route('/state_code/<string:state_code>')
class state_code(Resource):
    def get(self, state_code):
        print(f'state_name : {state_code}, {type(state_code)}')
        result_sql_df = pd.read_sql_query("select * from school where stateCode = " + "'" + state_code+ "'", engine)
        print(result_sql_df)
        result_json = result_sql_df.to_json(orient = 'columns')
        return result_json

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)