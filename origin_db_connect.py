import pymysql
import jwt
import bcrypt
from datetime import datetime
import json

user_info = {}

def db_connect():
    conn = pymysql.connect(host='',
                           user='', password='', db='', charset='utf8')
    cursor = conn.cursor()

    return conn, cursor


def db_execute_quiry(cursor, sql):
    #sql = "SELECT * FROM dummy_gps"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def db_close(conn):
    conn.commit()
    conn.close()

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
        subject_dict["subject_name"] = row[2]
        subject_dict["category"] = row[3] 
        subjects_list.append(subject_dict)

    if len(records) > 0:
        return True, subjects_list #extracted_student_json
    else:
        return False #None
    
def check_user_email_from_db(u_email):
    conn, cursor = db_connect()
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
    sql = "select * from User where userEmail = %s"       
    #sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (u_email))
    
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True #extracted_student_json
    else:
        return False #None
    
def get_all_user_info_from_db():
    conn, cursor = db_connect()
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
    sql = "select * from User"  
    #sql = "select * from dummy_gps2 where id = %s and timestep = %s"
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
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
    sql = "select * from User where userEmail = %s"      
    #sql = "select * from dummy_gps2 where id = %s and timestep = %s"
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
            #student_data = {"role" : role, "schoolName": user_school_name, "schoolCode" : user_school_code, "grade" : user_grade}
            #extracted_student_json = json.dumps(student_data)
        
        return True #extracted_student_json
    else:
        return False #None
    
def insert_user_db(u_id, u_passwd): #OK
    conn, cursor = db_connect()
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
    #sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    sql = "INSERT INTO User (userEmail, userPass, userRole, userGrade, schoolName, schoolCode) values(%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (u_id, u_passwd, '0', '10','Texas Highschool','0001'))
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

def update_user_info_db(email, passwd, role, school_name, school_code, grade):
    conn, cursor = db_connect()
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
    #sql = "select * from dummy_gps2 where id = %s and timestep = %s"
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

def get_user_info_db(email, passwd ):
    role = school_name = school_code = grade = ''
    conn, cursor = db_connect()
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
    sql = "select * from User where userEmail = %s and userPass = %s"      
    #sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (email, passwd))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            role = row[3]
            school_name = row[5]
            school_code = row[6]
            grade = row[4]

            #student_data = {"role" : role, "schoolName": user_school_name, "schoolCode" : user_school_code, "grade" : user_grade}
            #extracted_student_json = json.dumps(student_data)
        
    return role, school_name, school_code, grade
        
def check_password( u_id, u_passwd):
    conn, cursor = db_connect()
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
    sql = "select * from User where userEmail = %s"       
    #sql = "select * from dummy_gps2 where id = %s and timestep = %s"
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
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
    sql = "select * from User where schoolCode = %s"       
    #sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (school_code))
    
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False

def check_school_name(school_name):
    conn, cursor = db_connect()
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
    sql = "select * from User where schoolCode = %s"       
    #sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (school_name))
    
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False

def get_user_question_db(email, subject_id, page):
    question_list = list()
    conn, cursor = db_connect()
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
    sql = "select * from Question where author_email = %s ORDER by question_id DESC" 
    cursor.execute(sql, (email))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            question_list.append(row[4]) # row[4] : subject_name, row[6] : content
        return True, question_list
    else:
        return False, question_list

def get_question_list_all_db(query_str):
    query_str = list()
    question_list = {'question' : query_str}
    
    if len(query_str) == 0:
        conn, cursor = db_connect()
        #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
        sql = "select * from Question ORDER by question_id DESC LIMIT 10" 
        cursor.execute(sql)

        records = cursor.fetchall()
        db_close(conn)
        if len(records) > 0:

            for row in records:
                question_id = row[0]
                author_email = row[1]
                subject_id = row[2]
                subject_name = row[3]
                category = row[4]
                content = row[5]
                created = row[6]
                image_url = row[7]
                recognized_text = row[8]

                query_str.append(content) # row[4] : subject_name, row[6] : content
            question_list['question'] = query_str
            return True, question_list
        else:
            return False, question_list
    else:
        return False, question_list

