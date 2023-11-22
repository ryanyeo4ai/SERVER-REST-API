import numpy as np
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import jwt
import bcrypt
from flask_restx import Resource, Api, Namespace, fields
from datetime import datetime
from datetime import timedelta
import time
import uuid
import redis
import json
from db_connect import *
from otp import *
from timestamp import *
from estimate_job import *

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

subjects = {'sat': 'sat', 'middleMath': 'middle-math', 'algebra1': 'algebra-1', 'algebra2': 'algebra-2',
            'geometry': 'geometry', 'preCalculus': 'pre-calculus', 'apCalculus': 'ap-calculus', 'apStatistics': 'ap-statistics',
            'ibMath': 'ib-math', 'multiVariables': 'multi-variable', 'biology': 'biology', 'apBiology': 'ap-biology', 'ibBiology': 'ib-biology',
            'chemistry': 'chemistry', 'apChemistry': 'ap-chemistry', 'ibChemstry': 'ib-chemistry', 'physics': 'physics', 'apPhysics': 'ap-physics',
            'ibPhysics': 'ib-physics'}

users_info = get_all_user_info_from_db()
users_token = {}
users_expiration_time = {}
created_otp = {}

QuestionAnswer = Namespace(
    name="QA",
    description="Question과 Answer를 위한 API",
)

jwt_fields = QuestionAnswer.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})

qa_image_upload = QuestionAnswer.inherit('Image Upload', {
    'image file': fields.String(description='image to upload', required=True, example="image.png")
})

qa_delete_question = QuestionAnswer.model('Delete Question',  {
    'token': fields.String(description='put autorization token into HTTP header', required=True, example="XXXXXX"),
    'question_id': fields.String(description='delete question_id', required=True, example="10")
})

qa_delete_answer = QuestionAnswer.model('Delete Answer',  {
    'token': fields.String(description='put autorization token into HTTP header', required=True, example="XXXXXX"),
    'answer_id': fields.String(description='delete answer', required=True, example="10")
})

qa_question_list = QuestionAnswer.inherit('Question List', jwt_fields, {
    'subjectId': fields.String(description='subject ID', required=True, example="0"),
    'page': fields.String(description='page', required=True, example="1")
})

qa_list_all = QuestionAnswer.inherit('Question List All', {
    'query': fields.String(description='question', required=True, example=""),
})

qa_list_query = QuestionAnswer.inherit('Question List All', {
    'query': fields.String(description='question', required=True, example=""),
    'authorEmail': fields.String(description='email', required=True, example=""),
    'subjectId': fields.String(description='subject ID', required=True, example="0"),
    'page': fields.String(description='page', required=True, example="1"),
    'num': fields.String(description='num', required=False, example="10"),
    'hasAnswer': fields.String(description='hasAnswer', required=False, example="True")
})

qa_list_query_v2 = QuestionAnswer.inherit('Question List2 All', {
    'query': fields.String(description='question', required=True, example=""),
    'authorEmail': fields.String(description='email', required=True, example=""),
    'subjectIDs': fields.String(description='subject ID', required=True, example="['sat,'albegra-1']"),
    'page': fields.String(description='page', required=True, example="1"),
    'num': fields.String(description='num', required=False, example="10"),
    'hasAnswer': fields.String(description='hasAnswer', required=False, example="True")
})

qa_list_query_v3 = QuestionAnswer.inherit('Question List3 All', {
    'query': fields.String(description='question', required=True, example=""),
    'authorEmail': fields.String(description='email', required=True, example=""),
    'nickname': fields.String(description='nickname', required=True, example=""),
    'subjectIDs': fields.String(description='subject ID', required=True, example="['sat,'albegra-1']"),
    'page': fields.String(description='page', required=True, example="1"),
    'num': fields.String(description='num', required=False, example="10"),
    'hasAnswer': fields.String(description='hasAnswer', required=False, example="True")
})


qa_search_keyword = QuestionAnswer.inherit('List', {
    'query': fields.String(description='question', required=True, example="func, angle"),
    'subjectId': fields.String(description='subject ID', required=False, example="0"),
    'page': fields.String(description='page', required=False, example="1"),
    'num': fields.String(description='num', required=False, example="10")
})

qa_question = QuestionAnswer.inherit('Question', jwt_fields, {
    'questionId': fields.String(description='question ID', required=True, example="1")
})

qa_questions_ids = QuestionAnswer.inherit('Question', jwt_fields, {
    'array_questionId': fields.String(description='question ID', required=True, example="1")
})

