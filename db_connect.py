import pymysql
import jwt
import bcrypt
from datetime import datetime
import json
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer, util

user_info = {}


def db_connect():
    conn = pymysql.connect(host='',
                           user='', password='', db='', charset='utf8')
    cursor = conn.cursor()

    return conn, cursor


def db_execute_quiry(cursor, sql):
    # sql = "SELECT * FROM dummy_gps"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def db_close(conn):
    conn.commit()
    conn.close()

def extract_count_questions(email): #09.22
    count_value = 0
    conn, cursor = db_connect()
    sql = "SELECT question_id FROM Question where author_email = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()
    db_close(conn)

    count_value = len(records)
    print(f'count_value : {count_value}')
    # count_value.append(count_questions)

    return count_value

def extract_count_answers(email): #09.22
    conn, cursor = db_connect()
    sql = "SELECT answer_id FROM Answer where author_email = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()
    db_close(conn)
    
    return len(records)
def report_wrong_question_to_db(question_id, report_email, issue_email): #report_email : 신고자 , issue_email : 문제 올린 사람
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "INSERT INTO report_qa (question_id, report_email, issue_email, flag_qa) values(%s,%s,%s,%s)"
    cursor.execute(sql, (question_id, report_email, issue_email, '1'))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from report_qa where report_email = %s and question_id = %s"
    cursor.execute(sql, (report_email, question_id))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False

def report_wrong_answer_to_db(answer_id, report_email, issue_email): #report_email : 신고자 , issue_email : 답변 올린 사람
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "INSERT INTO report_qa (answer_id, report_email, issue_email, flag_qa) values(%s,%s,%s,%s)"
    cursor.execute(sql, (answer_id, report_email, issue_email, '2'))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from report_qa where report_email = %s and answer_id = %s"
    cursor.execute(sql, (report_email, answer_id))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False

def get_subjects_list_db():
    conn, cursor = db_connect()
    sql = "select * from Subject"
    cursor.execute(sql)
    subjects_list = []
    subject_dict = {}
    records = cursor.fetchall()
    db_close(conn)
    for row in records:
        subject_dict["subject_id"] = row[1]
        subject_dict["subject_name"] = row[3]
        subject_dict["category"] = row[2]
        subjects_list.append(subject_dict)

    if len(records) > 0:
        return True, subjects_list  # extracted_student_json
    else:
        return False  # None


def check_user_email_from_db(u_email):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where userEmail = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (u_email))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True  # extracted_student_json
    else:
        return False  # None


def get_user_reward_from_db(u_email):
    cur_reward = 0

    conn, cursor = db_connect()
    sql = "select reward from User where userEmail=%s"
    cursor.execute(sql, (u_email))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            cur_reward = row[0]

        return cur_reward
    else:
        return cur_reward



def get_all_user_reward_from_db():
    user_reward_data = {}
    user_reward_list = []

    conn, cursor = db_connect()
    sql = "select userEmail, reward from User order by reward DESC limit 5"
    cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            email = row[0]
            reward = row[1]
            user_reward_data = {'email': email, 'reward': reward}
            user_reward_list.append(user_reward_data)
        return user_reward_list
    else:
        return user_reward_list


def get_all_user_info_from_db():
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            email = row[1]
            user_info[email] = row[2]
        return user_info
    else:
        user_info['ryan@gmail.com'] = '123456'
        return user_info


def get_user_info_from_db(u_email):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where userEmail = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (u_email))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:

            is_student = row[3]
            is_solver = row[4]
            user_school_name = row[6]
            user_school_code = row[7]
            user_grade = row[5]
            if is_student == '1' and is_solver == '1':
                role = 'both'
            elif is_student == '1' and is_solver == '0':
                role = 'student'
            elif is_student == '0' and is_solver == '1':
                role = 'solver'
            else:
                role = 'nothing'
            # student_data = {"role" : role, "schoolName": user_school_name, "schoolCode" : user_school_code, "grade" : user_grade}
            # extracted_student_json = json.dumps(student_data)

        return True  # extracted_student_json
    else:
        return False  # None


def is_nickname(nkckname):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where nickname = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (nkckname))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False


def insert_user_db(u_id, u_passwd):  # OK
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    sql = "INSERT INTO User (userEmail, userPass, userRole, userGrade, schoolName, schoolCode) values(%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (u_id, u_passwd, '0', '10',
                   'Texas Highschool', '0001'))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from User where userEmail = %s and userPass = %s"
    cursor.execute(sql, (u_id, u_passwd))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False


def insert_user_db_v2(u_id, u_passwd, nickname):  # OK
    if is_nickname(nickname) == True:
        return False
    else:
        conn, cursor = db_connect()
        # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
        # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
        sql = "INSERT INTO User (userEmail, userPass, userRole, userGrade, schoolName, schoolCode, nickname) values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (u_id, u_passwd, '0', '10',
                             'Texas Highschool', '0001', nickname))
        db_close(conn)

        conn, cursor = db_connect()
        sql = "select * from User where userEmail = %s and userPass = %s"
        cursor.execute(sql, (u_id, u_passwd))
        records = cursor.fetchall()
        db_close(conn)
        if len(records) > 0:
            return True
        else:
            return False

# 2022.01.09
# 회원 탈퇴


def withdraw_user_db(u_id, u_passwd):  # OK
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    sql = "DELETE FROM User WHERE userEmail = %s"
    cursor.execute(sql, (u_id))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from User where userEmail = %s and userPass = %s"
    cursor.execute(sql, (u_id, u_passwd))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return False
    else:
        return True


def append_payment_info_db(email, account, option):
    # print(f'[02/21] account : {account}')
    # print(f'[02/21] option : {option}')
    conn, cursor = db_connect()
    sql = "INSERT INTO payment_account (email, account, payment_option) values(%s,%s,%s)"
    cursor.execute(sql, (email, account, option))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from payment_account where email = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False


def update_payment_info_db(email, account, option):
    # print(f'[03/16] email : {email}')
    conn, cursor = db_connect()
    sql = "select * from payment_account where email = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()
    
    if len(records) > 0:
        if option == '1':
            sql = "update payment_account SET account = %s, payment_option = %s where email = %s"
            cursor.execute(sql, (account, option, email))
        elif option == '2':
            sql = "update payment_account SET account = %s, payment_option = %s where email = %s"
            cursor.execute(sql, (account, option, email))
        
    else:
        append_payment_info_db(email, account, option)

    db_close(conn)


def update_reward_to_DB(email, transaction_reward):
    balanced_reward = 0

    conn, cursor = db_connect()
    sql = "SELECT reward from User where UserEmail = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()

    if len(records) > 0:
        for row in records:
            balanced_reward = row[0]
            break

    future_balanced = float(balanced_reward) - transaction_reward
    # print(f'future_balanced : {future_balanced}')

    sql = "update User SET reward = %s where UserEmail = %s"
    cursor.execute(sql, (future_balanced, email))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "update req_reward SET req_status = 'Completed' where email = %s and req_reward = %s"
    cursor.execute(sql, (email, str(transaction_reward)))
    db_close(conn)


def request_reward_to_admin(email, req_reward):
    balanced_reward = 0

    if int(req_reward) % 5 != 0:
        return False

    origin_calculated_reward = (float(req_reward) * 100) / 102
    calculated_reward = round(origin_calculated_reward, 2)
    print(f'caculated_reward : {calculated_reward}')
    
    conn, cursor = db_connect()
    sql = "SELECT reward from User where UserEmail = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()

    if len(records) > 0:
        for row in records:
            balanced_reward = row[0]
            break

    future_balanced = int(balanced_reward) - int(req_reward)
    print(f'future_balanced : {future_balanced}')
    if future_balanced < 0:
        return False

    sql = "update User SET reward = %s where UserEmail = %s"
    cursor.execute(sql, (future_balanced, email))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "SELECT account, payment_option from payment_account where email = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()

    if len(records) > 0:
        req_status = 'Pending'
        for row in records:
            payment_account = row[0]
            payment_option = row[1]

        sql = "INSERT INTO req_reward (date_time, email, account, payment_option, req_reward, req_status, calculated_reward) values(now(),%s,%s,%s,%s,%s, %s)"
        cursor.execute(sql, (email, payment_account,
                       payment_option, req_reward, req_status, calculated_reward))

    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False


def get_payment_info_db(email):
    payment_timestamp = ''
    payment_email = ''
    payment_account = ''
    payment_option = ''
    payment_req_reward = ''
    payment_req_status = ''

    conn, cursor = db_connect()
    # sql = "SELECT * from req_reward where email = %s"
    # cursor.execute(sql, (email))
    # records = cursor.fetchall()

    # for row in records:
    #     payment_timestamp = str(row[1])
    #     payment_email = row[2]
    #     payment_account = row[3]
    #     payment_option = row[4]
    #     payment_req_reward = row[5]
    #     payment_req_status = row[6]
    user_reward = get_user_reward_db(email)

    sql = "SELECT * from payment_account where email = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()

    for row in records:
        payment_email = row[1]
        payment_account = row[2]
        payment_option = row[3]

    db_close(conn)
    return payment_account, payment_option, user_reward


def get_transaction_info_db(email):
    payment_timestamp = ''
    payment_email = ''
    payment_account = ''
    payment_option = ''
    payment_req_reward = ''
    payment_req_status = ''

    conn, cursor = db_connect()
    sql = "SELECT * from req_reward where email = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()

    for row in records:
        payment_timestamp = str(row[1])
        payment_email = row[2]
        payment_account = row[3]
        payment_option = row[4]
        payment_req_reward = row[5]
        payment_req_status = row[6]
    user_reward = get_user_reward_db(email)

    sql = "SELECT * from payment_account where email = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()

    for row in records:
        payment_email = row[1]
        payment_account = row[2]
        payment_option = row[3]

    db_close(conn)
    return payment_timestamp, payment_account, payment_option, payment_req_reward, payment_req_status, user_reward


def update_user_info_db(email, passwd, role, school_name, school_code, grade):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    sql = "update User SET userRole = %s , SchoolName = %s , SchoolCode = %s , userGrade = %s where userEmail = %s and userPass = %s"

    cursor.execute(sql, (role, school_name, school_code, grade, email, passwd))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from User where userEmail = %s and userPass = %s"
    cursor.execute(sql, (email, passwd))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False


def update_user_info_db_v2(email, passwd, role, school_name, school_code, grade, nickname):
    # if is_nickname(nickname) == True:
    #     return False
    # else:
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    sql = "update User SET userRole = %s , SchoolName = %s , SchoolCode = %s , userGrade = %s,  nickname = %s where userEmail = %s and userPass = %s"

    cursor.execute(
        sql, (role, school_name, school_code, grade, nickname, email, passwd))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from User where userEmail = %s and userPass = %s"
    cursor.execute(sql, (email, passwd))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False


# def get_user_info_db(email, passwd):
#     role = school_name = school_code = grade = ''
#     conn, cursor = db_connect()
#     # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
#     sql = "select * from User where userEmail = %s and userPass = %s"
#     # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
#     cursor.execute(sql, (email, passwd))
#     records = cursor.fetchall()
#     db_close(conn)
#     if len(records) > 0:
#         for row in records:
#             role = row[3]
#             school_name = row[5]
#             school_code = row[6]
#             grade = row[4]

#             # student_data = {"role" : role, "schoolName": user_school_name, "schoolCode" : user_school_code, "grade" : user_grade}
#             # extracted_student_json = json.dumps(student_data)

