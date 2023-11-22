import hgsysinc
from hgchartype import HGGetToken
# 하이브리 글자 타입
# string1 = "벙커C유  대책T/F  워싱턴D.C  갤S10  비타민B1  중2  미그21  미그-21 "
# string2 = "2000㏄  2000cc  2천CC   80km/h   1/2   16.6g   1/4분기  06/1/18 "
# string3 = "D-데이   e-북    CD-롬    K-팝   M&A   CD-ROM  K-POP "
# string4 = " S-Oil   H5N1    A1-광구   U.S. "
# string_hybrid = "D-데이 D데이 용기 apple,패키지 디자인 가능자 우대• 포토샵, 일러스트 등 툴 숙련자• 웹 디자인과 제품 패키지 디자인 경력이 있으신 분• 코스메틱에 대한 기본적 지식 및 관심이 높으신 분"


def get_han_eng_token(string_hybrid):
    toknum = 0
    token_list = []
    # print(f'string_hybrid : {string_hybrid}')
    toklist = HGGetToken(string_hybrid)
    # print(toklist)
    for tok in toklist:
        word = tok['string']
        # print(f'word :{word}')
        if tok['script'] == 'H' or tok['script'] == 'E':
            if tok['len'] > 1:
                token_list.append(tok['string'])
    #     if(word.isspace() == False):
    #         print(tok['string'], end='\t')
    #         toknum += 1
    # print(), print('HGGetToken toknum :', toknum)

    return token_list