qa_question_create = QuestionAnswer.inherit('Question Create', jwt_fields, {
    'subjectName': fields.String(description='subject name', required=True, example="SAT"),
    # 'subjectId': fields.String(description='subject ID', required=True, example="0"),
    # 'category': fields.String(description='category', required=True, example="1"),
    'content': fields.String(description='content', required=True, example="Let f be the function defined by f If fwhich of the following must be true about t?"),
    'imageUrl': fields.String(description='imageUrl', required=True, example="uploads/question_01.jpg"),
    'recognizedText': fields.String(description='recognizedText', required=True, example="<latex>f ( t ) = 1</latex>"),
})

qa_question_similarity = QuestionAnswer.inherit('Question Create', jwt_fields, {
    'subjectName': fields.String(description='subject name', required=True, example="SAT"),
    # 'subjectId': fields.String(description='subject ID', required=True, example="0"),
    # 'category': fields.String(description='category', required=True, example="1"),
    'content': fields.String(description='content', required=True, example="Let f be the function defined by f If fwhich of the following must be true about t?"),
    'imageUrl': fields.String(description='imageUrl', required=True, example="uploads/question_01.jpg"),
    'recognizedText': fields.String(description='recognizedText', required=True, example="<latex>f ( t ) = 1</latex>"),
})

qa_write_answer = QuestionAnswer.inherit('Write Answer', jwt_fields, {
    'question_id': fields.String(description='question id', required=True, example="1"),
    'content': fields.String(description='content', required=True, example="Let f be the function defined by f If fwhich of the following must be true about t?"),
    'imageUrl': fields.String(description='imageUrl', required=True, example="uploads/question_01.jpg"),
    'recognizedText': fields.String(description='recognizedText', required=True, example="<latex>f ( t ) = 1</latex>"),
})

qa_question_report = QuestionAnswer.inherit('qa_question_report', jwt_fields, {
    'questionId': fields.String(description='questionID', required=True, example="1"),
    'reportEmail': fields.String(description='reportEmail', required=True, example="신고자 이메일"),
    'issueEmail': fields.String(description='issueEmail', required=True, example="wrong question 소유자 이메일")
})

qa_answer_report = QuestionAnswer.inherit('qa_answer_report', jwt_fields, {
    'answerId': fields.String(description='answerId', required=True, example="1"),
    'reportEmail': fields.String(description='reportEmail', required=True, example="신고자 이메일"),
    'issueEmail': fields.String(description='issueEmail', required=True, example="wrong answer 소유자 이메일")
})
qa_count_question_answer = QuestionAnswer.model('Count Question or Answer',  {
    'authorEmail': fields.String(description='email', required=True, example="")
})

@QuestionAnswer.route('/subjects')
class subjects(Resource):
    @QuestionAnswer.doc(responses={200: 'Return subjects_list '})
    def post(self):
        # subjects = list()
        result_flag, subjects_list = get_subjects_list_db()

        if not result_flag:
            return {
                "message": "No question list",
                "return_code": "0"
            }, 200
        else:
            # question_list = question_list.replace('\\','')
            json_question_list = json.dumps(subjects_list)
            # print(json_question_list)
            # with open('question_list.json', 'w') as outfile:
            #     json.dump(question_list, outfile, indent=4)
            return {
                "subjects list": subjects_list  # json_question_list
            }, 200



@QuestionAnswer.route('/get_count_questions') # 09.19
class get_count_questions(Resource):
    @QuestionAnswer.expect(qa_count_question_answer)
    @QuestionAnswer.doc(responses={200: 'Return # of questions '})
    def post(self):
        # subjects = list()
        data = request.data
        params = json.loads(data)
        print(f'params / # of params: {params} / {len(params)}')
        num_params = len(params)
        if num_params < 1:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        
        author_email = request.json['authorEmail']
        print(f'author_email : {author_email}')
        count_questions = extract_count_questions(author_email)
        print(f'count_questions : {count_questions}')
        return {
            "# of questions": count_questions  
        }, 200

@QuestionAnswer.route('/get_count_answers') # 09.19
class get_count_answers(Resource):
    @QuestionAnswer.expect(qa_count_question_answer)
    @QuestionAnswer.doc(responses={200: 'Return # of answers '})
    def post(self):
        # subjects = list()
        data = request.data
        params = json.loads(data)

        num_params = len(params)
        if num_params < 1:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        
        author_email = request.json['authorEmail']
        count_answers = extract_count_answers(author_email)
        return {
            "# of questions": count_answers  
        }, 200