#     return role, school_name, school_code, grade


def get_user_info_db(email, passwd):
    role = school_name = school_code = grade = ''
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where userEmail = %s and userPass = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (email, passwd))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            role = row[3]
            school_name = row[5]
            school_code = row[6]
            grade = row[4]
            nickname = row[9]
            # student_data = {"role" : role, "schoolName": user_school_name, "schoolCode" : user_school_code, "grade" : user_grade}
            # extracted_student_json = json.dumps(student_data)

    return role, school_name, school_code, grade, nickname

def get_user_info_db_v2(email, passwd):
    role = school_name = school_code = grade = ''
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where userEmail = %s and userPass = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (email, passwd))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            role = row[3]
            school_name = row[5]
            school_code = row[6]
            grade = row[4]
            nickname = row[9]
            # student_data = {"role" : role, "schoolName": user_school_name, "schoolCode" : user_school_code, "grade" : user_grade}
            # extracted_student_json = json.dumps(student_data)

    return role, school_name, school_code, grade, nickname

def get_nickname_info_db(email):
    role = school_name = school_code = grade = ''
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where nickname = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            nickname = row[9]
            # student_data = {"role" : role, "schoolName": user_school_name, "schoolCode" : user_school_code, "grade" : user_grade}
            # extracted_student_json = json.dumps(student_data)
            return nickname
    else:
        return None

def get_user_reward_db(email):
    user_reward = ''
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select reward from User where userEmail = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (email))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            user_reward = row[0]

    return user_reward


def check_password(u_id, u_passwd):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where userEmail = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (u_id))

    records = cursor.fetchall()
    for row in records:
        print(f'user id : {row[1]}')
        print(f'user passwd : {row[2]}')
    db_close(conn)

    if u_id == row[1] and bcrypt.check_password_hash(row[2], u_passwd):
        return True
    else:
        return False


def check_school_code(school_code):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where schoolCode = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (school_code))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False


def check_school_name(school_name):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where schoolCode = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (school_name))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False

def get_email_from_nickname(nickname):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select userEmail from User where nickname = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (nickname))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            return row[0]
    else:
        return None    

def get_user_question_db(email, subject_id, page):
    question_list = list()
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from Question where author_email = %s ORDER by question_id DESC"
    cursor.execute(sql, (email))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            # row[4] : subject_name, row[6] : content
            question_list.append(row[4])
        return True, question_list
    else:
        return False, question_list


def get_question_list_all_db(query_str):
    query_str = list()
    question_list = {'question': query_str}

    if len(query_str) == 0:
        conn, cursor = db_connect()
        # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
        sql = "select * from Question ORDER by question_id DESC"
        cursor.execute(sql)

        records = cursor.fetchall()
        db_close(conn)
        if len(records) > 0:

            for row in records:
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                image_url = row[7]
                recognized_text = row[8]

                # row[4] : subject_name, row[6] : content
                query_str.append(content)
            question_list['question'] = query_str
            return True, question_list
        else:
            return False, question_list
    else:
        return False, question_list


# @@ryan sql 수정
# hasAsnwer 3 & 4 조건 추가 12.01.2021
def query_empty_subject_id_empty_db(query, email, subject_id, page, num, hasAnswer):
    question_list = []
    print('[ query_empty_subject_id_empty_db ]')
    print(f'page : {page}')
    print(f'num : {num}')
    conn, cursor = db_connect()

    if len(page) == 0:
        int_page = 0
    else:
        int_page = int(page)
    if len(num) == 0:
        int_num = 0
    else:
        int_num = int(num)
    if int_page != 0 and int_num != 0:
        total_number = int_page * int_num

    if len(hasAnswer) > 0:
        num_of_answer = int(hasAnswer)
        print(f'num_of_answer : {num_of_answer}')
        if num_of_answer == 4:
            if len(email) == 0:
                sql = "select * from Question where (hasAnswer =%s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, ('0', '1'))
            else:
                sql = "select * from Question where author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                print(f'sql : {sql}')
                cursor.execute(sql, (email, '0', '1'))
        elif num_of_answer == 3:
            if len(email) == 0:
                sql = "select * from Question where (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, ('1', '2'))
            else:
                sql = "select * from Question where author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                print(f'sql : {sql}')
                cursor.execute(sql, (email, '1', '2'))
        elif num_of_answer < 3:
            if len(email) == 0:
                sql = "select * from Question where hasAnswer = %s order by question_id DESC"
                cursor.execute(sql, (hasAnswer))
            else:
                sql = "select * from Question where author_email = %s and hasAnswer = %s order by question_id DESC"
                print(f'sql : {sql}')
                cursor.execute(sql, (email, hasAnswer))
    else:
        if len(email) == 0:
            sql = "select * from Question order by question_id DESC"
            print(f'0_query_0_subject : {sql}')
            cursor.execute(sql)
        else:
            sql = "select * from Question where author_email = %s order by question_id DESC"
            print(f'sql : {sql}')
            cursor.execute(sql, (email))

    records = cursor.fetchall()
    db_close(conn)

    if (len(records) <= int_num) or (len(records) > 0 and int_num == 0):
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[3]
            subject_name = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            nickname = row[13]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, hasAnswer, nickname]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            # print(f'str : {str}')
            question_list.append(str)
    elif len(records) > int_num:
        index = 0
        for row in records:
            if index >= (int_num * (int_page - 1)) and index < (int_num * int_page):
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                hasAnswer = row[10]
                nickname = row[13]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                # print(f'str : {str}')
                question_list.append(str)
            index += 1

    return question_list


def query_empty_subject_id_empty_db_v2(query, email,  subject_id, page, num, hasAnswer):
    question_list = []
    print('[ query_empty_subject_id_empty_db_v2 ]')
    print(f'page : {page}')
    print(f'num : {num}')
    conn, cursor = db_connect()

    if len(page) == 0:
        int_page = 0
    else:
        int_page = int(page)
    if len(num) == 0:
        int_num = 0
    else:
        int_num = int(num)
    if int_page != 0 and int_num != 0:
        total_number = int_page * int_num

    if len(hasAnswer) > 0:
        num_of_answer = int(hasAnswer)
        print(f'num_of_answer : {num_of_answer}')
        if num_of_answer == 4:
            if len(email) == 0:
                sql = "select * from Question where (hasAnswer =%s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, ('0', '1'))
            else:
                sql = "select * from Question where author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                print(f'sql : {sql}')
                cursor.execute(sql, (email, '0', '1'))
        elif num_of_answer == 3:
            if len(email) == 0:
                sql = "select * from Question where (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, ('1', '2'))
            else:
                sql = "select * from Question where author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                print(f'sql : {sql}')
                cursor.execute(sql, (email, '1', '2'))
        elif num_of_answer < 3:
            if len(email) == 0:
                sql = "select * from Question where hasAnswer = %s order by question_id DESC"
                cursor.execute(sql, (hasAnswer))
            else:
                sql = "select * from Question where author_email = %s and hasAnswer = %s order by question_id DESC"
                print(f'sql : {sql}')
                cursor.execute(sql, (email, hasAnswer))
    else:
        if len(email) == 0:
            sql = "select * from Question order by question_id DESC"
            print(f'0_query_0_subject : {sql}')
            cursor.execute(sql)
        else:
            sql = "select * from Question where author_email = %s order by question_id DESC"
            print(f'sql : {sql}')
            cursor.execute(sql, (email))

    records = cursor.fetchall()
    db_close(conn)

    if (len(records) <= int_num) or (len(records) > 0 and int_num == 0):
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[3]
            subject_name = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            nickname = row[13]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, hasAnswer,nickname]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            # print(f'str : {str}')
            question_list.append(str)
    elif len(records) > int_num:
        index = 0
        for row in records:
            if index >= (int_num * (int_page - 1)) and index < (int_num * int_page):
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                hasAnswer = row[10]
                nickname = row[13]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                # print(f'str : {str}')
                question_list.append(str)
            index += 1

    return question_list

def query_empty_subject_id_empty_db_v3(query, email,  subject_id, page, num, hasAnswer): #09.12
    selected_question_id = -1
    isQuestion_id = False
    question_list = []
    answer_list = []
    print('[ query_empty_subject_id_empty_db_v3 ]')
    print(f'email : {email}')
    
    conn, cursor = db_connect()

    if len(page) == 0:
        int_page = 0
    else:
        int_page = int(page)
    if len(num) == 0:
        int_num = 0
    else:
        int_num = int(num)
    if int_page != 0 and int_num != 0:
        total_number = int_page * int_num

    if len(hasAnswer) > 0:
        num_of_answer = int(hasAnswer)
        print(f'num_of_answer : {num_of_answer}')
        if num_of_answer == 4:
            if len(email) == 0:
                sql = "select * from Question where (hasAnswer =%s or hasAnswer = %s) order by question_id DESC"
                print(f'1. sql : {sql}')
                cursor.execute(sql, ('0', '1'))
            else:
                sql = "select * from Question where author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                print(f'2. sql : {sql}')
                cursor.execute(sql, (email, '0', '1'))
        elif num_of_answer == 3:
            if len(email) == 0:
                sql = "select * from Question where (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                print(f'3. sql : {sql}')
                cursor.execute(sql, ('1', '2'))
            else:
                sql = "select * from Question where author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                print(f'4. sql : {sql}')
                cursor.execute(sql, (email, '1', '2'))
        elif num_of_answer < 3:
            if len(email) == 0:
                sql = "select * from Question where hasAnswer = %s order by question_id DESC"
                print(f'5. sql : {sql}')
                cursor.execute(sql, (hasAnswer))
            else:
                sql = "select * from Question where author_email = %s and hasAnswer = %s order by question_id DESC"
                print(f'6. sql : {sql}')
                cursor.execute(sql, (email, hasAnswer))
    else:
        if len(email) == 0:
            sql = "select * from Question order by question_id DESC"
            print(f'7. sql : {sql}')
            cursor.execute(sql)
        else:
            sql = "select * from Question where author_email = %s order by question_id DESC"
            print(f'8. sql : {sql}')
            cursor.execute(sql, (email))

    records = cursor.fetchall()
    db_close(conn)
    
    if len(records) == 0:
        isQuestion_id = False
    else:
        isQuestion_id = True
    if (len(records) <= int_num) or (len(records) > 0 and int_num == 0):
        print('(len(records) <= int_num) or (len(records) > 0 and int_num == 0):')
        for row in records:
            question_id = row[0]
            author_email = row[1]
            print(f'author_email : {author_email}')
            subject_id = row[3]
            subject_name = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            nickname = row[13]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, hasAnswer,nickname]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            print(f'str : {str}')
            question_list.append(str)
    elif len(records) > int_num:
        print('len(records) > int_num:')
        index = 0
        for row in records:
            if index >= (int_num * (int_page - 1)) and index < (int_num * int_page):
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                hasAnswer = row[10]
                nickname = row[13]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                print(f'str : {str}')
                question_list.append(str)
            index += 1

    conn, cursor = db_connect()

    sql_start = "select * from Answer "
    if len(email) == 0:
        option_1 = "where (re_recog LIKE '%" + query + "%' "
    else:
        option_1 = "where author_email = '" + email + \
            "' and (re_recog LIKE '%" + query + "%' "
    option_2 = "OR re_con LIKE '%" + query + "%') "

    if len(num) == 0:
        sql_end = "order by question_id DESC"
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    else:
        sql_end = "order by question_id DESC LIMIT " + num
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from Answer where question_id = %s ORDER BY answer_id"
    # cursor.execute(sql, (question_id))

    records = cursor.fetchall()
    db_close(conn)

    question_id_list = []
    if len(records) > 0:
        answer_str_data = []
        answer_str_list = []
        for row in records:
            answer_id = row[0]
            selected_question_id = row[1]
            print(f'selected_question_id: {selected_question_id}')
            if len(question_list) == 0:
                question_id = selected_question_id
                question_id_list.append(selected_question_id)
            author_email = row[2]
            content = row[3]
            selected = row[4]
            created = row[5]
            updated = row[6]
            image_url = row[7]
            recognized_text = row[8]
            nickname = row[11]
            answer_str_data = [answer_id, selected_question_id, author_email, content,
                               selected, created, updated, image_url, recognized_text, nickname]

            # row[4] : subject_name, row[6] : content
            answer_list.append(make_answer_dict_str(answer_str_data))
        # answer_str_list.append(answer_str_data)
        # print(f'answer_str_list : {answer_str_list}')
        # # answer_list['answer'] = make_answer_dict_str(answer_str_list)
        # for answer_data in answer_str_list:
        #     answer_list.append(make_answer_dict_str(answer_data))

    print(f'len of answer_list : {len(answer_list) }')
    print(f'len of question_list : {len(question_list)}')
    print(f'len of question_id_list : {len(question_id_list)}')
    if isQuestion_id == True and len(question_list) == 0 and len(answer_list) != 0:
        for index_question_id in question_id_list:
            conn, cursor = db_connect()
            print(f'index_question_id : {index_question_id}')
            sql_again_question = "select * from Question where question_id = " + index_question_id
            cursor.execute(sql_again_question)
            again_question_records = cursor.fetchall()
            db_close(conn)
            print(
                f'len of records [question_list == 0]: {len(again_question_records) }')
            if len(again_question_records) > 0:
                query_str_data = []
                question_list = []
                for again_question_row in again_question_records:
                    question_id = again_question_row[0]
                    print(f'Again question_id: {question_id}')
                    author_email = again_question_row[1]
                    subject_id = again_question_row[3]
                    subject_name = again_question_row[2]
                    category = again_question_row[4]
                    content = again_question_row[5]
                    created = again_question_row[6]
                    updated = again_question_row[7]
                    image_url = again_question_row[8]
                    recognized_text = again_question_row[9]
                    hasAnswer = again_question_row[10]
                    nickname = again_question_row[13]
                    query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                      content, created, updated, image_url, recognized_text, hasAnswer,nickname]
                    print(f'Again query_str_data : {query_str_data}')
                    # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                    str = make_question_dict_str(query_str_data)
                    print(f'str : {str}')
                    question_list.append(str)

    return question_list, answer_list
