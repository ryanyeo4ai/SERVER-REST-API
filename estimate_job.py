import pandas as pd
import numpy as np
import os
from glob import glob
from pandas import ExcelWriter
from pandas import ExcelFile
from datetime import datetime
import operator
import re
# from keras.preprocessing.text import Tokenizer
import pymysql
import pickle

from han_eng_token import *

FLAG_WRITE = False

DATASET_DIR= 'FINAL_dataset/'
INPUT_DATASET_DIR = 'input_dataset/'
TEST_FILE = INPUT_DATASET_DIR + 'label_wanted.xlsx'

TITLE_LIST = []
ROLE_LIST = []
CORE_LIST = []
FREQ_dict = {}

FLAG_DATASET_TYPE = ''

def db_connect():
    conn = pymysql.connect(host='',
                           user='', password='', db='', charset='utf8')
    cursor = conn.cursor()

    return conn, cursor

def db_close(conn):
    conn.commit()
    conn.close()

def LOAD_job_list(): 
    title_list = []
    core_list = []
    role_list = []

    job_index = 1

    conn, cursor = db_connect()
    sql = "SELECT * FROM job_dataset"
    cursor.execute(sql)
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            title_list.append(row[1])
            core_list.append(row[2])
            role_list.append(row[3])
    else:
        print('NO job data ')

    return title_list, core_list, role_list



def gen_word_vector(description):
    desc_word  = []
    # print(f'description :{description}')
    # target_desc = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", " ",description)
    # # print(f'target_desc :{target_desc}')
    # pre_1step_list = target_desc.split(' ')
    # print(f'pre_1step_list :{pre_1step_list}')
    pre_1step_list = get_han_eng_token(description)
    for i in range(len(pre_1step_list)):
        desc_word.append(pre_1step_list[i])
    
    return desc_word

def gen_word_token(description):

    tk = Tokenizer()
    tk.fit_on_texts(description)

    desc_word = []
    for i, word in enumerate(tk.word_index.items()):
        desc_word.append(word[0])

    return desc_word

def word_vectorize(extracted_desc):

    desc_word = gen_word_vector(extracted_desc)
    # desc_word = gen_word_token(extracted_desc)
    return desc_word

def estimate_keyword(description, TITLE_LIST, ROLE_LIST, CORE_LIST):
    desc_title = ''
    desc_word = []
    ROLE_KEYWORD_LIST = []
    CORE_KEYWORD_LIST = []
    matching_dict = {}

    print(f'# of TITLE_LIST :{len(TITLE_LIST)}')
    desc_word = word_vectorize(description)
    # if FLAG_WRITE == False:
    print(f'desc_word : {desc_word}')
    MAX_KEYWORD_COUNT = -1
    SELECTED_ROLE_INDEX = -1
   
    flag_role_CORE_list = []
    CORE_TITLE = ''

    for role_index in range(len(ROLE_LIST)):
        core_low = []
        role_low = []
        flag_role_CORE = False
        ROLE_KEYWORD_LIST = ROLE_LIST[role_index].split(',')
        role_low = [i.strip().lower() for i in ROLE_KEYWORD_LIST]
        ROLE_KEYWORD_LIST = role_low

        CORE_KEYWORD_LIST = CORE_LIST[role_index].split(',')
        core_low = [i.strip().lower() for i in CORE_KEYWORD_LIST]
        CORE_KEYWORD_LIST = core_low

        matching_score = 0
        check_ROLE_keyword = []
        check_CORE_keyword = []
        title_CORE = ''
        selected_core = ''
        for index in range(len(desc_word)):
            DESC_WORD = desc_word[index].strip().lower() 
            for i in range(len(ROLE_KEYWORD_LIST)):
                role_word = ROLE_KEYWORD_LIST[i].strip().lower()
                if DESC_WORD in role_word:
                    check_ROLE_keyword.append(ROLE_KEYWORD_LIST[i])
                    matching_score += 1
            
            # print(f'DESC_WORD : {DESC_WORD}')
            # if 'PHP' in CORE_KEYWORD_LIST:
            #     print(f'CORE_KEYWORD_LIST : {CORE_KEYWORD_LIST}')
            if DESC_WORD in CORE_KEYWORD_LIST:
                # matching_score += 50
                # flag_role_CORE = True

                for i in range(len(CORE_KEYWORD_LIST)):
                    target_word = DESC_WORD.strip().lower() #DESC_WORD.replace(' ','').lower()
                    # print(f'target_word : {target_word}')
                    core_word = CORE_KEYWORD_LIST[i].strip().lower()
                    # print(f'core_word :{core_word}')
                    if target_word == core_word:
                        # print(f'matched target_word :{target_word}')
                        if gen_freq_count_word(target_word) < 100:
                            check_CORE_keyword.append(CORE_KEYWORD_LIST[i])
                            if len(selected_core) == 0:
                                selected_core = CORE_KEYWORD_LIST[i]
                            else:
                                selected_core = selected_core + ',' + CORE_KEYWORD_LIST[i]
                            matching_score += 50
                            flag_role_CORE = True
                    
            
        if matching_score > 0:
            matching_dict[TITLE_LIST[role_index]] = matching_score

            if MAX_KEYWORD_COUNT < matching_score:
                SELECTED_ROLE_INDEX = role_index
                MAX_KEYWORD_COUNT = matching_score
                if flag_role_CORE :
                    title_CORE = TITLE_LIST[SELECTED_ROLE_INDEX]
                    CORE_TITLE = title_CORE
                    flag_role_CORE_list.append(selected_core)
                else:
                    flag_role_CORE_list = []

    score_list = []
    final_score = 0          
    if SELECTED_ROLE_INDEX > -1:
        sorted_matching_dict = dict(sorted(matching_dict.items(), key=operator.itemgetter(1), reverse=True))
        rank_index = 1
        for key, score in sorted_matching_dict.items():
            # print(f'[ RANK {rank_index} ] : {key}, score : {score}')
            score_list.append(score)
            rank_index += 1
        final_score = MAX_KEYWORD_COUNT

    final_CORE = ''
    if len(flag_role_CORE_list) > 0: 
        final_CORE = flag_role_CORE_list[-1]

    return TITLE_LIST[SELECTED_ROLE_INDEX], final_score, CORE_TITLE, final_CORE
    # return {
    #     "title" : TITLE_LIST[SELECTED_ROLE_INDEX],
    #     "score" : final_score,
    #     "core_title" : CORE_TITLE,
    #     "selected_core_keyword" : final_CORE
    # }