@QuestionAnswer.route('/rank')
class rank(Resource):
    @QuestionAnswer.doc(responses={200: 'Return rank_list [userEmail, userRank]'})
    def post(self):
        rank_list = []
        rank_list = get_all_user_reward_from_db()
        print(rank_list)
        return {
            "message": "rank list success!!",
            "return_code": "1",
            "rank_list": rank_list
        }, 200


@QuestionAnswer.route('/image_upload')
class image_upload(Resource):
    @QuestionAnswer.expect(qa_image_upload)
    @QuestionAnswer.doc(responses={200: 'Return upload result'})
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
        if email not in user_info:
            return {
                "message": "Please Login First",
                "return_code": "0"
            }, 200
        else:
            f = request.files['file']
            image_uuid = uuid.uuid4()
            image_file_name = str(image_uuid) + '.png'
            imageUrl = 'static/upload/' + image_file_name
            print(f'imageUrl : {imageUrl}')
            # 저장할 경로 + 파일명
            # f.save('web/api_server/static/uploads/1.png' + secure_filename(f.filename))
            f.save(imageUrl)
            return {
                "message": "Image upload success!!",
                "return_code": "1",
                "imageURL": imageUrl
            }, 200

# @QuestionAnswer.route('/question_list')
# class question_list(Resource):
#     @QuestionAnswer.expect(qa_question_list)
#     @QuestionAnswer.doc(responses={200: 'Return Question List'})
#     def post(self):
#         #users_info = get_all_user_info_from_db()
#         header = request.headers.get('Authorization')  # Authorization 헤더로 담음
#         if header == None:
#             return {
#                 "message": "Please Login",
#                 "return_code": "0"
#             }, 200
#         token_data = jwt.decode(header, "secret", algorithm="HS256")
#         print(f'token_data : {token_data}')
#         email = token_data['email']#request.json['email']
#         subject_id = request.json['subjectId']
#         page = request.json['page']

#         if email not in user_info:
#             return {
#                 "message": "Please Login First",
#                 "return_code": "0"
#             }, 200
#         # elif not bcrypt.checkpw(password.encode('utf-8'), users_info[email].encode('utf-8')):  # 비밀번호 일치 확인
#         #     return {
#         #         "message": "password mismatch",
#         #         "return_code": "1"
#         #     }, 200
#         # elif token_data['email'] != email:
#         #     return {
#         #         "message": "token mismatch",
#         #         "return_code": "2"
#         #     }, 200
#         else:
#             question_list = list()
#             result_flag, question_list = get_user_question_db(email, subject_id, page)
#             if not result_flag:
#                 return {
#                     "message": "No question list",
#                     "return_code": "0"
#                 }, 200
#             else:
#                 return {
#                     "message": "extract question list success!!",
#                     "return_code": "1",
#                     "question list": str(question_list)
#                 }, 200

# @QuestionAnswer.route('/list_all')
# class question_list(Resource):
#     @QuestionAnswer.expect(qa_list_all)
#     @QuestionAnswer.doc(responses={200: 'Return List'})
#     def post(self):
#         #users_info = get_all_user_info_from_db()
#         query_str = request.json['query']

#         if len(query_str) == 0:
#             subject_id = -1
#             page = -1
#         question_list = list()
#         result_flag, question_list = get_question_list_all_db(query_str)
#         if not result_flag:
#             return {
#                 "message": "No question list",
#                 "return_code": "0"
#             }, 200
#         else:
#             return {
#                 "message": "extract question list success!!",
#                 "return_code": "1",
#                 "question list": str(question_list)
#             }, 200



@QuestionAnswer.route('/reportQuestion')  # @@ryan 09.08.22
class list(Resource):
    @QuestionAnswer.expect(qa_question_report)
    @QuestionAnswer.doc(responses={200: 'Return List'})
    def post(self):
        # print('/list')
        data = request.data
        params = json.loads(data)

        num_params = len(params)
        if num_params < 3:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login First",
                "return_code": "0"
            }, 200
        else :
            token_data = jwt.decode(header, "secret", algorithm="HS256")
            print(f'token_data : {token_data}')
            email = token_data['email']  # request.json['email']
            if email not in user_info:
                return {
                    "message": "Please login first",
                    "return_code": "0"
                }, 200 
            question_id = request.json['questionID']
            report_email = request.json['reportEmail'] #report_email : 신고자 
            issue_email = request.json['issueEmail'] # issue_email : 문제 올린 사람

            if report_email == email :
                result_flag = report_wrong_question_to_db(question_id, report_email, issue_email)
                # print(f'[qa/answer_list] : {answer_list}')
                if not result_flag:
                    return {
                        "message": "The report of WRONG question is FAILED",
                        "return_code": "0"
                    }, 200
                else:
                    return {
                        "message": "The report of WRONG question is submitted successfully",
                        "return_code": "1"
                    }, 200
            else:
                return {
                    "message": "TReporter email and authorization email are different.",
                    "return_code": "0"
                }, 200