# @@ryan : sql 수정 (hasAnswer)
# hasAsnwer 3 & 4 조건 추가 12.01.2021
def query_empty_subject_id_NOT_empty_db(query, email, subject_id, page, num, hasAnswer):
    question_list = []
    print('[ query_empty_subject_id_NOT_empty_db ]')
    conn, cursor = db_connect()

    if len(page) == 0:
        int_page = 0
    else:
        int_page = int(page)
    if len(num) == 0:
        int_num = 0
    else:
        int_num = int(num)

    print(f'page : {page}')
    print(f'num : {num}')
    if int_page != 0 and int_num != 0:
        total_number = int_page * int_num

    if len(hasAnswer) > 0:
        num_of_answer = int(hasAnswer)
        print(f'num_of_answer : {num_of_answer}')
        if num_of_answer == 4:
            if len(email) == 0:
                sql = "select * from Question where subject_id = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, (subject_id, '0', '1'))
            else:
                sql = "select * from Question where subject_id = %s and author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, (subject_id, email, '0', '1'))
        elif num_of_answer == 3:
            if len(email) == 0:
                sql = "select * from Question where subject_id = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, (subject_id, '1', '2'))
            else:
                sql = "select * from Question where subject_id = %s and author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, (subject_id, email, '1', '2'))
        elif num_of_answer < 3:
            if len(email) == 0:
                sql = "select * from Question where subject_id = %s and hasAnswer = %s order by question_id DESC"
                cursor.execute(sql, (subject_id, hasAnswer))
            else:
                sql = "select * from Question where subject_id = %s and author_email = %s and hasAnswer = %s order by question_id DESC"
                cursor.execute(sql, (subject_id, email, hasAnswer))
    else:
        print(f'len(hasAnswer) == 0')
        if len(email) == 0:
            sql = "select * from Question where subject_id = %s order by question_id DESC"
            cursor.execute(sql, (subject_id))
        else:
            sql = "select * from Question where subject_id = %s and author_email = %s order by question_id DESC"
            cursor.execute(sql, (subject_id, email))

    records = cursor.fetchall()
    db_close(conn)

    if (len(records) <= int_num) or (len(records) > 0 and int_num == 0):
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[3]
            subject_name = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            nickname = row[13]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, hasAnswer, nickname]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            # print(f'str : {str}')
            question_list.append(str)
    elif len(records) > int_num:
        index = 0
        for row in records:
            if index >= (int_num * (int_page - 1)) and index < (int_num * int_page):
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                hasAnswer = row[10]
                nickname = row[13]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                # print(f'str : {str}')
                question_list.append(str)
            index += 1
    return question_list


def query_empty_subject_id_NOT_empty_db_v2(query, email, subject_id, page, num, hasAnswer):
    question_list = []
    print('[ query_empty_subject_id_NOT_empty_db ]')
    conn, cursor = db_connect()

    if len(page) == 0:
        int_page = 0
    else:
        int_page = int(page)
    if len(num) == 0:
        int_num = 0
    else:
        int_num = int(num)

    print(f'page : {page}')
    print(f'num : {num}')
    if int_page != 0 and int_num != 0:
        total_number = int_page * int_num

    if len(hasAnswer) > 0:
        num_of_answer = int(hasAnswer)
        print(f'num_of_answer : {num_of_answer}')
        if num_of_answer == 4:
            if len(email) == 0:
                sql = "select * from Question where subject_id = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, (subject_id, '0', '1'))
            else:
                sql = "select * from Question where subject_id = %s and author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, (subject_id, email, '0', '1'))
        elif num_of_answer == 3:
            if len(email) == 0:
                sql = "select * from Question where subject_id = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, (subject_id, '1', '2'))
            else:
                sql = "select * from Question where subject_id = %s and author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                cursor.execute(sql, (subject_id, email, '1', '2'))
        elif num_of_answer < 3:
            if len(email) == 0:
                sql = "select * from Question where subject_id = %s and hasAnswer = %s order by question_id DESC"
                cursor.execute(sql, (subject_id, hasAnswer))
            else:
                sql = "select * from Question where subject_id = %s and author_email = %s and hasAnswer = %s order by question_id DESC"
                cursor.execute(sql, (subject_id, email, hasAnswer))
    else:
        print(f'len(hasAnswer) == 0')
        if len(email) == 0:
            sql = "select * from Question where subject_id = %s order by question_id DESC"
            cursor.execute(sql, (subject_id))
        else:
            sql = "select * from Question where subject_id = %s and author_email = %s order by question_id DESC"
            cursor.execute(sql, (subject_id, email))

    records = cursor.fetchall()
    db_close(conn)

    if (len(records) <= int_num) or (len(records) > 0 and int_num == 0):
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[3]
            subject_name = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            recognized_text = row[11]
            re_con = row[12]
            nickname = row[13]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, hasAnswer, nickname]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            # print(f'str : {str}')
            question_list.append(str)
    elif len(records) > int_num:
        index = 0
        for row in records:
            if index >= (int_num * (int_page - 1)) and index < (int_num * int_page):
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                hasAnswer = row[10]
                nickname = row[13]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                # print(f'str : {str}')
                question_list.append(str)
            index += 1
    return question_list


def query_empty_subject_id_NOT_empty_db(query, email, subject_ids, page, num, hasAnswer):
    question_list = []
    print('[ query_empty_subject_id_NOT_empty_db ]')
    conn, cursor = db_connect()

    if len(page) == 0:
        int_page = 0
    else:
        int_page = int(page)
    if len(num) == 0:
        int_num = 0
    else:
        int_num = int(num)

    print(f'page : {page}')
    print(f'num : {num}')
    print(f'n_hasAnswer : {len(hasAnswer)}')
    if int_page != 0 and int_num != 0:
        total_number = int_page * int_num

    if len(hasAnswer) > 0:
        num_of_answer = int(hasAnswer)
        print(f'num_of_answer : {num_of_answer}')
        flag = False
        front_sql = "select * from Question where "
        n_subject_ids = len(subject_ids)
        middle_sql = ""
        if n_subject_ids == 1:
            middle_sql = " subject_id = '" + subject_ids[0] + "' and "
        elif n_subject_ids > 1:
            i = 0

            for i in range(n_subject_ids):
                middle_sql += " subject_id = '" + subject_ids[i] + "' OR "

        if num_of_answer == 4:
            if len(email) == 0:
                # sql = "select * from Question where subject_id = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                sql = front_sql + middle_sql + \
                    " (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                print(f'[01/29_case_1] sql : {sql}')
                cursor.execute(sql, ('0', '1'))
            else:
                # sql = "select * from Question where subject_id = %s and author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                sql = front_sql + middle_sql + \
                    "author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                print(f'[01/29_case_2] sql : {sql}')
                cursor.execute(sql, (email, '0', '1'))
        elif num_of_answer == 3:
            if len(email) == 0:
                # sql = "select * from Question where subject_id = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                sql = front_sql + middle_sql + \
                    "(hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                print(f'[01/29_case_3] sql : {sql}')
                cursor.execute(sql, ('1', '2'))
            else:
                # sql = "select * from Question where subject_id = %s and author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                sql = front_sql + middle_sql + \
                    "author_email = %s and (hasAnswer = %s or hasAnswer = %s) order by question_id DESC"
                print(f'[01/29_case_4] sql : {sql}')
                cursor.execute(sql, (email, '1', '2'))
        elif num_of_answer < 3:
            if len(email) == 0:
                # sql = "select * from Question where subject_id = %s and hasAnswer = %s order by question_id DESC"
                sql = front_sql + middle_sql + "hasAnswer = %s order by question_id DESC"
                print(f'[01/29_case_5] sql : {sql}')
                cursor.execute(sql, (hasAnswer))
            else:
                # sql = "select * from Question where subject_id = %s and author_email = %s and hasAnswer = %s order by question_id DESC"
                sql = front_sql + middle_sql + \
                    "author_email = %s and hasAnswer = %s order by question_id DESC"
                print(f'[01/29_case_6] sql : {sql}')
                cursor.execute(sql, (email, hasAnswer))
    else:
        print(f'len(hasAnswer) == 0')
        middle_sql = ""
        front_sql = "select * from Question where "
        n_subject_ids = len(subject_ids)
        if n_subject_ids == 1:
            middle_sql = " subject_id = '" + subject_ids[0] + "' "
        elif n_subject_ids > 1:
            i = 1
            middle_sql = " subject_id = '" + subject_ids[0] + "' "
            while i < n_subject_ids:
                middle_sql += " OR subject_id = '" + subject_ids[i] + "' "
                i += 1

        if len(email) == 0:
            # sql = "select * from Question where subject_id = %s order by question_id DESC"
            sql = front_sql + middle_sql + "order by question_id DESC"
            print(f'[01/29_case_7] sql : {sql}')
            cursor.execute(sql)
        else:
            # sql = "select * from Question where subject_id = %s and author_email = %s order by question_id DESC"
            sql = front_sql + middle_sql + "and author_email = %s order by question_id DESC"
            print(f'[01/29_case_8] sql : {sql}')
            cursor.execute(sql, (email))

    records = cursor.fetchall()
    db_close(conn)

    if (len(records) <= int_num) or (len(records) > 0 and int_num == 0):
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[3]
            subject_name = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            nickname = row[13]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, hasAnswer, nickname]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            # print(f'str : {str}')
            question_list.append(str)
    elif len(records) > int_num:
        index = 0
        for row in records:
            if index >= (int_num * (int_page - 1)) and index < (int_num * int_page):
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                hasAnswer = row[10]
                nickname = row[13]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                # print(f'str : {str}')
                question_list.append(str)
            index += 1
    return question_list