def get_question_list_query_db(query,subject_id, page, num, hasAnswer):
    print('[ get_question_list_query_db ]')
    query_str = list()
    question_list = []
    print(f'query size: {len(query)}')
    print(f'subject_id size : {len(subject_id)}')
    print(f'page : {page}')
    print(f'num : {num}')
    print(f'hasAnswer : {hasAnswer}')
    if len(query) == 0:
        print('len of query = 0')
        if len(subject_id) == 0:
            conn, cursor = db_connect()
            #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
            if (int(page) > 0 ):
                sql = "select * from Question order by question_id DESC LIMIT 10 " 
                cursor.execute(sql)
            else:
                sql = "select * from Question order by question_id DESC LIMIT %s" 
                cursor.execute(sql, (page))

            records = cursor.fetchall()
            db_close(conn)
            if len(records) > 0:
                # query_str_data = []
                # query_str_list = []
                for row in records:
                    question_id = row[0]
                    author_email = row[1]
                    subject_id = row[2]
                    subject_name = row[3]
                    category = row[4]
                    content = row[5]
                    created = row[6]
                    updated = row[7]
                    image_url = row[8]
                    recognized_text = row[9]
                    has_correct_answer = row[10]
                    query_str_data = [question_id, author_email, subject_id, subject_name, category, content, created, updated, image_url, recognized_text, has_correct_answer]
                    print(query_str_data)
                    #query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                    str = make_question_dict_str(query_str_data)
                    #print(f'str : {str}')
                    question_list.append(str)
                    
                return True, question_list
            else:
                return False, question_list
        else:
            conn, cursor = db_connect()
            #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
            if (int(page) > 0 ):
                sql = "select * from Question where subject_id = %s order by question_id DESC LIMIT 10 " 
                cursor.execute(sql, (subject_id))
            else:
                sql = "select * from Question where subject_id = %s order by question_id DESC LIMIT %s" 
                cursor.execute(sql, (subject_id, page))
            records = cursor.fetchall()
            db_close(conn)
            if len(records) > 0:
                # query_str_data = []
                # query_str_list = []
                for row in records:
                    question_id = row[0]
                    author_email = row[1]
                    subject_id = row[2]
                    subject_name = row[3]
                    category = row[4]
                    content = row[5]
                    created = row[6]
                    updated = row[7]
                    image_url = row[8]
                    recognized_text = row[9]
                    has_correct_answer = row[10]
                    query_str_data = [question_id, author_email, subject_id, subject_name, category, content, created, updated, image_url, recognized_text, has_correct_answer]
                    print(query_str_data)
                    #query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                    str = make_question_dict_str(query_str_data)
                    #print(f'str : {str}')
                    question_list.append(str)
                return True, question_list
            else:
                return False, question_list
    else:
        print('len of query > 0')
        print(f'subject_id : {subject_id}')
        leng_of_subject_id = len(subject_id)
        print(f'leng_of_subject_id : {leng_of_subject_id}')
        # if leng_of_subject_id == 0:
        print('len of subject_id == 0')
        conn, cursor = db_connect()
        #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
        if (int(page) > 0 ):
            sql = "select * from Question where content LIKE '%" + query + "%' " + "order by question_id DESC LIMIT 10"
            cursor.execute(sql)
        else:
            sql = "select * from Question where content LIKE '%" + query + "%' " + "order by question_id DESC LIMIT %s"
            cursor.execute(sql, (page))

        records = cursor.fetchall()
        db_close(conn)
        if len(records) > 0:
            # query_str_data = []
            # query_str_list = []
            for row in records:
                question_id = row[0]
                author_email = row[1]
                subject_id = row[2]
                subject_name = row[3]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                has_correct_answer = row[10]
                query_str_data = [question_id, author_email, subject_id, subject_name, category, content, created, updated, image_url, recognized_text, has_correct_answer]
                print(query_str_data)
                #query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                print(f'str : {str}')
                question_list.append(str)
            return True, question_list
        else:
            return False, question_list
        # else:
        #     print('len of subject_id >= 0')
        #     conn, cursor = db_connect()
        #     #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
        #     if (int(page) > 0 ):
        #         print(f'subject_id : {subject_id}')
        #         sql = "select * from Question where content LIKE '%" + query + "%' " + "and subject_id = '" + subject_id + "'order by question_id DESC LIMIT 10"
        #         print(f'sql : {sql}') 
        #         cursor.execute(sql, )
        #     else:
        #         sql = "select * from Question where content LIKE '%" + query + "%' " + "and subject_id = '" + subject_id + "' order by question_id DESC LIMIT %s"
        #         cursor.execute(sql, (subject_id, page))
        #     records = cursor.fetchall()
        #     db_close(conn)
        #     if len(records) > 0:
        #         # query_str_data = []
        #         # query_str_list = []
        #         for row in records:
        #             question_id = row[0]
        #             author_email = row[1]
        #             subject_id = row[2]
        #             subject_name = row[3]
        #             category = row[4]
        #             content = row[5]
        #             created = row[6]
        #             updated = row[7]
        #             image_url = row[8]
        #             recognized_text = row[9]
        #             has_correct_answer = row[10]
        #             query_str_data = [question_id, author_email, subject_id, subject_name, category, content, created, updated, image_url, recognized_text, has_correct_answer]
        #             print(query_str_data)
        #             #query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
        #             str = make_question_dict_str(query_str_data)
        #             print(f'str : {str}')
        #             question_list.append(str)
        #         return True, question_list
        #     else:
        #         return False, question_list