@QuestionAnswer.route('/reportAnswer')  # @@ryan 09.08.22
class list(Resource):
    @QuestionAnswer.expect(qa_answer_report)
    @QuestionAnswer.doc(responses={200: 'Return List'})
    def post(self):
        # print('/list')
        data = request.data
        params = json.loads(data)

        num_params = len(params)
        if num_params < 3:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login First",
                "return_code": "0"
            }, 200
        else : 
            token_data = jwt.decode(header, "secret", algorithm="HS256")
            print(f'token_data : {token_data}')
            email = token_data['email']  # request.json['email']
            if email not in user_info:
                return {
                    "message": "Please login first",
                    "return_code": "0"
                }, 200
            answer_id = request.json['answerID']
            report_email = request.json['reportEmail'] #report_email : 신고자 
            issue_email = request.json['issueEmail'] # issue_email : 문제 올린 사람

            if report_email == email :
                result_flag = report_wrong_answer_to_db(answer_id, report_email, issue_email)
                # print(f'[qa/answer_list] : {answer_list}')
                if not result_flag:
                    return {
                        "message": "The report of WRONG answer is FAILED",
                        "return_code": "0"
                    }, 200
                else:
                    return {
                        "message": "The report of WRONG answer is submitted successfully",
                        "return_code": "1"
                    }, 200
            else:
                return {
                    "message": "TReporter email and authorization email are different.",
                    "return_code": "0"
                }, 200

@QuestionAnswer.route('/list')  # @@ryan: question answer 디폴트값 --> 파라미터로 수정
class list(Resource):
    @QuestionAnswer.expect(qa_list_query)
    @QuestionAnswer.doc(responses={200: 'Return List'})
    def post(self):
        print('/list')
        data = request.data
        params = json.loads(data)

        num_params = len(params)
        if num_params < 6:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200
        query_str = request.json['query']
        author_email = request.json['authorEmail']
        subject_id = request.json['subjectId']
        page = request.json['page']
        query_hasAnswer = request.json['hasAnswer']
        # if len(page) == 0:
        #     query_page = '10'
        # else:
        query_page = page
        num = request.json['num']
        if len(num) == 0:
            query_num = ''
        else:
            query_num = num
        # hasAnswer = request.json['hasAnswer']
        # if len(hasAnswer) == 0:
        #     query_hasAnswer = '0'
        # else:
        #     query_hasAnswer = hasAnswer

        print(f'query_str : {query_str}')
        print(f'subject_id : {subject_id}')
        print(f'page : {page}')
        print(f'num : {num}')
        # print(f'hasAnswer : {hasAnswer}')

        question_list = list()
        answer_list = list()
        result_flag, question_list, answer_list = get_question_list_query_db(
            query_str, author_email, subject_id, query_page, query_num, query_hasAnswer)
        # print(f'[qa/answer_list] : {answer_list}')
        if not result_flag:
            return {
                "message": "No question list",
                "return_code": "0"
            }, 200
        else:
            # question_list = question_list.replace('\\','')
            json_question_list = json.dumps(question_list)
            # print(json_question_list)
            # with open('question_list.json', 'w') as outfile:
            #     json.dump(question_list, outfile, indent=4)
            return {
                "message": "extract question list success!!",
                "return_code": "1",
                "question_list": question_list,  # json_question_list
                "answer_list": answer_list  # json_answer_list
            }, 200


