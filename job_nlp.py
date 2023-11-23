import pandas as pd
import numpy as np
import os
from glob import glob
from pandas import ExcelWriter
from pandas import ExcelFile
from keras.preprocessing.text import Tokenizer
from datetime import datetime
import operator
import re

import pymysql
# import urllib.request
# from soynlp import DoublespaceLineCorpus
# from soynlp.word import WordExtractor
# from soynlp.tokenizer import LTokenizer

DATASET_DIR= 'FINAL_dataset/'
INPUT_DATASET_DIR = 'input_dataset/'
JOB_ROLE_DIR = DATASET_DIR + 'role_keyword_1130/'
CORE_FILE = DATASET_DIR + 'core_keyword_list_1130.xlsx'
TEST_FILE = INPUT_DATASET_DIR + 'label_wanted.xlsx'
# TEST_FILE = INPUT_DATASET_DIR + 'label_saramin.xlsx'


TITLE_LIST = []
ROLE_LIST = []
CORE_LIST = []

FLAG_DATASET_TYPE = ''

def db_connect():
    conn = pymysql.connect(host='',
                           user='', password='', db='', charset='utf8')
    cursor = conn.cursor()

    return conn, cursor

def db_close(conn):
    conn.commit()
    conn.close()

def SELECT_job(): 
    title = '변리사'
    conn, cursor = db_connect()
    sql = "SELECT * FROM job_dataset where title = %s"
    cursor.execute(sql, (title))
    records = cursor.fetchall()
    if len(records) > 0:
        print('data exists')
    else:
        print('data is NOT exist')
    db_close(conn)

def INSERT_job_info(title,core,role ):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "INSERT INTO job_dataset (title, core, role) values(%s,%s,%s)"
    cursor.execute(sql, (title, core, role))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from job_dataset"
    cursor.execute(sql)
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        print(f'INSERT is completed : {len(records)}')
        return True
    else:
        print('INSERT is failure')
        return False

def read_description(index):
    preprocessed_desc = []

    job_desc_df = pd.read_excel(TEST_FILE, sheet_name='Sheet1')
    FLAG_DATASET_TYPE = TEST_FILE.split('_')[2]

    if FLAG_DATASET_TYPE == 'wanted.xlsx':
        full_desc = job_desc_df.loc[[index],['주요업무','자격요건','우대사항']].values.tolist()[0]
        title = job_desc_df.loc[[index],['직무']].values.tolist()[0]
    elif FLAG_DATASET_TYPE == 'saramin.xlsx':
        full_desc = job_desc_df.loc[[index],['주요업무','자격요건','우대사항']].values.tolist()[0]
        title = job_desc_df.loc[[index],['구인광고 직무(이름)']].values.tolist()[0]
    
    title[0] = title[0].replace('\n',' ')
    # full_desc = full_desc.replace('\n', ' ')

    for i,item in enumerate(full_desc):
        pure_text = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", str(item))
        preprocessed_desc.append(pure_text.replace('\n',' '))

    return title[0], preprocessed_desc


def upload_job_dataset():
    directory = os.path.abspath(JOB_ROLE_DIR)
    file_list = os.listdir(directory)
    job_list = [file for file in file_list if file.endswith(".xlsx")]

    SELECT_job()
    
    for i, filename in enumerate(job_list):
        print(f'processing ... [ {filename} ]')
        title, role = read_ROLE_keyword(filename)
        # TITLE_LIST.append(title)
        core_keyword =  read_core_keyword(i,CORE_FILE)
        print(f'[ {title} ] : {core_keyword}]')
        INSERT_job_info(title,core_keyword,role )
    
def read_ROLE_keyword(filename):
    ROLE_KEYWORD_FILE = JOB_ROLE_DIR + filename
    UserExcel = pd.read_excel(ROLE_KEYWORD_FILE, sheet_name='Sheet1')
    keyword_list = UserExcel['keywords'].tolist()
    raw_title = UserExcel['title'].tolist()[0]
    # TITLE_LIST.append(title)

    raw_role = keyword_list[0].replace('\n',' ').replace('\t',' ')
    # ROLE_LIST.append(keyword_list[0])

    return raw_title, raw_role
    

def read_core_keyword(index, filename):
    CORE_KEYWORD_FILE = filename
    core_df = pd.read_excel(CORE_KEYWORD_FILE, sheet_name='Sheet1')
    
    job_file_list = core_df.loc[[index],['job_file']].values.tolist()[0]
    job_title_list = core_df.loc[[index],['job_title']].values.tolist()[0]
    core_keyword_list = core_df.loc[[index],['core_keywords']].values.tolist()[0]
    # CORE_LIST.append(core_keyword_list[0])

    return core_keyword_list[0]

def get_size_description(filename = TEST_FILE):
    job_desc_df = pd.read_excel(TEST_FILE, sheet_name='Sheet1')
    return job_desc_df.shape[0]

def gen_word_vector(description):

    tk = Tokenizer()
    tk.fit_on_texts(description)

    desc_word = []
    for i, word in enumerate(tk.word_index.items()):
        desc_word.append(word[0])

    return desc_word

def read_input_dataset(job_list_index):
    desc_title = ''
    full_desc, desc_word = [],[]
    matching_dict = {}
   
    desc_title, full_desc = read_description(job_list_index)
    desc_word = gen_word_vector(full_desc)
    print(f'desc_word : {desc_word}')    
    return desc_title, full_desc, desc_word

def read_ROLE_info():
    directory = os.path.abspath(JOB_ROLE_DIR)
    file_list = os.listdir(directory)
    job_list = [file for file in file_list if file.endswith(".xlsx")]

    for i, filename in enumerate(job_list):
        print(f'processing ... [ {filename} ]')
        read_ROLE_keyword(filename)
        read_core_keyword(i,CORE_FILE)
    return job_list 

if __name__ == "__main__":
    JOB_LIST = read_ROLE_info()
    JOB_LIST_SIZE = get_size_description()

    # desc_title, estimated_title, final_score, score_list, core_list = gen_report(0)
    # print(f'core_list :{core_list}')
    
    final_pd = pd.DataFrame(columns=['desc_title','estimated_title','final_score','score_var','score_std', 'core_keywords'])

    # with open(RESULT_DIR + 'RESULT_estimated_job_SARAMIN_' + FILE_NAME_EXT + '.csv', 'a', -1, 'utf-8') as f:
        # f.write('test data line')
    # FILE_NAME_EXT = nowDate.strftime("%Y-%m-%d-%H-%M")

    for i in range(2):#range(JOB_LIST_SIZE):
        desc_title, full_desc, desc_word = read_input_dataset(i)
        # print(f'[{desc_title}] [{estimated_title}] {core_list}')
 