def converted_special_char(data):
    str = data

    str = str.replace('\n', '')
    # str = str.strip('\\')
    str = str.replace('\\', '')
    str = str.replace('\\', '')
    # regex = re.compile((r'\\'))
    # conv_txt = regex.sub("\\", "", str)
    text = re.sub(
        '<>#/\:$.@*\"※~&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》', '', str)

    # print(f'text : {text}')
    text = text.replace('<latex>', '')
    text = text.replace('</latex>', '')
    return text

# hasAsnwer 3 & 4 조건 추가 12.01.2021


def query_NOT_empty_subject_id_empty_db(origin_query, email, subject_id, page, num, hasAnswer):
    selected_question_id = -1
    question_list = []
    answer_list = []
    print('[ query_NOT_empty_subject_id_empty_db ]')

    conn, cursor = db_connect()
    if len(page) == 0:
        int_page = 1
    else:
        int_page = int(page)
    if len(num) == 0:
        int_num = 0
    else:
        int_num = int(num)

    print(f'page : {page}')
    print(f'num : {num}')
    if int_num != 0:
        total_number = int_page * int_num
    else:
        total_number = 0

    query = converted_special_char(origin_query)
    print(f'conv_query : {query}')
    print(f'hasAnswer : {hasAnswer}')

    if len(hasAnswer) > 0:
        num_of_answer = int(hasAnswer)
        print(f'num_of_answer : {num_of_answer}')
        if num_of_answer == 4:
            if len(email) > 0:
                sql = "select * from Question a where a.author_email = '" + email + "' and (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
        elif num_of_answer == 3:
            if len(email) > 0:
                sql = "select * from Question a where a.author_email = '" + email + "' and (a.hasAnswer = '1' or a.hasAnswer = '2') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where (a.hasAnswer = '1' or a.hasAnswer = '2') and " + \
                    "(a.re_recog LIKE '%" + query + "' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
        elif num_of_answer < 3:
            if len(email) > 0:
                sql = "select * from Question a where a.author_email = '" + email + "' and a.hasAnswer = " + hasAnswer + " and " + \
                    "(a.re_recog LIKE '%" + query + "' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where a.hasAnswer = %s and " + \
                    "(a.re_recog LIKE '%" + query + "' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql, (hasAnswer))
    else:
        print(f'len(hasAnswer) == 0')
        if len(email) > 0:
            sql = "select * from Question a where a.author_email = '" + email + "' and " + \
                "(a.re_recog LIKE '%" + query + "' OR a.re_con LIKE '%" + \
                query + "%') order by a.question_id DESC "
            print(f'email sql : {sql}')
            cursor.execute(sql)
        else:
            sql = "select * from Question a where " + \
                "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                query + "%') order by a.question_id DESC"
            cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)
    print(f'len of records : {len(records) }')

    if (len(records) <= int_num) or (len(records) > 0 and int_num == 0):
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[3]
            subject_name = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            nickname = row[13]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, hasAnswer,nickname]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            print(f'str : {str}')
            question_list.append(str)
    elif len(records) > int_num:
        index = 0
        for row in records:
            if index >= (int_num * (int_page - 1)) and index < (int_num * int_page):
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                hasAnswer = row[10]
                nickname = row[13]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                print(f'str : {str}')
                question_list.append(str)
            index += 1
    conn, cursor = db_connect()

    sql_start = "select * from Answer "
    if len(email) == 0:
        option_1 = "where (re_recog LIKE '%" + query + "%' "
    else:
        option_1 = "where author_email = '" + email + \
            "' and (re_recog LIKE '%" + query + "%' "
    option_2 = "OR re_con LIKE '%" + query + "%') "

    if len(num) == 0:
        sql_end = "order by question_id DESC"
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    else:
        sql_end = "order by question_id DESC LIMIT " + num
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from Answer where question_id = %s ORDER BY answer_id"
    # cursor.execute(sql, (question_id))

    records = cursor.fetchall()
    db_close(conn)

    question_id_list = []
    if len(records) > 0:
        answer_str_data = []
        answer_str_list = []
        for row in records:
            answer_id = row[0]
            selected_question_id = row[1]
            print(f'selected_question_id: {selected_question_id}')
            if len(question_list) == 0:
                question_id = selected_question_id
                question_id_list.append(selected_question_id)
            author_email = row[2]
            content = row[3]
            selected = row[4]
            created = row[5]
            updated = row[6]
            image_url = row[7]
            recognized_text = row[8]
            nickname = row[11]
            answer_str_data = [answer_id, selected_question_id, author_email, content,
                               selected, created, updated, image_url, recognized_text, nickname]

            # row[4] : subject_name, row[6] : content
            answer_list.append(make_answer_dict_str(answer_str_data))
        # answer_str_list.append(answer_str_data)
        # print(f'answer_str_list : {answer_str_list}')
        # # answer_list['answer'] = make_answer_dict_str(answer_str_list)
        # for answer_data in answer_str_list:
        #     answer_list.append(make_answer_dict_str(answer_data))

    print(f'len of answer_list : {len(answer_list) }')
    print(f'len of question_list : {len(question_list)}')
    print(f'len of question_id_list : {len(question_id_list)}')
    if len(question_list) == 0 and len(answer_list) != 0:
        for index_question_id in question_id_list:
            conn, cursor = db_connect()
            print(f'index_question_id : {index_question_id}')
            sql_again_question = "select * from Question where question_id = " + index_question_id
            cursor.execute(sql_again_question)
            again_question_records = cursor.fetchall()
            db_close(conn)
            print(
                f'len of records [question_list == 0]: {len(again_question_records) }')
            if len(again_question_records) > 0:
                query_str_data = []
                question_list = []
                for again_question_row in again_question_records:
                    question_id = again_question_row[0]
                    print(f'Again question_id: {question_id}')
                    author_email = again_question_row[1]
                    subject_id = again_question_row[3]
                    subject_name = again_question_row[2]
                    category = again_question_row[4]
                    content = again_question_row[5]
                    created = again_question_row[6]
                    updated = again_question_row[7]
                    image_url = again_question_row[8]
                    recognized_text = again_question_row[9]
                    hasAnswer = again_question_row[10]
                    nickname = again_question_row[13]
                    query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                      content, created, updated, image_url, recognized_text, hasAnswer,nickname]
                    print(f'Again query_str_data : {query_str_data}')
                    # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                    str = make_question_dict_str(query_str_data)
                    print(f'str : {str}')
                    question_list.append(str)

    return question_list, answer_list

###### -------------------------- 03.14 ---------------- ########


def query_NOT_empty_subject_id_empty_db_v2(origin_query, email, subject_id, page, num, hasAnswer):
    selected_question_id = -1
    question_list = []
    answer_list = []
    print('[ query_NOT_empty_subject_id_empty_db ]')

    conn, cursor = db_connect()
    if len(page) == 0:
        int_page = 1
    else:
        int_page = int(page)
    if len(num) == 0:
        int_num = 0
    else:
        int_num = int(num)

    print(f'page : {page}')
    print(f'num : {num}')
    if int_num != 0:
        total_number = int_page * int_num
    else:
        total_number = 0

    query = converted_special_char(origin_query)
    print(f'conv_query : {query}')
    print(f'hasAnswer : {hasAnswer}')

    if len(hasAnswer) > 0:
        num_of_answer = int(hasAnswer)
        print(f'num_of_answer : {num_of_answer}')
        if num_of_answer == 4:
            if len(email) > 0:
                sql = "select * from Question a where a.author_email = '" + email + "' and (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
        elif num_of_answer == 3:
            if len(email) > 0:
                sql = "select * from Question a where a.author_email = '" + email + "' and (a.hasAnswer = '1' or a.hasAnswer = '2') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where (a.hasAnswer = '1' or a.hasAnswer = '2') and " + \
                    "(a.re_recog LIKE '%" + query + "' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
        elif num_of_answer < 3:
            if len(email) > 0:
                sql = "select * from Question a where a.author_email = '" + email + "' and a.hasAnswer = " + hasAnswer + " and " + \
                    "(a.re_recog LIKE '%" + query + "' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where a.hasAnswer = %s and " + \
                    "(a.re_recog LIKE '%" + query + "' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql, (hasAnswer))
    else:
        print(f'len(hasAnswer) == 0')
        if len(email) > 0:
            sql = "select * from Question a where a.author_email = '" + email + "' and " + \
                "(a.re_recog LIKE '%" + query + "' OR a.re_con LIKE '%" + \
                query + "%') order by a.question_id DESC "
            print(f'email sql : {sql}')
            cursor.execute(sql)
        else:
            sql = "select * from Question a where " + \
                "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                query + "%') order by a.question_id DESC"
            cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)
    print(f'len of records : {len(records) }')

    if (len(records) <= int_num) or (len(records) > 0 and int_num == 0):
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[3]
            subject_name = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            nickname = row[13]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, hasAnswer, nickname]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            print(f'str : {str}')
            question_list.append(str)
    elif len(records) > int_num:
        index = 0
        for row in records:
            if index >= (int_num * (int_page - 1)) and index < (int_num * int_page):
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                hasAnswer = row[10]
                nickname = row[13]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                print(f'str : {str}')
                question_list.append(str)
            index += 1
    conn, cursor = db_connect()

    sql_start = "select * from Answer "
    if len(email) == 0:
        option_1 = "where (re_recog LIKE '%" + query + "%' "
    else:
        option_1 = "where author_email = '" + email + \
            "' and (re_recog LIKE '%" + query + "%' "
    option_2 = "OR re_con LIKE '%" + query + "%') "

    if len(num) == 0:
        sql_end = "order by question_id DESC"
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    else:
        sql_end = "order by question_id DESC LIMIT " + num
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from Answer where question_id = %s ORDER BY answer_id"
    # cursor.execute(sql, (question_id))

    records = cursor.fetchall()
    db_close(conn)

    question_id_list = []
    if len(records) > 0:
        answer_str_data = []
        answer_str_list = []
        for row in records:
            answer_id = row[0]
            selected_question_id = row[1]
            print(f'selected_question_id: {selected_question_id}')
            if len(question_list) == 0:
                question_id = selected_question_id
                question_id_list.append(selected_question_id)
            author_email = row[2]
            content = row[3]
            selected = row[4]
            created = row[5]
            updated = row[6]
            image_url = row[7]
            recognized_text = row[8]
            nickname = row[11]
            answer_str_data = [answer_id, selected_question_id, author_email, content,
                               selected, created, updated, image_url, recognized_text, nickname]

            # row[4] : subject_name, row[6] : content
            answer_list.append(make_answer_dict_str(answer_str_data))
        # answer_str_list.append(answer_str_data)
        # print(f'answer_str_list : {answer_str_list}')
        # # answer_list['answer'] = make_answer_dict_str(answer_str_list)
        # for answer_data in answer_str_list:
        #     answer_list.append(make_answer_dict_str(answer_data))

    print(f'len of answer_list : {len(answer_list) }')
    print(f'len of question_list : {len(question_list)}')
    print(f'len of question_id_list : {len(question_id_list)}')
    if len(question_list) == 0 and len(answer_list) != 0:
        for index_question_id in question_id_list:
            conn, cursor = db_connect()
            print(f'index_question_id : {index_question_id}')
            sql_again_question = "select * from Question where question_id = " + index_question_id
            cursor.execute(sql_again_question)
            again_question_records = cursor.fetchall()
            db_close(conn)
            print(
                f'len of records [question_list == 0]: {len(again_question_records) }')
            if len(again_question_records) > 0:
                query_str_data = []
                question_list = []
                for again_question_row in again_question_records:
                    question_id = again_question_row[0]
                    print(f'Again question_id: {question_id}')
                    author_email = again_question_row[1]
                    subject_id = again_question_row[3]
                    subject_name = again_question_row[2]
                    category = again_question_row[4]
                    content = again_question_row[5]
                    created = again_question_row[6]
                    updated = again_question_row[7]
                    image_url = again_question_row[8]
                    recognized_text = again_question_row[9]
                    hasAnswer = again_question_row[10]
                    nickname = again_question_row[13]
                    query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                      content, created, updated, image_url, recognized_text, hasAnswer,nickname]
                    print(f'Again query_str_data : {query_str_data}')
                    # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                    str = make_question_dict_str(query_str_data)
                    print(f'str : {str}')
                    question_list.append(str)

    return question_list, answer_list