@QuestionAnswer.route('/list/v2')  # @@ryan: question answer 디폴트값 --> 파라미터로 수정
class listv2(Resource):
    @QuestionAnswer.expect(qa_list_query_v2)
    @QuestionAnswer.doc(responses={200: 'Return List'})
    def post(self):
        print('/list/v2')
        data = request.data
        params = json.loads(data)

        num_params = len(params)
        if num_params < 6:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        subject_ids = []
        query_str = request.json['query']
        author_email = request.json['authorEmail']
        subject_ids = request.json['subjectIDs']
        page = request.json['page']
        query_hasAnswer = request.json['hasAnswer']
        # if len(page) == 0:
        #     query_page = '10'
        # else:
        query_page = page
        num = request.json['num']
        if len(num) == 0:
            query_num = ''
        else:
            query_num = num
        # hasAnswer = request.json['hasAnswer']
        # if len(hasAnswer) == 0:
        #     query_hasAnswer = '0'
        # else:
        #     query_hasAnswer = hasAnswer

        print(f'query_str : {query_str}')
        print(f'subject_ids : {subject_ids}')
        print(f'page : {page}')
        print(f'num : {num}')
        # print(f'hasAnswer : {hasAnswer}')

        if len(subject_ids) < 1:
            if len(subject_ids) == 0:
                subject_id = ''
                question_list = list()
                answer_list = list()
                result_flag, question_list, answer_list = get_question_list_query_dbv2(
                    query_str, author_email, subject_id, query_page, query_num, query_hasAnswer)
                # print(f'[qa/answer_list] : {answer_list}')
                if not result_flag:
                    return {
                        "message": "No question list",
                        "return_code": "0"
                    }, 200
                else:
                    # question_list = question_list.replace('\\','')
                    json_question_list = json.dumps(question_list)
                    # print(json_question_list)
                    # with open('question_list.json', 'w') as outfile:
                    #     json.dump(question_list, outfile, indent=4)
                    return {
                        "message": "extract question list success!!",
                        "return_code": "1",
                        "question_list": question_list,  # json_question_list
                        "answer_list": answer_list  # json_answer_list
                    }, 200
            else:
                subject_id = subject_ids[0]
                question_list = list()
                answer_list = list()
                result_flag, question_list, answer_list = get_question_list_query_dbv2(
                    query_str, author_email, subject_id, query_page, query_num, query_hasAnswer)
                # print(f'[qa/answer_list] : {answer_list}')
                if not result_flag:
                    return {
                        "message": "No question list",
                        "return_code": "0"
                    }, 200
                else:
                    # question_list = question_list.replace('\\','')
                    json_question_list = json.dumps(question_list)
                    # print(json_question_list)
                    # with open('question_list.json', 'w') as outfile:
                    #     json.dump(question_list, outfile, indent=4)
                    return {
                        "message": "extract question list success!!",
                        "return_code": "1",
                        "question_list": question_list,  # json_question_list
                        "answer_list": answer_list  # json_answer_list
                    }, 200
        else:
            question_list = list()
            # question_list_2nd = list()
            question_list_final = []
            answer_list = list()

            result_flag, question_list, answer_list = get_question_list_query_dbv2(
                query_str, author_email, subject_ids, query_page, query_num, query_hasAnswer)
            question_list_final.extend(question_list)
            if not result_flag:
                return {
                    "message": "No question list",
                    "return_code": "0"
                }, 200
            else:
                # question_list_final = np.array(question_list_2nd).fattenj().tolist()
                return {
                    "message": "extract question list success!!",
                    "return_code": "1",
                    # json_question_list
                    "question_list": question_list_final[0],
                    "answer_list": answer_list  # json_answer_list
                }, 200