def make_question_dict_str(query):
    #print(f'make_question_dict_str')
    #print(query)
    #print(f'query_str_list size : {len(query_str_list)}')
    #query_dict_list = []

    print(f'query : {query}')
    query_dict = {}
    query_dict["question_id"] = str(query[0])
    query_dict["author_email"] = query[1]
    query_dict["subject_id"] = query[2]
    query_dict["subject_name"] = query[3]
    query_dict["category"] = query[4]
    query_dict["content"] = query[5]
    query_dict["created"] = query[6]
    query_dict["updated"] = query[7]
    query_dict["image_url"] = query[8]
    query_dict["recognized_text"] = query[9]
    query_dict["has_correct_answer"] = query[10]

    #json_query_dict = json.dumps(query_dict)
    #json_query_dict = json_query_dict.strip().replace('\"','"')
    #query_dict_list.append(query_dict)
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
    # json_answer_dict = json.dumps(answer_dict)

    return answer_dict

def get_question_list_db(query_str,subject_id, page):
    print('[ get_question_list_db ]')   
    answer_list = list()
    answer_list = {'question' : query_str}


    question_list = {'search_keywords' : query_str, 'answer':answer_list}
    question_id_list = []
    
    query_str_list = query_str.split(',')

    for i in range(len(query_str_list)):
        query_str_list[i] = query_str_list[i].replace(' ','')

    print(f'len of query_str : {len(query_str_list)}')
    print(f'query_str : {query_str_list}')
    for search_item in query_str_list:
        conn, cursor = db_connect()
        # search_sql = "select question_id from Question where content LIKE '{0}".format('%')
        # search_sql = search_sql + search_item + "{}'".format('%') 
        search_sql = "select question_id from Question where content LIKE '%" + search_item + "%'"
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
                    answer_list.append(content) # row[4] : subject_name, row[6] : content
                question_list['answer'] = answer_list
                return True, question_list
            else:   
                return False, question_list

def get_answer_for_question_db(email, question_id):
    print('[ get_answer_for_question_db ]') 
    answer_str = list()
    question_str = list()
    question_list = {}
    answer_list = []
    flag_question_is = False
    
    print(f'question_id : {question_id}')
    conn, cursor = db_connect()
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
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
            subject_id = row[2]
            subject_name = row[3]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            has_correct_answer = row[10]

            query_str_data = [question_id, author_email, subject_id, subject_name, category, content, created, updated, image_url, recognized_text, has_correct_answer]
            
            query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
        question_list = make_question_dict_str(query_str_list[0])
        print(f'question_list : {question_list}')
        
    conn, cursor = db_connect()
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
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

            answer_str_data = [answer_id, question_id, author_email, content, selected, created, updated, image_url, recognized_text]
            
            answer_str_list.append(answer_str_data) # row[4] : subject_name, row[6] : content
        print(f'answer_str_list : {answer_str_list}')
        #answer_list['answer'] = make_answer_dict_str(answer_str_list)
        for answer_data in answer_str_list:
            answer_list.append(make_answer_dict_str(answer_data))

        return True, question_list, answer_list
    else:
        if flag_question_is :
            return True, question_list, answer_list
        else:
            return False, question_list, answer_list    

def create_question_db(email, subject_name, subject_id, category, content, imageUrl, recog_text):
    current_datetime = datetime.now()
    created_date = str(current_datetime)
    print(f'email : {email}')
    print(f'subject_name : {subject_name}')
    print(f'subject_id : {subject_id}')
    print(f'category : {category}')
    print(f'content : {content}')
    print(f'created_date : {created_date}')
    print(f'imageUrl : {imageUrl}')
    print(f'recog_text : {recog_text}')
    conn, cursor = db_connect()
    
    sql = "INSERT INTO Question (author_email, subject_id, subject_name, category, content,  created, image_Url, recognized_text) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (email, subject_id, subject_name,  category, content, created_date ,imageUrl, recog_text ))
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
    print(f'created_date : {created_date}')
    print(f'imageUrl : {imageUrl}')
    conn, cursor = db_connect()
    sql = "INSERT INTO Answer (author_email, question_id, content, created, image_Url, recognized_text) values(%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (email, question_id, content, created_date ,imageUrl, recog_text ))
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

def recent_question_db(question_num):
    question_list = list()
    conn, cursor = db_connect()
    #sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"       
    sql = "select * from Question order by question_id DESC limit 10" 
    cursor.execute(sql )

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