def gen_freq_count_word(word):

    if word in FREQ_dict:
        value = FREQ_dict[word]
        return value
    else:
        return 0

def LOAD_FREQ_dict():
    data_dict = {}
    with open('FREQ_dict.pkl','rb') as f:
        data_dict = pickle.load(f)

    return data_dict

def estimate_job_title_role(full_desc):
    estimated_json = {}
    TITLE_LIST = []
    CORE_LIST = []
    ROLE_LIST= []
    TITLE_LIST, CORE_LIST, ROLE_LIST = LOAD_job_list()
    
    
    Final_title, FINAL_score, Final_core_title, Final_core_keywords = estimate_keyword(full_desc, TITLE_LIST, ROLE_LIST, CORE_LIST)
    print(f'core list : {Final_core_keywords}')
    if len(Final_core_title) == 0:
        Final_title = 'No Matching'
    else:
        Final_title = Final_core_title
        
    return Final_title, FINAL_score

def get_size_description(filename = TEST_FILE):
    # job_desc_df = pd.read_excel(TEST_FILE, sheet_name='Sheet1')
    # return job_desc_df.shape[0]
    size = 733
    return size

def read_test_file(df, index):
    preprocessed_desc = ''

    full_desc = df.loc[[index],['주요업무','자격요건','우대사항']].values.tolist()[0]
    # title = df.loc[[index],['구인광고 직무(이름)']].values.tolist()[0]
    title = job_desc_df.loc[[index],['직무']].values.tolist()[0]
    
    title[0] = title[0].replace('\n',' ')
    title[0] = title[0].replace('\t',' ')
    # full_desc = full_desc.replace('\n', ' ')

    for i,item in enumerate(full_desc):
        pure_text = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", str(item))
        pure_text = pure_text.strip()
        preprocessed_desc = preprocessed_desc + ' ' + pure_text.replace('\n',' ')
        
    # preprocessed_desc = title[0] + ' ' + preprocessed_desc
    return title[0], preprocessed_desc

if __name__ == "__main__":

    FREQ_dict = dict(LOAD_FREQ_dict())
    input_file_size = get_size_description()
    
    desc_title = '웹 디자이너'
    full_desc = '• 웹사이트 제품 상세페이지 / 광고 컨텐츠 디자인• 이벤트 및 프로모션 디자인 (리플렛 포함)• 소셜/오픈마켓/쇼핑몰용 웹 컨텐츠 기획 제작• 제품 그래픽 이미지 보정/합성 및 편집• 제품 용기 패키지 디자인 기획 개발 및 생산관리'
    Final_title, FINAL_score = estimate_job_title_role(full_desc)
    # print(f'{Final_title}-{FINAL_score}-{Final_core_title}-{Final_core_keywords}')
    
    print(f'title : {Final_title} , score : {FINAL_score}')