# hasAsnwer 3 & 4 조건 추가 12.01.2021


def query_NOT_empty_subject_id_NOT_empty_db(origin_query, email, subject_id, page, num, hasAnswer):
    question_list = []
    answer_list = []
    print('[ query_NOT_empty_subject_id_NOT_empty_db ]')
    conn, cursor = db_connect()

    query = converted_special_char(origin_query)
    print(f'conv_query : {query}')
    if len(page) == 0:
        int_page = 1
    else:
        int_page = int(page)
    if len(num) == 0:
        int_num = 0
    else:
        int_num = int(num)

    print(f'page : {page}')
    print(f'num : {num}')
    if int_num != 0:
        total_number = int_page * int_num
    else:
        total_number = 0

    if len(hasAnswer) > 0:
        num_of_answer = int(hasAnswer)

        if num_of_answer == 4:
            if len(email) > 0:
                sql = "select * from Question a where a.subject_id = '" + subject_id + "' and a.author_email = '" + email + "' and (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where a.subject_id = '" + subject_id + "' and (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
        elif num_of_answer == 3:
            if len(email) > 0:
                sql = "select * from Question a where a.subject_id = '" + subject_id + "' and a.author_email = '" + email + "' and (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where and a.subject_id = '" + subject_id + "' and (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
        elif num_of_answer < 3:
            if len(email) > 0:
                sql = "select * from Question a where a.subject_id = '" + subject_id + "' and a.author_email = '" + email + "' and a.hasAnswer = " + hasAnswer + " and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where a.subject_id = '" + subject_id + "' and a.hasAnswer = " + hasAnswer + " and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
    else:
        print(f'len(hasAnswer) == 0')
        if len(email) > 0:
            sql = "select * from Question a where a.subject_id = '" + subject_id + "' and a.author_email = '" + email + "'" + \
                "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                query + "%') order by a.question_id DESC"
            print(f'email sql : {sql}')
            cursor.execute(sql)
        else:
            print(f'num : {num}')
            print(f'type(num) : {type(num)}')
            sql = "select * from Question a where a.subject_id = '" + subject_id + "' and " + \
                "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                query + "%') order by a.question_id DESC"
            print(f'default sql : {sql}')
            cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)

    if (len(records) <= int_num) or (len(records) > 0 and int_num == 0):
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[3]
            subject_name = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            nickname = row[13]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, hasAnswer,nickname]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            print(f'str : {str}')
            question_list.append(str)
    elif len(records) > int_num:
        index = 0
        for row in records:
            if index >= (int_num * (int_page - 1)) and index < (int_num * int_page):
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                hasAnswer = row[10]
                nickname = row[13]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                print(f'str : {str}')
                question_list.append(str)
            index += 1

    conn, cursor = db_connect()

    sql_start = "select * from Answer "
    if len(email) == 0:
        option_1 = "where (re_recog LIKE '%" + query + "%' "
    else:
        option_1 = "where author_email = '" + email + \
            "' and (re_recog LIKE '%" + query + "%' "
    option_2 = "OR re_con LIKE '%" + query + "%') "

    if len(num) == 0:
        sql_end = "order by question_id DESC"
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    else:
        sql_end = "order by question_id DESC LIMIT " + num
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from Answer where question_id = %s ORDER BY answer_id"
    # cursor.execute(sql, (question_id))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        answer_str_data = []
        answer_str_list = []
        for row in records:
            answer_id = row[0]
            question_id = row[1]
            author_email = row[2]
            content = row[3]
            selected = row[4]
            created = row[5]
            updated = row[6]
            image_url = row[7]
            recognized_text = row[8]
            nickname = row[11]
            answer_str_data = [answer_id, question_id, author_email, content,
                               selected, created, updated, image_url, recognized_text, nickname]

            # row[4] : subject_name, row[6] : content
        answer_list.append(make_answer_dict_str(answer_str_data))
        # answer_str_list.append(answer_str_data)
        # print(f'answer_str_list : {answer_str_list}')
        # # answer_list['answer'] = make_answer_dict_str(answer_str_list)
        # for answer_data in answer_str_list:
        #     answer_list.append(make_answer_dict_str(answer_data))

    return question_list, answer_list


def query_NOT_empty_subject_id_NOT_empty_db_v2(origin_query, email, subject_id, page, num, hasAnswer):
    question_list = []
    answer_list = []
    print('[ query_NOT_empty_subject_id_NOT_empty_db_v2 ]')
    conn, cursor = db_connect()

    query = converted_special_char(origin_query)
    print(f'conv_query : {query}')
    if len(page) == 0:
        int_page = 1
    else:
        int_page = int(page)
    if len(num) == 0:
        int_num = 0
    else:
        int_num = int(num)

    print(f'page : {page}')
    print(f'num : {num}')
    if int_num != 0:
        total_number = int_page * int_num
    else:
        total_number = 0

    if len(hasAnswer) > 0:
        num_of_answer = int(hasAnswer)

        if num_of_answer == 4:
            if len(email) > 0:
                sql = "select * from Question a where a.subject_id = '" + subject_id + "' and a.author_email = '" + email + "' and (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where a.subject_id = '" + subject_id + "' and (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
        elif num_of_answer == 3:
            if len(email) > 0:
                sql = "select * from Question a where a.subject_id = '" + subject_id + "' and a.author_email = '" + email + "' and (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where and a.subject_id = '" + subject_id + "' and (a.hasAnswer = '0' or a.hasAnswer = '1') and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
        elif num_of_answer < 3:
            if len(email) > 0:
                sql = "select * from Question a where a.subject_id = '" + subject_id + "' and a.author_email = '" + email + "' and a.hasAnswer = " + hasAnswer + " and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
            else:
                sql = "select * from Question a where a.subject_id = '" + subject_id + "' and a.hasAnswer = " + hasAnswer + " and " + \
                    "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                    query + "%') order by a.question_id DESC"
                cursor.execute(sql)
    else:
        print(f'len(hasAnswer) == 0')
        if len(email) > 0:
            sql = "select * from Question a where a.subject_id = '" + subject_id + "' and a.author_email = '" + email + "'" + \
                "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                query + "%') order by a.question_id DESC"
            print(f'email sql : {sql}')
            cursor.execute(sql)
        else:
            print(f'num : {num}')
            print(f'type(num) : {type(num)}')
            sql = "select * from Question a where a.subject_id = '" + subject_id + "' and " + \
                "(a.re_recog LIKE '%" + query + "%' OR a.re_con LIKE '%" + \
                query + "%') order by a.question_id DESC"
            print(f'default sql : {sql}')
            cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)

    if (len(records) <= int_num) or (len(records) > 0 and int_num == 0):
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[3]
            subject_name = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            nickname = row[13]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, hasAnswer, nickname]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            print(f'str : {str}')
            question_list.append(str)
    elif len(records) > int_num:
        index = 0
        for row in records:
            if index >= (int_num * (int_page - 1)) and index < (int_num * int_page):
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                hasAnswer = row[10]
                nickname = row[13]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                print(f'str : {str}')
                question_list.append(str)
            index += 1

    conn, cursor = db_connect()

    sql_start = "select * from Answer "
    if len(email) == 0:
        option_1 = "where (re_recog LIKE '%" + query + "%' "
    else:
        option_1 = "where author_email = '" + email + \
            "' and (re_recog LIKE '%" + query + "%' "
    option_2 = "OR re_con LIKE '%" + query + "%') "

    if len(num) == 0:
        sql_end = "order by question_id DESC"
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    else:
        sql_end = "order by question_id DESC LIMIT " + num
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from Answer where question_id = %s ORDER BY answer_id"
    # cursor.execute(sql, (question_id))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        answer_str_data = []
        answer_str_list = []
        for row in records:
            answer_id = row[0]
            question_id = row[1]
            author_email = row[2]
            content = row[3]
            selected = row[4]
            created = row[5]
            updated = row[6]
            image_url = row[7]
            recognized_text = row[8]
            nickname = row[11]
            answer_str_data = [answer_id, question_id, author_email, content,
                               selected, created, updated, image_url, recognized_text, nickname]

            # row[4] : subject_name, row[6] : content
        answer_list.append(make_answer_dict_str(answer_str_data))
        # answer_str_list.append(answer_str_data)
        # print(f'answer_str_list : {answer_str_list}')
        # # answer_list['answer'] = make_answer_dict_str(answer_str_list)
        # for answer_data in answer_str_list:
        #     answer_list.append(make_answer_dict_str(answer_data))

    return question_list, answer_list


def get_question_ids_list_db(question_ids, number_question_ids):
    print('[ get_question_ids_list_db ]')
    query_str = list()
    question_list = []

    print(f'question_ids : {question_ids}')
    print(f'number_question_ids : {number_question_ids}')

    if number_question_ids == 0:
        sql = "select * from Question order by question_id DESC"
        conn, cursor = db_connect()
        cursor.execute(sql)
        records = cursor.fetchall()
        db_close(conn)
        if len(records) > 0:
            # query_str_data = []
            # query_str_list = []
            for row in records:
                question_id = row[0]
                author_email = row[1]
                subject_id = row[3]
                subject_name = row[2]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                hasAnswer = row[10]
                nickname = row[13]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                print(f'str : {str}')
                question_list.append(str)
        return True, question_list
    else:
        for ids in question_ids:
            # ids = question_ids[0]
            sql_start = "select * from Question"
            sql_content = ' where '
            sql_content = sql_content + "question_id = " + ids
            sql_end = " order by question_id DESC"
            sql = sql_start + sql_content + sql_end
            print(f'sql : {sql}')
            conn, cursor = db_connect()
            cursor.execute(sql)
            records = cursor.fetchall()
            db_close(conn)
            if len(records) > 0:
                # query_str_data = []
                # query_str_list = []
                for row in records:
                    question_id = row[0]
                    author_email = row[1]
                    subject_id = row[3]
                    subject_name = row[2]
                    category = row[4]
                    content = row[5]
                    created = row[6]
                    updated = row[7]
                    image_url = row[8]
                    recognized_text = row[9]
                    hasAnswer = row[10]
                    nickname = row[13]
                    query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                      content, created, updated, image_url, recognized_text, hasAnswer, nickname]
                    print(query_str_data)
                    # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                    str = make_question_dict_str(query_str_data)
                    print(f'str : {str}')
                    question_list.append(str)
        return True, question_list