@QuestionAnswer.route('/list_v3')  # 06.25.202 2ryan: question answer 디폴트값 --> 파라미터로 수정
class list_v3(Resource):
    @QuestionAnswer.expect(qa_list_query_v3)
    @QuestionAnswer.doc(responses={200: 'Return List'})
    def post(self):
        data = request.data
        params = json.loads(data)

        num_params = len(params)
        if num_params < 7:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        subject_ids = []
        query_str = request.json['query']
        author_email = request.json['authorEmail']
        nickname = request.json['nickname']
        subject_ids = request.json['subjectIDs']
        page = request.json['page']
        query_hasAnswer = request.json['hasAnswer']

        if len(author_email) == 0 and len(nickname) > 0:
            author_email = get_email_from_nickname(nickname)

        # if len(page) == 0:
        #     query_page = '10'
        # else:
        query_page = page
        num = request.json['num']
        if len(num) == 0:
            query_num = ''
        else:
            query_num = num
        # hasAnswer = request.json['hasAnswer']
        # if len(hasAnswer) == 0:
        #     query_hasAnswer = '0'
        # else:
        #     query_hasAnswer = hasAnswer

        # print(f'query_str : {query_str}')
        # print(f'author_email : {author_email}')
        # print(f'nickname : {nickname}')
        # print(f'subject_ids : {subject_ids}')
        # print(f'page : {page}')
        # print(f'num : {num}')
        # print(f'query_hasAnswer : {query_hasAnswer}')

        if len(subject_ids) < 1:
            if len(subject_ids) == 0:
                subject_id = ''
                question_list = list()
                answer_list = list()
                result_flag, question_list, answer_list = get_question_list_query_db_v4( 
                    query_str, nickname, author_email, subject_id, query_page, query_num, query_hasAnswer)
                # print(f'[qa/answer_list] : {answer_list}')
                if not result_flag:
                    return {
                        "message": "No question list",
                        "return_code": "0"
                    }, 200
                else:
                    # question_list = question_list.replace('\\','')
                    # json_question_list = json.dumps(question_list)
                    # print(json_question_list)
                    # with open('question_list.json', 'w') as outfile:
                    #     json.dump(question_list, outfile, indent=4)
                    return {
                        "message": "extract question list success!!",
                        "return_code": "1",
                        "question_list": question_list,  # json_question_list
                        "answer_list": answer_list  # json_answer_list
                    }, 200
            else:
                subject_id = subject_ids[0]
                question_list = list()
                answer_list = list()
                result_flag, question_list, answer_list = get_question_list_query_db_v3(
                    query_str, nickname, author_email, subject_id, query_page, query_num, query_hasAnswer)
                # print(f'[qa/answer_list] : {answer_list}')
                if not result_flag:
                    return {
                        "message": "No question list",
                        "return_code": "0"
                    }, 200
                else:
                    # question_list = question_list.replace('\\','')
                    json_question_list = json.dumps(question_list)
                    # print(json_question_list)
                    # with open('question_list.json', 'w') as outfile:
                    #     json.dump(question_list, outfile, indent=4)
                    return {
                        "message": "extract question list success!!",
                        "return_code": "1",
                        "question_list": question_list,  # json_question_list
                        "answer_list": answer_list  # json_answer_list
                    }, 200
        else:
            question_list = list()
            # question_list_2nd = list()
            question_list_final = []
            answer_list = list()

            result_flag, question_list, answer_list = get_question_list_query_dbv2_v2(
                query_str, author_email, nickname, subject_ids, query_page, query_num, query_hasAnswer)
            question_list_final.extend(question_list)
            if not result_flag:
                return {
                    "message": "No question list",
                    "return_code": "0"
                }, 200
            else:
                # question_list_final = np.array(question_list_2nd).fattenj().tolist()
                return {
                    "message": "extract question list success!!",
                    "return_code": "1",
                    # json_question_list
                    "question_list": question_list_final[0],
                    "answer_list": answer_list  # json_answer_list
                }, 200


@QuestionAnswer.route('/list/ids')
class search_keyword(Resource):
    @QuestionAnswer.expect(qa_questions_ids)
    @QuestionAnswer.doc(responses={200: 'Return List'})
    def post(self):
        question_ids = []

        data = request.data
        params = json.loads(data)
        # print(f'/list val --> {params}')
        # print(f'params.keys : {params.keys()}')
        num_params = len(params)
        if num_params < 6:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        str = request.json['ids']
        if len(str) != 0:
            str = str.replace('[', '')
            str = str.replace(']', '')
            # print(f'str : {str}')
            question_ids = str.split(',')
            number_question_ids = len(question_ids)
            # print(f'len(question_ids) : {len(question_ids)}')
            # print(f'question_ids : {question_ids}')
        else:
            number_question_ids = 0
        # print(f'[qa] query_str : {query_str}')
        # subject_id = request.json['subjectId']
        # page = request.json['page']
        # if len(query_str) == 0:
        #     subject_id = -1
        #     page = -1
        question_list = list()
        result_flag, question_list = get_question_ids_list_db(
            question_ids, number_question_ids)
        if not result_flag:
            return {
                "message": "No question list",
                "return_code": "0"
            }, 200
        else:
            return {
                "message": "extract question list success!!",
                "return_code": "1",
                "question list": question_list
            }, 200


@QuestionAnswer.route('/question')
class question(Resource):
    @QuestionAnswer.expect(qa_question)
    @QuestionAnswer.doc(responses={200: 'Return Answer List'})
    def post(self):
        print('[qa/question]')
        data = request.data
        params = json.loads(data)
        print(f'/list val --> {params}')
        print(f'params.keys : {params.keys()}')
        num_params = len(params)
        if num_params < 1:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200

        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login First",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        question_id = request.json['questionId']

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
            answer_list = list()
            result_flag, question_list, answer_list = get_answer_for_question_db(
                email, question_id)
            if not result_flag:
                return {
                    "message": "No question list",
                    "return_code": "0"
                }, 200
            else:
                json_answer_list = json.dumps(answer_list)
                return {
                    "message": "extract answer list success!!",
                    "return_code": "1",
                    "question": question_list,
                    "answer_list": answer_list  # json_answer_list
                }, 200


@QuestionAnswer.route('/create')
class create(Resource):
    @QuestionAnswer.expect(qa_question_create)
    @QuestionAnswer.doc(responses={200: 'Return Create Question No'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 6
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login First",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        subject_name = request.json['subjectName']
        subject_id = request.json['subjectId']
        category = request.json['category']
        content = request.json['content']
        imageUrl = request.json['imageUrl']
        recog_text = request.json['recognizedText']

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
            answer_list = list()
            sbj_name = 'Who are you?'
            q_no = create_question_db(
                email, subject_id, subject_name, category, content, imageUrl, recog_text)

            return {
                "message": " Question Creation Success",
                "return_code": "1",
                "question_id": q_no
            }, 200


@QuestionAnswer.route('/create_v2')
class create_v2(Resource):
    @QuestionAnswer.expect(qa_question_create)
    @QuestionAnswer.doc(responses={200: 'Return Create Question No'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 6
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login First",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # schoolname = token_data['schoolName']
        # schoolcode = token_data['schoolCode']
        subject_name = request.json['subjectName']
        subject_id = request.json['subjectId']
        category = request.json['category']
        content = request.json['content']
        imageUrl = request.json['imageUrl']
        recog_text = request.json['recognizedText']

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
            answer_list = list()
            # q_no = create_question_db_v2(
            #     email, schoolname, schoolcode, subject_name, subject_id, category, content, imageUrl, recog_text)
            q_no = create_question_db_v2( 
                email, subject_name, subject_id, category, content, imageUrl, recog_text)
            return {
                "message": " Question Creation Success",
                "return_code": "1",
                "question_id": q_no
            }, 200

@QuestionAnswer.route('/check_similarity')
class check_similarity(Resource):
    @QuestionAnswer.expect(qa_question_similarity)
    @QuestionAnswer.doc(responses={200: 'Return similiar Question ID'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        required_params = 6
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login First",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # schoolname = token_data['schoolName']
        # schoolcode = token_data['schoolCode']
        # subject_name = request.json['subjectName']
        # subject_id = request.json['subjectId']
        # category = request.json['category']
        # content = request.json['content']
        # imageUrl = request.json['imageUrl']
        recog_text = request.json['recognizedText']

        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        else:
            q_no = question_similarity_2(recog_text)
            return {
                "message": " Similiar Question ID",
                "return_code": "1",
                "question_id": q_no
            }, 200

@QuestionAnswer.route('/deleteQuestion')
class delete_question(Resource):
    @QuestionAnswer.expect(qa_delete_question)
    @QuestionAnswer.doc(responses={200: 'Return List'})
    def post(self):
        print('/delete_question')
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
                "message": "Please Login First",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        question_id = request.json['question_id']

        if email not in user_info:
            return {
                "message": "Invalide email",
                "return_code": "0"
            }, 200
        else:
            result_flag = delete_question_db(question_id)
            if not result_flag:
                return {
                    "message": "No question_id to delete",
                    "return_code": "0"
                }, 200
            else:
                return {
                    "message": "Delete question success!!",
                    "return_code": "1"
                }, 200


@QuestionAnswer.route('/write_answer')
class write_answer(Resource):
    @QuestionAnswer.expect(qa_write_answer)
    @QuestionAnswer.doc(responses={200: 'Return Write Answer No.'})
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
                "message": "Please Login First",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        question_id = request.json['question_id']
        content = request.json['content']
        imageUrl = request.json['imageUrl']
        recog_text = request.json['recognizedText']

        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        else:
            answer_list = list()
            ans_no = create_write_answer_db(
                email, question_id, content, imageUrl, recog_text)
            if ans_no == '-2':
                return {
                    "message": "You CAN'T write the answer by your question",
                    "return_code": "0"
                }, 200    
            elif ans_no == '-1':
                return {
                    "message": "Write Answer FAIL",
                    "return_code": "0"
                }, 200   
            else:
                return {
                    "message": " Write Answer Success",
                    "return_code": "1",
                    "answer no": ans_no
                }, 200


@QuestionAnswer.route('/write_answer_v2')
class write_answer_v2(Resource):
    @QuestionAnswer.expect(qa_write_answer)
    @QuestionAnswer.doc(responses={200: 'Return Write Answer No.'})
    def post(self):
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        print(f'num_params : {num_params}')
        # question_id = request.json['question_id']
        # subject_name = request.json['subjectName']
        # category = request.json['category']
        # content = request.json['content']
        # imageUrl = request.json['imageUrl']
        # recog_text = request.json['recognizedText']
        required_params = 5
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login First",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        # nickname = token_data['nickname']
        question_id = request.json['question_id']
        content = request.json['content']
        imageUrl = request.json['imageUrl']
        recog_text = request.json['recognizedText']

        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        else:
            answer_list = list()
            ans_no = create_write_answer_db_v2(
                email, question_id, content, imageUrl, recog_text)

            if ans_no == '-2':
                return {
                    "message": "You CAN'T write the answer by your question",
                    "return_code": "0"
                }, 200    
            elif ans_no == '-1':
                return {
                    "message": "Write Answer FAIL",
                    "return_code": "0"
                }, 200   
            else:
                return {
                    "message": " Write Answer Success",
                    "return_code": "1",
                    "answer no": ans_no
                }, 200

@QuestionAnswer.route('/deleteAnswer')
class deleteAnswer(Resource):
    @QuestionAnswer.expect(qa_delete_answer)
    @QuestionAnswer.doc(responses={200: 'Return List'})
    def post(self):
        print('/deleteAnswer')
        data = request.data
        params = json.loads(data)
        num_params = len(params)
        print(f'num_params : {num_params}')
        required_params = 1
        if num_params < required_params:
            return {
                "message": "lack of parameters",
                "return_code": "0"
            }, 200
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {
                "message": "Please Login First",
                "return_code": "0"
            }, 200
        token_data = jwt.decode(header, "secret", algorithm="HS256")
        print(f'token_data : {token_data}')
        email = token_data['email']  # request.json['email']
        answer_id = request.json['answer_id']


        if email not in user_info:
            return {
                "message": "Please login first",
                "return_code": "0"
            }, 200
        else:
            result_flag = delete_write_answer_db(answer_id)
            if not result_flag:
                return {
                    "message": "No answer_id to delete",
                    "return_code": "0"
                }, 200
            else:
                return {
                    "message": "delete answer success!!",
                    "return_code": "1"
                }, 200
# @QuestionAnswer.route('/recent')
# class question(Resource):
#     @QuestionAnswer.expect(qa_recent_question_list)
#     @QuestionAnswer.doc(responses={200: 'Return Recent Question'})
#     def post(self):

#         question_num = int(request.json['number'])
#         if question_num <= 0:
#             question_num = 10

#         question_list = recent_question_db(question_num)

#         return {
#             "message": " Write Answer Success",
#             "return_code" : "1",
#             "answer no" : question_list
#         }, 200
@QuestionAnswer.route('/estimate_job')
class estimate_job(Resource):
    def post(self):
        data = request.data
        params = json.loads(data)
        desc = params["desc"]
        
        print(f'desc : {desc}')
        title,score = estimate_job_title_role(desc)
        print(f'title : {title}')
        print(f'score : {score}')

        return {
            "title": title,
            "score" : score
        }, 200
    
@QuestionAnswer.route('/get_roles_from_job')
class estimate_job(Resource):
    def post(self):
        # JOB_FILE = 'job_db.csv'
        # job_db_df = pd.read_csv(JOB_FILE)
        
        data = request.data
        params = json.loads(data)
        print(params)
        req_title = params["req_title"]
        
        keywords_list = []
        roles_list = []
        # db_title = job_db_df.iloc[0,1]
        # keywords_list = job_db_df.iloc[0,2].split(',')
        
        count, keywords_list = extract_roles(req_title)
        if count > 0:
            for i, item in enumerate(keywords_list):
                if item in roles_list:
                   continue
                else:
                    if item == '개발' or item == '설계' or item == '제품' or item == '상품':
                        continue
                    else:
                        roles_list.append(item)

            print(f'keywords : {roles_list}')

            return {
                "req_title": req_title,
                "keywords" : roles_list
            }, 200
        else:
            return {
                "req_title": 'no title',
                "keywords" : []
            }, 200