def get_question_list_query_db_v2(query, email, nickname, subject_id, page, num, hasAnswer): 
    print('[ get_question_list_query_db_v2 ]')
    query_str = list()
    question_list = []
    answer_list = []
    print(f'query : {query}')
    print(f'subject_id : {subject_id}')
    print(f'email : {email}')
    print(f'page : {page}')
    print(f'num : {num}')
    print(f'hasAnswer : {hasAnswer}')
    if len(query) == 0:
        if len(subject_id) == 0:
            # @@ ryan : query 수정 완료
            question_list = query_empty_subject_id_empty_db_v2(
                query, email,  subject_id, page, num, hasAnswer)
            if len(question_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
        else:
            question_list = query_empty_subject_id_NOT_empty_db_v2(
                query, email, nickname, subject_id, page, num, hasAnswer)
            if len(question_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
    else:
        if len(subject_id) == 0:
            question_list, answer_list = query_NOT_empty_subject_id_empty_db_v2(
                query, email, subject_id, page, num, hasAnswer)
            # print(
            # f'[get_question_list_query_db-->question_list] : {question_list}')
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
        else:
            question_list, answer_list = query_NOT_empty_subject_id_NOT_empty_db_v2(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list

def get_question_list_query_db_v3(query, nickname, email, subject_id, page, num, hasAnswer): # 06.25
    print('[ get_question_list_query_db_v3 ]')
    query_str = list()
    question_list = []
    answer_list = []
    print(f'query : {query}')
    print(f'subject_id : {subject_id}')
    print(f'email : {email}')
    print(f'nickname : {nickname}')
    print(f'page : {page}')
    print(f'num : {num}')
    print(f'hasAnswer : {hasAnswer}')
    if len(query) == 0:
        if len(subject_id) == 0:
            # @@ ryan : query 수정 완료
            question_list = query_empty_subject_id_empty_db_v2(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
        else:
            question_list = query_empty_subject_id_NOT_empty_db_v2(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
    else:
        if len(subject_id) == 0:
            question_list, answer_list = query_NOT_empty_subject_id_empty_db_v2(
                query, email, subject_id, page, num, hasAnswer)
            # print(
            # f'[get_question_list_query_db-->question_list] : {question_list}')
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
        else:
            question_list, answer_list = query_NOT_empty_subject_id_NOT_empty_db_v2(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list

def get_question_list_query_db_v4(query, nickname, email, subject_id, page, num, hasAnswer): # 09.12
    print('[ get_question_list_query_db_v4 ]')
    query_str = list()
    question_list = []
    answer_list = []
    print(f'query : {query}')
    print(f'subject_id : {subject_id}')
    print(f'email : {email}')
    print(f'nickname : {nickname}')
    print(f'page : {page}')
    print(f'num : {num}')
    print(f'hasAnswer : {hasAnswer}')
    if len(query) == 0:
        if len(subject_id) == 0:
            # @@ ryan : query 수정 완료
            question_list, answer_list = query_empty_subject_id_empty_db_v3(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) == 0 and len(answer_list) == 0:
                return False, question_list, answer_list
            else:
                return True, question_list, answer_list
        else:
            question_list = query_empty_subject_id_NOT_empty_db_v2(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
    else:
        if len(subject_id) == 0:
            question_list, answer_list = query_NOT_empty_subject_id_empty_db_v2(
                query, email, subject_id, page, num, hasAnswer)
            # print(
            # f'[get_question_list_query_db-->question_list] : {question_list}')
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
        else:
            question_list, answer_list = query_NOT_empty_subject_id_NOT_empty_db_v2(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list

def get_question_list_query_dbv2(query, email, subject_ids, page, num, hasAnswer):
    print('[ get_question_list_query_db_v2 ]')
    query_str = list()
    question_list = []
    q_list = []
    a_list = []
    answer_list = []
    print(f'query : {query}')
    print(f'subject_ids : {subject_ids}')
    print(f'email : {email}')
    print(f'page : {page}')
    print(f'num : {num}')
    print(f'hasAnswer : {hasAnswer}')
    if len(query) == 0:
        if len(subject_ids) == 0:
            # @@ ryan : query 수정 완료
            subject_id = ''
            question_list = query_empty_subject_id_empty_db(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
        else:
            # for subject_id in subject_ids:
            q_list = query_empty_subject_id_NOT_empty_db_v2(
                query, email, subject_ids, page, num, hasAnswer)
            question_list.append(q_list)
            if len(question_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
    else:
        if len(subject_ids) == 0:
            subject_id = ''
            question_list, answer_list = query_NOT_empty_subject_id_empty_db(
                query, email, subject_id, page, num, hasAnswer)
            # print(
            # f'[get_question_list_query_db-->question_list] : {question_list}')
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
        else:
            for subject_id in subject_ids:
                q_list, a_list = query_NOT_empty_subject_id_NOT_empty_db(
                    query, email, subject_id, page, num, hasAnswer)
                question_list.append(q_list)
                answer_list.append(a_list)
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list


def get_question_list_query_dbv2_v2(query, email, nickname, subject_ids, page, num, hasAnswer):
    print('[ get_question_list_query_db_v2 ]')
    query_str = list()
    question_list = []
    q_list = []
    a_list = []
    answer_list = []
    print(f'query : {query}')
    print(f'subject_ids : {subject_ids}')
    print(f'email : {email}')
    print(f'page : {page}')
    print(f'num : {num}')
    print(f'hasAnswer : {hasAnswer}')
    if len(query) == 0:
        if len(subject_ids) == 0:
            # @@ ryan : query 수정 완료
            subject_id = ''
            question_list = query_empty_subject_id_empty_db_v2(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
        else:
            # for subject_id in subject_ids:
            q_list = query_empty_subject_id_NOT_empty_db_v2(
                query, email, subject_ids, page, num, hasAnswer)
            question_list.append(q_list)
            if len(question_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
    else:
        if len(subject_ids) == 0:
            subject_id = ''
            question_list, answer_list = query_NOT_empty_subject_id_empty_db_v2(
                query, email, subject_id, page, num, hasAnswer)
            # print(
            # f'[get_question_list_query_db-->question_list] : {question_list}')
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
        else:
            for subject_id in subject_ids:
                q_list, a_list = query_NOT_empty_subject_id_NOT_empty_db_v2(
                    query, email, subject_id, page, num, hasAnswer)
                question_list.append(q_list)
                answer_list.append(a_list)
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list


def make_reward_dict_str(reward_list):
    # print(f'make_question_dict_str')
    # print(query)
    # print(f'query_str_list size : {len(query_str_list)}')
    # query_dict_list = []

    print(f'reward_list : {reward_list}')
    reward_dict = {}
    reward_dict["date_time"] = reward_list[0]
    reward_dict["email"] = reward_list[1]
    reward_dict["account"] = reward_list[2]
    reward_dict["payment_option"] = reward_list[3]
    reward_dict["req_reward"] = reward_list[4]
    reward_dict["req_status"] = reward_list[5]
    reward_dict["balance"] = reward_list[6]

    # json_query_dict = json.dumps(query_dict)
    # json_query_dict = json_query_dict.strip().replace('\"','"')
    # query_dict_list.append(query_dict)
    # print(query_dict_list)

    # with open('question.json', 'w') as outfile:
    #     json.dump(query_dict_list, outfile, indent=4)

    return reward_dict

def make_question_dict_str(query):
    # print(f'make_question_dict_str')
    # print(query)
    # print(f'query_str_list size : {len(query_str_list)}')
    # query_dict_list = []

    # print(f'query : {query}')
    query_dict = {}
    query_dict["question_id"] = str(query[0])
    query_dict["author_email"] = query[1]
    query_dict['subject_id'] = query[3]
    query_dict["subject_name"] = query[2]
    query_dict["category"] = query[4]
    query_dict["content"] = query[5]
    query_dict["created"] = query[6]
    query_dict["updated"] = query[7]
    query_dict["image_url"] = query[8]
    query_dict["recognized_text"] = query[9]
    query_dict["hasAnswer"] = query[10]
    query_dict["nickname"] = query[11]
    # query_dict['nickname'] = get_nickname_info_db(query[1])    
    # json_query_dict = json.dumps(query_dict)
    # json_query_dict = json_query_dict.strip().replace('\"','"')
    # query_dict_list.append(query_dict)
    # print(query_dict_list)

    # with open('question.json', 'w') as outfile:
    #     json.dump(query_dict_list, outfile, indent=4)

    return query_dict


def make_answer_dict_str(answer):
    print('[ make_answer_dict_str ]')
    # print(answer_str_list)
    # print(f'answer_str_list size : {len(answer_str_list)}')
    # answer_dict_list = []

    # for answer in answer_str_list:
    print(f'answer : {answer}')
    answer_dict = {}
    answer_dict["answer_id"] = answer[0]
    answer_dict["question_id"] = answer[1]
    answer_dict["author_email"] = answer[2]
    answer_dict["content"] = answer[3]
    answer_dict["selected"] = answer[4]
    answer_dict["created"] = answer[5]
    answer_dict["updated"] = answer[6]
    answer_dict["image_url"] = answer[7]
    answer_dict["recognized_text"] = answer[8]
    answer_dict["nickname"] = answer[9]
    # json_answer_dict = json.dumps(answer_dict)

    print(f'answer_dict : {answer_dict}')
    return answer_dict


def get_question_list_db(query_str, subject_id, page):
    print('[ get_question_list_db ]')
    answer_list = list()
    answer_list = {'question': query_str}

    question_list = {'search_keywords': query_str, 'answer': answer_list}
    question_id_list = []

    query_str_list = query_str.split(',')

    for i in range(len(query_str_list)):
        query_str_list[i] = query_str_list[i].replace(' ', '')

    print(f'len of query_str : {len(query_str_list)}')
    print(f'query_str : {query_str_list}')
    for search_item in query_str_list:
        conn, cursor = db_connect()
        # search_sql = "select question_id from Question where recognized_text '{0}".format('%')
        # search_sql = search_sql + search_item + "{}'".format('%')get_question_list_query_db
        search_sql = "select question_id from Question where recognized_text '%" + \
            search_item + "%'"
        print(f'sql : {search_sql}')
        cursor.execute(search_sql)
        records = cursor.fetchall()
        db_close(conn)
        if len(records) > 0:
            for row in records:
                question_id_list.append(row[0])

    if len(question_id_list) > 0:
        print(f'question_id_list : {question_id_list}')
        for search_id in question_id_list:
            print(f'question_id_list : {search_id}')
            conn, cursor = db_connect()
            sql = "select * from Answer where question_id = %s ORDER BY answer_id"
            cursor.execute(sql, (str(search_id)))
            records = cursor.fetchall()
            db_close(conn)
            if len(records) > 0:
                for row in records:
                    answer_id = row[0]
                    question_id = row[1]
                    author_emial = row[2]
                    content = row[3]
                    selected = row[4]
                    created = row[5]
                    updated = row[6]
                    image_url = row[7]
                    recognized_text = row[8]
                    # row[4] : subject_name, row[6] : content
                    answer_list.append(content)
                question_list['answer'] = answer_list
                return True, question_list
            else:
                return False, question_list


def get_nickname_schoolinfo_from_db(email):
    nickname = ''
    schoolcode = ''
    schoolname = ''
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where userEmail = %s"
    cursor.execute(sql, (email))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            schoolname = row[5]
            schoolcode = row[6]
            nickname = row[9]
            break

    return nickname, schoolcode, schoolname


def get_answer_for_question_db(email, question_id):
    print(f'[ get_answer_for_question_db ] question_id : {question_id}')
    answer_str = list()
    question_str = list()
    question_list = {}
    answer_list = []
    flag_question_is = False

    # print(f'question_id : {question_id}')
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from Question where question_id = %s ORDER by question_id DESC"
    cursor.execute(sql, (question_id))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        flag_question_is = True
        query_str_data = []
        query_str_list = []
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_name = row[3]
            subject_id = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            nickname = row[13] #nickname field
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, hasAnswer,nickname]

            # row[4] : subject_name, row[6] : content
            query_str_list.append(query_str_data)
        question_list = make_question_dict_str(query_str_list[0])
        # print(f'[get_answer_for_question_db] question_list : {question_list}')

    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from Answer where question_id = %s ORDER BY answer_id"
    cursor.execute(sql, (question_id))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        answer_str_data = []
        answer_str_list = []
        for row in records:
            answer_id = str(row[0])
            question_id = row[1]
            author_email = row[2]
            content = row[3]
            selected = row[4]
            created = row[5]
            updated = row[6]
            image_url = row[7]
            recognized_text = row[8]
            nickname = row[11]

            answer_str_data = [answer_id, question_id, author_email, content,
                               selected, created, updated, image_url, recognized_text, nickname]

            # row[4] : subject_name, row[6] : content
            answer_str_list.append(answer_str_data)
        # print(f'answer_str_list : {answer_str_list}')
        # answer_list['answer'] = make_answer_dict_str(answer_str_list)
        for answer_data in answer_str_list:
            answer_list.append(make_answer_dict_str(answer_data))

        return True, question_list, answer_list
    else:
        if flag_question_is:
            return True, question_list, answer_list
        else:
            return False, question_list, answer_list


# @@ryan : hasAnswer 추가
def create_question_db(email, subject_id, subject_name, category, content, imageUrl, recog_text):
    current_datetime = datetime.now()
    created_date = str(current_datetime)
    # print(f'[db_connect] email : {email}')
    # print(f'[db_connect] subject_name : {subject_name}')
    # print(f'[db_connect] subject_id : {subject_id}')
    # print(f'[db_connect] category : {category}')
    # print(f'[db_connect] content : {content}')
    # print(f'[db_connect] created_date : {created_date}')
    # print(f'[db_connect] imageUrl : {imageUrl}')
    # print(f'[db_connect] recog_text : {recog_text}')
    conn, cursor = db_connect()

    conv_content = converted_special_char(content)
    conv_recog_text = converted_special_char(recog_text)
    hasAnwser = '0'
    sql = "INSERT INTO Question (author_email, subject_id, subject_name, category, content,  created, image_url, recognized_text, re_con, re_recog, hasAnswer) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # print(f'[db_connect] sql : {sql}')
    cursor.execute(sql, (email, subject_id, subject_name,
                   category, content, created_date, imageUrl, recog_text, conv_content, conv_recog_text, hasAnwser))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from Question where author_email = %s and subject_name = %s"
    cursor.execute(sql, (email, subject_name))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            q_no = str(row[0])
    else:
        q_no = str(-1)

    return q_no


def create_question_db_v2(email, subject_id, subject_name, category, content, imageUrl, recog_text):
    nickname, schoolcode, schoolname = get_nickname_schoolinfo_from_db(email)
    current_datetime = datetime.now()
    created_date = str(current_datetime)
    # print(f'[db_connect] email : {email}')
    # print(f'[db_connect] subject_name : {subject_name}')
    # print(f'[db_connect] subject_id : {subject_id}')
    # print(f'[db_connect] category : {category}')
    # print(f'[db_connect] content : {content}')
    # print(f'[db_connect] created_date : {created_date}')
    # print(f'[db_connect] imageUrl : {imageUrl}')
    # print(f'[db_connect] recog_text : {recog_text}')

    conn, cursor = db_connect()

    conv_content = converted_special_char(content)
    conv_recog_text = converted_special_char(recog_text)
    hasAnwser = '0'
    sql = "INSERT INTO Question (author_email, nickname, subject_id, subject_name, category, content,  created, image_url, recognized_text, re_con, re_recog, hasAnswer) values(%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # print(f'[db_connect] sql : {sql}')
    cursor.execute(sql, (email, nickname, subject_id, subject_name,
                   category, content, created_date, imageUrl, recog_text, conv_content, conv_recog_text, hasAnwser))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from Question where author_email = %s and subject_name = %s"
    cursor.execute(sql, (email, subject_name))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            q_no = str(row[0])
    else:
        q_no = str(-1)

    return q_no


def create_write_answer_db(email, question_id, content, imageUrl, recog_text):
    current_datetime = datetime.now()
    created_date = str(current_datetime)
    # print(f'created_date : {created_date}')
    # print(f'imageUrl : {imageUrl}')
    conv_content = converted_special_char(content)
    conv_recog_text = converted_special_char(recog_text)
    
    conn, cursor = db_connect()
    check_author_question = "SELECT author_email from Question where question_id = %s"
    cursor.execute(check_author_question, (question_id))

    records = cursor.fetchall()

    if len(records) > 0:
        for row in records:
            author_email = row[0]

            if author_email != email:
                db_close(conn)
                return str(-1)

    db_close(conn)

    conn, cursor = db_connect()
    answer_sql = "INSERT INTO Answer (author_email, question_id, content, created, image_Url, recognized_text, re_con, re_recog) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(answer_sql, (email, question_id, content,
                   created_date, imageUrl, recog_text, conv_content, conv_recog_text))
    question_sql = "UPDATE Question SET hasAnswer = %s where question_id = %s"
    cursor.execute(question_sql, ('1', question_id))
    records = cursor.fetchall()

    if len(records) > 0:
        for row in records:
            author_email = row[0]

            if author_email != email:
                db_close(conn)
                return str(-2)
    db_close(conn)
    conn, cursor = db_connect()
    sql = "select * from Answer where author_email = %s and question_id = %s"
    cursor.execute(sql, (email, question_id))
    records = cursor.fetchall()

    db_close(conn)

    if len(records) > 0:
        for row in records:
            ano_no = str(row[0])
    else:
        ano_no = str(-1)

    return ano_no


def create_write_answer_db_v2(email, question_id, content, imageUrl, recog_text):
    nickname, schoolcode, schoolname = get_nickname_schoolinfo_from_db(email)
    current_datetime = datetime.now()
    created_date = str(current_datetime)
    # print(f'created_date : {created_date}')
    # print(f'imageUrl : {imageUrl}')
    conv_content = converted_special_char(content)
    conv_recog_text = converted_special_char(recog_text)

    conn, cursor = db_connect()
    check_author_question = "SELECT adminEmail from Admin where adminEmail = %s"
    cursor.execute(check_author_question, (question_id))

    records = cursor.fetchall()
    db_close(conn)

    if len(records) == 0: # Not admin
        conn, cursor = db_connect()
        check_author_question = "SELECT author_email from Question where question_id = %s"
        cursor.execute(check_author_question, (question_id))

        records = cursor.fetchall()
        db_close(conn)
        if len(records) > 0:
            for row in records:
                author_email = row[0]
                if author_email == email:
                    return str(-1)

    conn, cursor = db_connect()

    answer_sql = "INSERT INTO Answer (author_email, nickname, question_id, content, created, image_Url, recognized_text, re_con, re_recog) values(%s,%s, %s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(answer_sql, (email, nickname, question_id, content,
                   created_date, imageUrl, recog_text, conv_content, conv_recog_text))
    question_sql = "UPDATE Question SET hasAnswer = %s where question_id = %s"
    cursor.execute(question_sql, ('1', question_id))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from Answer where author_email = %s and question_id = %s"
    cursor.execute(sql, (email, question_id))
    records = cursor.fetchall()

    db_close(conn)

    if len(records) > 0:
        for row in records:
            ano_no = str(row[0])
    else:
        ano_no = str(-1)

    return ano_no


def delete_question_db(question_id):

    conn, cursor = db_connect()
    sql = "DELETE FROM Question WHERE question_id = " + str(question_id)
    cursor.execute(sql)
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from Question where question_id = " + str(question_id)
    cursor.execute(sql)
    records = cursor.fetchall()
    db_close(conn)

    if len(records) > 0:
        return False
    else:
        return True


def delete_write_answer_db(answer_id):

    conn, cursor = db_connect()
    sql = "DELETE FROM Answer WHERE answer_id = " + str(answer_id)
    cursor.execute(sql)
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from Answer where answer_id = " + str(answer_id)
    cursor.execute(sql)
    records = cursor.fetchall()
    db_close(conn)

    if len(records) > 0:
        return False
    else:
        return True


def recent_question_db(question_num):
    question_list = list()
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from Question order by question_id DESC limit 10"
    cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            question = []
            question.append(row[0])
            question.append(row[1])
            question.append(row[2])
            question.append(row[3])
            question.append(row[4])
            question.append(row[5])
            question.append(row[8])
            question.append(row[9])

            question_list.append(question)
    return question_list

def process_paypal_result(filename):
    print("this is paypal name : "+filename)
    df = pd.read_csv(filename)
    for i in range(len(df)):
        if df.iloc[i,4] == 'Mass Pay Payment':
            gross = df.iloc[i,7]
            receipt_email = df.iloc[i,11]
            # print(str(gross) + ':' + receipt_email)
        
            conn, cursor = db_connect()
            sql = "select * from req_reward where email = %s"
            cursor.execute(sql,(receipt_email))
            records = cursor.fetchall()
            db_close(conn)

            if len(records) > 0:
                for row in records:
                    req_id = str(row[0])
                    req_reward = row[5]
                    req_status = row[6]
                    
                    print(req_id + ' ' + req_reward + ' ' + req_status)
                    update_req_reward_db(receipt_email)
                    update_User_db(receipt_email, req_reward)
                    
def update_User_db(receipt_email, req_reward):
    conn, cursor = db_connect()
    sql = "select * from User where userEmail = %s"
    cursor.execute(sql,(receipt_email))
    records = cursor.fetchall()
    db_close(conn)
    
    if len(records) > 0:
        for row in records:
            reward = float(row[7])
            updated_reward = reward # - float(req_reward)
            
            conn, cursor = db_connect()
            sql = "update User set reward = %s where userEmail = %s"
            cursor.execute(sql,(updated_reward, receipt_email))
            records = cursor.fetchall()
            db_close(conn)

def update_req_reward_db(receipt_email):
    updated_status = "Completed"
    conn, cursor = db_connect()
    sql = "update req_reward set req_status = 'Completed' where email = %s"
    cursor.execute(sql,(receipt_email))
    records = cursor.fetchall()
    db_close(conn)
    
def payment_request_history(reward_req_email):
    
    reward_list = []
    conn, cursor = db_connect()
    sql = "select * from req_reward where email = %s order by date_time DESC"
    # print(f'sql : {sql}')
    cursor.execute(sql,(reward_req_email))
    records = cursor.fetchall()
    db_close(conn)
    
    if len(records) > 0:
        for row in records:
            rewward_id = row[0]
            date_time = str(row[1])
            email = row[2]
            account = row[3]
            payment_option = row[4]
            req_reward = row[5]
            req_status = row[6]
            balance = row[7]
            str_date_time = str(date_time)
            # print(f'str_date_time : {str_date_time}')
            reward_payment_str = [date_time, email, account, payment_option, req_reward, req_status,balance]
            reward_dict_str = make_reward_dict_str(reward_payment_str)
            reward_list.append(reward_dict_str)

    return True, reward_list

# 두 벡터의 코사인 유사도
def get_question_with_question_id(qid):
    question_list = []
    question_text_list = []

    conn, cursor = db_connect()
    sql = "select * from Question where question_id = %s"
    cursor.execute(sql, (qid))

    records = cursor.fetchall()
    db_close(conn)
    
    if len(records) > 0:
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[3]
            subject_name = row[2]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            hasAnswer = row[10]
            nickname = row[13]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                content, created, updated, image_url, recognized_text, hasAnswer,nickname]
            # query_str_data = [question_id, recognized_text]

            # query_dict = {}
            # query_dict["question_id"] = str(query_str_data[0])
            # query_dict["recognized_text"] = query_str_data[1]
            
            # print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content

            str = make_question_dict_str(query_str_data)
            
            # question_list.append('"question_id" : ' + str["question_id"])
            # question_list.append('"author_email" : ' + str["author_email"])
            # question_list.append('"subject_id" : ' + str["subject_id"])
            # question_list.append('"subject_name" : ' + str["subject_name"])
            # question_list.append('"category" : ' + str["category"])
            # question_list.append('"content" : ' + str["content"])
            # question_list.append('"created" : ' + str["created"])
            # if str["updated"] == None:
            #     question_list.append('"updated" : ' + "")    
            # else:
            #     question_list.append('"updated" : ' + str["updated"])
            # question_list.append('"image_url" : ' + str["image_url"])
            # question_list.append('"recognized_text" : ' + str["recognized_text"])
            # question_list.append('"hasAnswer" : ' + str["hasAnswer"])
            # if str["nickname"] == None:
            #     question_list.append('"nickname" : ' + "")
            # else:
            #     question_list.append('"nickname" : ' + str["nickname"])
            question_list.append(str)
            question_text_list.append(recognized_text)
        # print('question_list :')
        # print(question_list)
        return True, question_list, question_text_list
    else:
        return False, None, None

def cos_similarity(v1, v2):
    dot_product = v1 @ v2
    ab_norm = np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2)))
    similarity = dot_product / ab_norm
    
    return similarity

def extract_questions(src):
    MAX_QUESTION_ID = 100000
    processed_src = src.split('<latex>')[0]
    # processed_src = src
    # print(f'src text : {processed_src}')
    doc_list = []
    question_id_list = []
    doc_list.append(processed_src)
    question_id_list.append(MAX_QUESTION_ID)
    # print(doc_list)
    conn, cursor = db_connect()
    sql = "select question_id, recognized_text from Question where question_id > 200"
    cursor.execute(sql)
    subjects_list = []
    subject_dict = {}
    records = cursor.fetchall()
    db_close(conn)
    count = 0
    for row in records:
        dst = row[1]
        question_id = row[0]
        processed_dst = dst.split('<latex>')[0]
        # processed_dst = dst
        # if len(processed_dst) == 0:
        #     continue
        doc_list.append(processed_dst)
        question_id_list.append(question_id)
        # if count >= 100:
        #     break
        # count += 1
    # print(f'# of questions : {len(doc_list)}')
    # print(f'question_id_list[0:10] : {question_id_list}')
    return doc_list, question_id_list

    # for i in range(len(doc_list)):
    #     print(f'[{i}] : ##{doc_list[i]}##')

def question_similarity(src_question):
    result_list = []
    question_text_list = []
    text_list = []
    final_list = []
    doc_list, question_id_list = extract_questions(src_question)
    print()
    print(f'# of question_id_list : {len(question_id_list)}')
    print(f'# of doc_list : {len(doc_list)}')
    # for i in range(len(doc_list)):
    #     print(f'{question_id_list[i]} : {doc_list[i]}')

    tfidf_vect = TfidfVectorizer()
    feature_vect = tfidf_vect.fit_transform(doc_list)

    similarity_simple_pair = cosine_similarity(feature_vect[0] , feature_vect[1:])
    # print(similarity_simple_pair)
    # print(f'len doc_lsit : {len(doc_list)}')
    # similarity_list = similarity_simple_pair[0]
    # question_list = question_id_list

    # similarity_dict = {}
    # for i in range(len(similarity_list)):
    #     similarity_dict[similarity_list[i]] = question_list[i]

    # # print(f'similarity_list[0] : {similarity_list[0]}')
    # # print(f'question_list[0] : {question_list[0]}')
    # # print(f'similarity_dict[0] : {similarity_dict[similarity_list[0]]}')

    # sorted_dict = dict(sorted(similarity_dict.items(), reverse=True))
    # # limited_10_dict = sorted_dict[1:11]
    # count = 0

    # for key, question_id in sorted_dict.items():
    #     if count > 0:
    #         # print(f'key :{key} --> question_id :{question_id}')
    #         flag, result_list, text_list = get_question_with_question_id(question_id)
    #         # print('result_list : ')
    #         # print(result_list)
    #         if flag:
    #             final_list.append(result_list[0])
    #             question_text_list.append(text_list)
    #             print(f'key :{key} --> question_id :{question_id}')
    #     if count >= 10 :
    #         break
    #     else:
    #         count += 1
    # print(f'len(final_list) : {len(final_list)}')



    return final_list, question_text_list

def question_similarity_2(src_question):


    result_list = []
    question_text_list = []
    text_list = []
    final_list = []
    doc_list, question_id_list = extract_questions(src_question)
    # print()
    # print(f'# of question_id_list : {len(question_id_list)}')
    # print(f'# of doc_list : {len(doc_list)}')
    # for i in range(len(doc_list)):
    #     print(f'{question_id_list[i]} : {doc_list[i]}')

    model = SentenceTransformer('paraphrase-distilroberta-base-v1')

    embeddings = model.encode(doc_list, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)
    # print(f'cosine_scores:')
    # print(cosine_scores)
    cosine_scores_list = cosine_scores[0].tolist()
    # print(cosine_scores_list)
    sorted_cosine_scores_list = sorted(cosine_scores_list, reverse=True)
    # print(sorted_cosine_scores_list)
    for i in range(len(sorted_cosine_scores_list)):
        if sorted_cosine_scores_list[1] == cosine_scores_list[i]:
            final_list.append(question_id_list[i])
        if sorted_cosine_scores_list[2] == cosine_scores_list[i]:
            final_list.append(question_id_list[i])
        if sorted_cosine_scores_list[3] == cosine_scores_list[i]:
            final_list.append(question_id_list[i])
        if sorted_cosine_scores_list[4] == cosine_scores_list[i]:
            final_list.append(question_id_list[i])
        if sorted_cosine_scores_list[5] == cosine_scores_list[i]:
            final_list.append(question_id_list[i])
    # similarity_list = similarity_simple_pair[0]
    # question_list = question_id_list

    # similarity_dict = {}
    # for i in range(len(similarity_list)):
    #     similarity_dict[similarity_list[i]] = question_list[i]

    # # print(f'similarity_list[0] : {similarity_list[0]}')
    # # print(f'question_list[0] : {question_list[0]}')
    # # print(f'similarity_dict[0] : {similarity_dict[similarity_list[0]]}')

    # sorted_dict = dict(sorted(similarity_dict.items(), reverse=True))
    # # limited_10_dict = sorted_dict[1:11]
    # count = 0

    # for key, question_id in sorted_dict.items():
    #     if count > 0:
    #         # print(f'key :{key} --> question_id :{question_id}')
    #         flag, result_list, text_list = get_question_with_question_id(question_id)
    #         # print('result_list : ')
    #         # print(result_list)
    #         if flag:
    #             final_list.append(result_list[0])
    #             question_text_list.append(text_list)
    #             print(f'key :{key} --> question_id :{question_id}')
    #     if count >= 10 :
    #         break
    #     else:
    #         count += 1
    # print(f'len(final_list) : {len(final_list)}')



    return final_list    

def extract_roles(req_title): #12.22
    # req_title = '영상콘텐츠 디자이너'
    print(f'req_title : {req_title}')
    count_value = 0
    conn, cursor = db_connect()
    sql = "SELECT core FROM job_dataset where title = %s"
    cursor.execute(sql, (req_title))
    records = cursor.fetchall()
    db_close(conn)

    count_value = len(records)
    role_list = []
    print(f'count_value : {count_value}')
    for row in records:
        role_list = row[0].split(',')
        

    return count_value, role_list

if __name__ == "__main__":
    # doc_list = ['if you take the blue pill, the story ends' ,
    #         'if you take the red pill, you stay in Wonderland',
    #         'if you take the red pill, I show you how deep the rabbit hole goes']
    # sample_txt = "dollars, and the price of Paul's sandwich was $1 more than the price of Ken's sandwich. If Ken and Paul split the cost of the sandwiches evenly and each paid a 20% tip, which of the following expressions represents the amount, in dollars, each of them paid? (Assume there is no sales tax.) <latex>\text { dollars \
    #         and the price of Paul's sandwich was } \
    #         \$ 1 \text { more than the price of Ken's sandwich. If } \
    #         \text { Ken and Paul split the cost of the sandwiches } \
    #         \text { evenly and each paid a } 20 \% \text { tip \
    #         which of the } \
    #         \text { following expressions represents the amount \
    #         in } \text { dollars each of them paid? (Assume there is } \text { no sales tax.) }</latex><latex>20 \%</latex>"
    sample_txt = "Find all the real zeros"
    result = question_similarity_2(sample_txt) 
    print(result)
    # print(question_text_list)
    # print(len(question_text_list))

    # print(f'sample_txt : {sample_txt}')
    # for i in range(len(question_text_list)):
    #     target_str = str(question_text_list[i])
    #     print(target_str.split('<latex>')[0])
    # dic = {'pop': 3100, 'classic': 1450, 'trot':620}
    # # key 값을 기준으로 오름차순 정렬하여 리스트 출력
    # print(sorted(dic))
    # # key 값을 기준으로 내림차순 정렬한 리스트 출력 
    # print(sorted(dic, reverse=True))
    # print(limited_10_dict.items())
    # index = list_results.argmax()
    # print(f'index :{index}')
    # print(f'doc_list : {doc_list[index]}')
    # print(f'question_id : {question_id_list[index]}')
    # origin_results = list_results
    # sorted_list = np.sort(list_results)[::-1]
    # print(sorted_list)
    # print(f'sorted_list[1] : {sorted_list[1]}')
    # for i in range(len(origin_results)):
    #     if origin_results[i] == sorted_list[1]:
    #         print(origin_results[i])
    #         print(question_id_list[i])
    # second_index = np.where(origin_results == sorted_list[1])
    # print(f'second_index : {second_index}')
    # print(f'second doc_list : {doc_list[second_index]}')
    # print(f'second question_id : {question_id_list[second_index]}')