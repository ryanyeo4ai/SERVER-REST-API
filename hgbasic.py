#-------------------------------
#-------------------------------
import inspect


#-------------------------------
#-------------------------------
__debug_print_on__ = False

#-------------------------------
#-------------------------------
#frame = inspect.currentframe()
# __FILE__ = inspect.currentframe().f_code.co_filename
__LINE__ = fileNo = inspect.currentframe().f_lineno
__FUNCTION__ = inspect.stack()[0][3]

def _func_line_():
  callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  #print(info.filename)                      # __FILE__     -> Test.py
  #print(info.function)                      # __FUNCTION__ -> Caller
  #print(info.lineno)                        # __LINE__     -> 13
  print(info.lineno, 'line', 'at', info.function, '[', info.filename, ']')

def _print_function_name_(prelinefeed=0):
    if(prelinefeed > 0): # 함수 이름을 출력하기 전에 줄바꿈을 할 것인가?
        for i in range(prelinefeed):
            print()
            if(i >= 20): # '20'번 이상은 줄바꿈을 하지 않는다.
                break
    #
    import sys
    print(sys._getframe(1).f_code.co_name,'()') # 이 함수를 호출한 함수 이름
    #=print(sys._getframe(0).f_code.co_name,'()') # 현재 여기 함수 이름


#-------------------------------
#-------------------------------
__HG_SYL_NUM__ = 11172  # (ord('힣') - ord('가') + 1)
__HG_SYL_LEADING_DEC__ = 44032 # ord('가'), 0xAC00
__HG_CHO_NUM__ = 19 # 초성 개수
__HG_JUNG_NUM__ = 21 # 중성 개수
__HG_JONG_NUM__ = 28 # 종성 개수[종성(27) + 채움(1)]

__HG_JUNG_X_JONG_NUM__ = (__HG_JUNG_NUM__ * __HG_JONG_NUM__) # 중성 개수 x 종성 개수 = 588

#-------------------------------
#-------------------------------
def debug_print_on():
    global __debug_print_on__
    __debug_print_on__ = True

def debug_print_off():
    global __debug_print_on__
    __debug_print_on__ = False

def get_backword_string(str):
    #-----
    #=backword_str = ''
    #=hglen = len(str)
    #=for i in range(, , -1):
    #=    backword_str += str[i - 1]
    #-----
    backword_str = str[::-1]  # slicing 가장 빠르다. 다른 방식에 비해 최소 5배 이상 빠름
    return backword_str

def get_char_code_value_string3(char1, decFlag=True, hexFlag=True, sep=' '):
    char_code_value_string = ''
    if(len(char1) != 1):
        print('logic error :', '(len(char1) != 1)', __FUNCTION__, __name__)
        return char_code_value_string
    char_code_value_string = char1
    if(decFlag == True):
        char_code_value_string += sep
        char_code_value_string += str(ord(char1))
    if(hexFlag == True):
        char_code_value_string += sep
        hexchar1 = hexUpper(ord(char1))
        char_code_value_string += hexchar1
    return char_code_value_string

def get_hangul_syllable__index(cho_i, jung_i, jong_i=0, SyllableFalg=True):
    """
    초성, 중성, 종성 자모 인덱스로 음절 문자 변환
    if(SyllableFalg==True) 음절 문자로 반환, else 음절 인덱스로 반환
    """
    #print(cho_i, jung_i, jong_i,)
    if(SyllableFalg == True):  # 한글 음절을 돌려준다.
        syllable = ""
    else: # 한글 음절 인덱스를 돌려준다.
        syllable = (-1)
    #
    if((cho_i < 0) or (cho_i >= __HG_CHO_NUM__)): # 초성 범위
        return syllable
    if((jung_i < 0) or (jung_i >= __HG_JUNG_NUM__)): # 중성 범위
        return syllable
    if((jong_i < 0) or (jong_i >= __HG_JONG_NUM__)): # 종성 범위
        return syllable
    #
    syllable_index = (cho_i * __HG_JUNG_X_JONG_NUM__) + \
                        (jung_i * __HG_JONG_NUM__) + jong_i
    if(SyllableFalg == True):  # 한글 음절을 돌려준다.
        syllable = chr(syllable_index + __HG_SYL_LEADING_DEC__)
        return syllable
    else: # 한글 음절 인덱스를 돌려준다.
        return syllable_index

def PrintCodeValueBlock_Num(beginVal, charNum, decFlag=True, hexFlag=True, sep=' '):
    for i in range(0, charNum):
        char1 = chr(i + beginVal)
        char_code_value_string3 = get_char_code_value_string3(char1, decFlag=decFlag, hexFlag=hexFlag, sep=sep)
        print('%i :' %(i+1), sep, char_code_value_string3)
    print('total :', charNum)
    print()

    for i in range(0, charNum):
        print(chr(i + beginVal), end='')
    print()

def PrintCodeValueBlock_Value(beginVal, endVal):
    if(isinstance(beginVal, int) != True):
        print('logic error :', '(type(beginVal) != int) at',  __FUNCTION__)
        return
    if(isinstance(endVal, int) != True):
        print('logic error :', '(type(endVal) != int) at',  __FUNCTION__)
        return
    charnum = (endVal - beginVal) + 1
    PrintCodeValueBlock_Num(beginVal, charnum)

def PrintCodeValueBlock_Char(beginChar, endChar):
    if((len(beginChar) != 1) or (len(endChar) != 1)):
        print('logic error :', '((len(beginChar) != 1) or (len(endChar) != 0))')
        return
    #
    beginVal = ord(beginChar)
    endVal = ord(endChar)
    PrintCodeValueBlock_Value(beginVal, endVal)

def PrintCodeValue_String(String, sep=' '):
    hglen = len(String)
    tmpStr = ''
    for i in range(0, hglen):
        char1 = String[i]
        char_code_value_string3 = get_char_code_value_string3(char1, sep=sep)

        # print('%i :' %(i+1), sep, char_code_value_string3) # 너무 느려서 바꾼다.
        tmpStr += str(i + 1)
        tmpStr += sep
        tmpStr += char_code_value_string3
        tmpStr += '\n'
        if((i % 100) == 1):
            print(tmpStr, end='')
            tmpStr = ''
    print(tmpStr, end='')

def MakeCodePageString_16__Char(beginChar, label=True, DelLastHexChar=True, xValue=16):
    CharCode = ord(beginChar)
    CodePageString_16x16 = MakeCodePageString_16(CharCode, label=label, DelLastHexChar=DelLastHexChar, xValue=xValue)
    return CodePageString_16x16

def MakeCodePageString_16(CharCode, label=True, DelLastHexChar=True, xValue=16):
    #
    CodePageString = ''

    #--- code table _ line-break-16_x_16
    if(label == True):
        # caption 
        for cap in range(0, 16):
            if(cap == 0):
                CodePageString += '0x'
                CodePageString += '\t'
            CodePageString += hexUpper(cap)
            CodePageString += '\t'
        CodePageString += '\n'

    curCharCode = CharCode
    choCount = 1
    lineCount = 1
    charCount = 1
    range_line = xValue
    for v in range(0, range_line):
        for t in range(0, 16):
            #print(charCount) # dbg-print
            if(label == True):
                if(t == 0): # label
                    hexChar = hexUpper(curCharCode)
                    if(DelLastHexChar==True): # 16진수의 마지막 글자를 지우기
                        hexChar = hexChar[0: len(hexChar) - 1]
                    CodePageString += hexChar
                    CodePageString += '\t'
            #print(curChar, end='')
            curChar = chr(curCharCode)
            if(curChar.isprintable() == True):
                CodePageString += curChar
            else: # 출력이 안 되는 문자
                # 사용자 영역은 공백 문자로 바꾸지 말고 그대로 전달한다.
                if((curCharCode >= 0xE000) and (curCharCode <= 0xF8FF)):
                    CodePageString += curChar
                else: # 출력이 안 되면 공백 문자로 바꾼다.
                    CodePageString += ' '
            CodePageString += '\t'

            charCount += 1
            curCharCode += 1
        CodePageString += '\n'
        lineCount += 1
    charCount -= 1
    #print(charCount) # 총 출력 문자수

    return CodePageString

def print_debug_msg(msg):
    if(__debug_print_on__ == True):
        print(msg)

def print_debug_msg_line(msg):
    if(__debug_print_on__ == True):
        print(__file__, __FUNCTION__, __LINE__, '\n', msg)

def find_mismatch_pos(str1, str2, match_len=0, state_print=False, print_len = 10):
    len1 = len(str1)
    len2 = len(str2)
    pos = 0
    while(pos < len1):
        char1 = str1[pos]
        char2 = str2[pos]
        if(char1 != char2):
            if(state_print == True):
                print('mis-match: ', pos)
                print('[a]', str1[pos:pos+print_len])
                print('[b]', str2[pos:pos+print_len])
                print()
            return pos
        pos += 1
        if(match_len > 0): # 비교 길이가 있으면 확인
            if(pos >= match_len):
                break
    return (-1)

def find_mismatch_pos_list(baseStr, compStr, mismatch_control_len = 5):
    # mismatch_control_len = 5 # 일치하지 않는 부분이 발견되면 '5'글자까지만 조정해본다
    mismatch_pos_list = []

    #
    base_mismatch_pos_total = 0
    comp_mismatch_pos_total = 0
    mismatch_cnt = 1
    while(1):
        mismatch_pos = find_mismatch_pos(baseStr, compStr)
        if(mismatch_pos < 0):
            break
        #-----------
        #-----------
        ##print('[%i]위치:' %mismatch_cnt, mismatch_pos_total, '(',mismatch_pos,')')
        ##print(baseStr[mismatch_pos:mismatch_pos+10])
        ##print(compStr[mismatch_pos:mismatch_pos+10])
        mismatch_cnt += 1

        base_mismatch_pos_total += mismatch_pos
        comp_mismatch_pos_total += mismatch_pos
        mismatch_pos_item = {'base':base_mismatch_pos_total, 'comp':comp_mismatch_pos_total}
        mismatch_pos_list.append(mismatch_pos_item)

        #-----------
        # 새로운 위치를 찾아본다.
        #-----------
        baseStr_new = baseStr[mismatch_pos:]
        compStr_new = compStr[mismatch_pos:]

        # check first1
        new_base_pos = 0
        new_comp_pos = 0
        new_mismatch_pos = 0
        while(1):
            if(new_base_pos >= mismatch_control_len):
                break
            
            new_mismatch_pos = 0
            new_comp_pos = 0
            while(1):
                #print(new_base_pos, new_comp_pos)
                #print(baseStr_new[new_base_pos:20])
                #print(compStr_new[new_comp_pos:20])
                if(new_comp_pos >= mismatch_control_len):
                    break
                new_mismatch_pos = find_mismatch_pos(baseStr_new[new_base_pos:], compStr_new[new_comp_pos:], match_len=mismatch_control_len)
                #print('new_mismatch_pos:',new_mismatch_pos)
                if(new_mismatch_pos >= 0):
                    new_comp_pos += 1
                    continue
                elif(new_mismatch_pos < 0): # match
                    break
            if(new_mismatch_pos < 0): # match
                break
            new_base_pos += 1
        if(new_mismatch_pos < 0): # match
            baseStr = baseStr_new[new_base_pos:]
            compStr = compStr_new[new_comp_pos:]
            #print('---새로운 일치---')
            #print(baseStr[:20])
            #print(compStr[:20])

            base_mismatch_pos_total += new_base_pos
            comp_mismatch_pos_total += new_comp_pos

            continue
        break
    return mismatch_pos_list

def hexUpper(curVal, add_0x = False):
    if(isinstance(curVal, int) == False):
        return ''
    curHex = hex(curVal)
    curHex = curHex[2:]
    curHex = curHex.upper()
    if(add_0x == True):
        curHex = '0x' + curHex
    return curHex

def hexUpper2(curVal_1, curVal_2, add_0x = False):
    hex1 = hexUpper(curVal_1, add_0x = add_0x)# 앞에 글자에는 옵션에 따라서 '0x'를 붙인다.
    hex2 = hexUpper(curVal_2, add_0x = False) # 뒤에 글자에는 '0x'를 붙이지 않는다.
    curHex = hex1 + hex2
    return curHex

def hexChar(codeval, add_0x = False):
    if(isinstance(codeval, int) == False):
        return ''
    curHex = hex(codeval)
    curHex = curHex[2:]
    if(add_0x == True):
        curHex = '0x' + curHex
    return curHex

def PrintList_ByLine(List, NumInLine=1, SortFlag=False, Printnum=None, ShowIndex=True, SepInLine='\t'): 

    if(SortFlag == True):
        PrtList = sorted(List)
    else:
        PrtList = List
    for i, x in enumerate(PrtList):
        if(ShowIndex==True):
            print(i, ': ', end='')
        print(x, end='')
        if(NumInLine <= 1): # 한줄에 1개 출력
            print()
        else: # 한줄에 여러 개 출력
            print(SepInLine, end='')
            if(((i + 1) % NumInLine) == 0): # 한 줄당 몇개 출력
                if(i != 0): # 맨처음은 출력하면 안 된다.
                    print()

        #            
        i += 1
        if ((Printnum != None) and (Printnum > 0)):
            if i >= Printnum:
                break

def PrintDictList_ByLine(DictList, ShowIndex=True, SortFlag=False, Printnum=None): 
    if(SortFlag == True):
        PrtList = sorted(DictList)
    else:
        PrtList = DictList
    for i, x in enumerate(PrtList):
        if(ShowIndex==True):
            print('%i' %i, ':', end='')
        print(x)
        #
        i += 1
        if ((Printnum != None) and (Printnum > 0)):
            if i >= Printnum:
                break

def GetCharDictList_CharList(charlist):
    char_dict_list = []

    charlist_sort = charlist.copy()
    charlist_sort.sort() # by abc

    i = 0
    pre_c = None
    for c in charlist_sort:
        #print(i)
        append_flag = False
        if(i == 0):
            append_flag = True
        else:
            if(pre_c['char'] == c):
                freq = pre_c['freq']
                freq += 1
                pre_c['freq'] = freq
                c = pre_c
            else:
                append_flag = True

        if(append_flag == True):
            char_dict = {'char': c, 'freq': 1, 'code': ord(c), 'hex': hex(ord(c))}
            char_dict_list.append(char_dict)
            pre_c = char_dict
        else:
            pre_c = c
        # next
        i += 1
        #print(pre_c)

    return char_dict_list

def GetCharDictList_String(string):
    charlist = [char for char in string]
    char_dict_list = GetCharDictList_CharList(charlist)
    return char_dict_list

def GetTextFileList(filename, encoding='utf-8', ReadNum=-1, EraseEOL=True, PrintTextFlag = False):
    ### 줄 단위 텍스트 읽기
    TextList = []

    if filename.is_file():
        if filename.exists():pass
        else: return TextList
    else:
        print("file not found: %s" %filename)
        return TextList

    file = open(filename, 'r', encoding=encoding)

    ReadCnt = 0;
    while True:
        line = file.readline()
        if not line: 
            break
        if(PrintTextFlag == True): 
            print(line)

        if(EraseEOL == True):
            line = line.rstrip('\n')
        TextList.append(line)

        ###            
        ReadCnt += 1;
        if(ReadNum > 0): # 읽을 개수 검사
            if(ReadCnt >= ReadNum):
                break;

    file.close()
    return TextList

def PrintDict_ByLine(PDict, ShowIndex=True, Printnum=None, RoundNum=0, OnlyKey=False): 
    PrtDict = PDict
    for i, key in enumerate(PrtDict):
        if(ShowIndex==True):
            print('%i' %i, ':', end='')
        #
        print(f'{key} :', end='')
        if(OnlyKey == True):
            pass
        else:
            if(RoundNum != 0):
                print(f'\t', round(PrtDict[key], RoundNum), end='')
            else:
                print (f'\t{PrtDict[key]}', end='')
        print()

        #
        i += 1
        if ((Printnum != None) and (Printnum > 0)):
            if i >= Printnum:
                break

def PrintDict_KeyValue_ByLine(PDict, ShowIndex=True, Printnum=None, SepChar=None): 
    #=print(), print(*PDict.items(), sep='\n')
    print()
    for i, Dict in enumerate(PDict):
        if(ShowIndex==True):
            print(f'{i}', end='')

        if(SepChar == None):
            print(f': {Dict}({PDict[Dict]})')
        else: # 탭문자 구분
            print(SepChar, *PDict[Dict], sep='\t')
        #
        i += 1
        if ((Printnum != None) and (Printnum > 0)):
            if i >= Printnum:
                break

def PrintDictKeyFreq(PDict, ShowMoreZero=False, RoundNum=0, 
    SimpleFormat=False, Printnum=None, ShowIndex=True, PrintFreqOrder=False, 
    SortByHigh=False, OnlyKey=False, ExcFilter=None):
    # format: dict{'key':value}

    #=import collections
    #=token_sort = collections.OrderedDict(sorted(PDict.items()))
    #=for key, value in token_sort.items():
    #=    print (f'{key}:\t{value}')

    print()
        
    if(PrintFreqOrder == True):
        #= dict format: {key: val for key, val in sorted(PDict.items(), key=lambda item: -item[1])}
        if(SortByHigh == True):
            dict_by_values = sorted(PDict.items(), key=lambda item: -item[1]) # by high
        else:
            dict_by_values = sorted(PDict.items(), key=lambda item: item[1]) # by low
        inx = 0
        for key in dict_by_values:
            printFlag = False
            if(ShowMoreZero == True): # '0'보다 큰 값만 출력
                if(key[1] > 0):
                    printFlag = True
            else: # 모두 출력
                printFlag = True
            
            if(ExcFilter != None): # 제외 목록에 있으면 출력하지 않는다.
                if(key[0] in ExcFilter):
                    printFlag = False

            if(printFlag == True):
                if(SimpleFormat == True): # 줄바꿈을 하지 않는다.
                    print (f"'{key[0]}':", end='')
                    if(OnlyKey == True):
                        pass
                    else:
                        if(RoundNum != 0):
                            print (round(key[1], RoundNum), end='')
                        else:
                            print (f"{key[1]}", end='')
                else:
                    if(ShowIndex==True):
                        print((inx + 1), ':\t', end='')

                    print (f"'{key[0]}'", end='')
                    if(OnlyKey == True):
                        pass
                    else:
                        if(RoundNum != 0):
                            print (f'\t', round(key[1], RoundNum), end='')
                        else:
                            print (f'\t{key[1]}', end='')
                
                if(SimpleFormat == True):
                    print(', ', end='')
                else:
                    print()
                
                #
                inx += 1
                if ((Printnum != None) and (Printnum > 0)):
                    if inx >= Printnum:
                        break
        if(SimpleFormat == True): 
            print() # 위에서 문단 구분이 없기 때문에 넣어야 한다.

        # gab = first - last 
        dict_by_values_first = dict_by_values[0]
        dict_by_values_last = dict_by_values[len(dict_by_values) - 1]
        value_gab = (dict_by_values_first[1] - dict_by_values_last[1])
        if(value_gab < 0): # 음수이면 양수로 변환 => 절대값
            value_gab = -value_gab
        print ('[Gab : High - Low]', value_gab)
        print('[First]', dict_by_values_first)
        print('[Last]', dict_by_values_last)

    else:
        if(SortByHigh == True):
            dict_by_keys = sorted(PDict.items(), key=lambda item: item[0], reverse=True) # by key: z->a
        else:
            dict_by_keys = sorted(PDict.items(), key=lambda item: item[0]) # by key: a->z
        inx = 0
        for key in dict_by_keys:
            printFlag = False
            if(ShowMoreZero == True): # '0'보다 큰 값만 출력
                if(key[1] > 0):
                    printFlag = True
            else: # 모두 출력
                printFlag = True

            if(ExcFilter != None): # 제외 목록에 있으면 출력하지 않는다.
                if(key[0] in ExcFilter):
                    printFlag = False

            if(printFlag == True):
                if(SimpleFormat == True): # 줄바꿈을 하지 않는다.
                    print (f"'{key[0]}':", end='')
                    if(OnlyKey == True):
                        pass
                    else:
                        if(RoundNum != 0):
                            print (round(key[1], RoundNum), end='')
                        else:
                            print (f"{key[1]}", end='')
                else:
                    if(ShowIndex==True):
                        print((inx + 1), ':\t', end='')
                    print (f"'{key[0]}':", end='')
                    if(OnlyKey == True):
                        pass
                    else:
                        if(RoundNum != 0):
                            print (f'\t', round(key[1], RoundNum), end='')
                        else:
                            print (f'\t{key[1]}', end='')
                if(SimpleFormat == True): # 줄바꿈을 하지 않는다.
                    print(', ', end='')
                else:
                    print()

                #
                inx += 1
                if ((Printnum != None) and (Printnum > 0)):
                    if inx >= Printnum:
                        break
    print()

def PrintDictKeyFreqs(PDicts, ShowMoreZero=False, RoundNum=0, SimpleFormat=False, 
    ShowIndex=True, PrintFreqOrder=False, SortByHigh=False, ExcFilter=None):
    print()
    for PDict in PDicts:
        PrintDictKeyFreq(PDict, ShowMoreZero=ShowMoreZero, RoundNum=RoundNum, 
            SimpleFormat=SimpleFormat, ShowIndex=ShowIndex, 
            PrintFreqOrder=PrintFreqOrder, ExcFilter=ExcFilter)
    print()

def PrintSet(PSet, SortFlag=False, ShowIndex=True):
    if(SortFlag == True):
        p_keys = sorted(PSet)
    else:
        p_keys = PSet

    print()
    inx = 0
    for key in p_keys:
        if(ShowIndex==True):
            print((inx + 1), ':\t', end='')
        print (key)
        inx += 1
    print()

def GetDictKeyFreq_TotalFreq(KeyDict, FilterLen = None, FilterFreq = None):
    TotalFreq = 0

    if(KeyDict == None): 
        return TotalFreq
    
    FilterCnt = 0
    inx = 0
    for key in KeyDict:
        ### filter
        if(FilterLen != None):
            keyLen = len(key)
            if(FilterLen != keyLen):
                continue
        
        if(FilterFreq != None): # 빈도 필터
            if(FilterFreq != KeyDict[key]):
                continue

        ###            
        FilterCnt += 1
        TotalFreq += KeyDict[key]
    
    return TotalFreq

def GetDictKeyFreq_FreqListInfo(KeyDict, FilterLen = None):
    #
    FreqListInfo = []
    
    TotalFreq = 0

    if(KeyDict == None): 
        return FreqListInfo

    #
    p_values = sorted(KeyDict.items(), key=lambda item: -item[1]) # by high

    #
    FilterCnt = 0
    FreqList = []
    FreqListkey = None
    inx = 0
    for key in p_values:
        ### filter
        if(FilterLen != None):
            WordkeyLen = len(key[0])
            if(FilterLen != WordkeyLen):
                continue
        
        ###            
        FilterCnt += 1
        TotalFreq += key[1]

        AddFalg = False
        if(FreqListkey == None):
            AddFalg = True
        else:
            if(FreqListkey['freq'] == key[1]):
                FreqListkey['count'] += 1
            else:
                AddFalg = True

        if(AddFalg == True):
             FreqListkey = {'freq': key[1], 'count': 1}
             FreqList.append(FreqListkey)

    FreqListInfo = {'TotalFreq':TotalFreq, 'ListSum':FilterCnt, 'FilterLen':FilterLen, 'List':FreqList}
    return FreqListInfo

def GetDictKeyFreq_LenListInfo(KeyDict, FilterFreq = None):
    #
    LenListInfo = []
    
    TotalFreq = 0

    if(KeyDict == None): 
        return LenListInfo

    #
    p_values = sorted(KeyDict.items(), key=lambda item: -len(item[0])) # by key-len-high

    #
    FilterCnt = 0
    LenList = []
    LenListkey = None
    for key in p_values:
        #keyLen = len(key[0])
    
        ### filter
        #if(FilterLen > 0):
        #    if(FilterLen != len(key[0])):
        #        continue
        
        if(FilterFreq != None):
            if(FilterFreq != key[1]):
                continue

        ###            
        FilterCnt += 1
        TotalFreq += key[1]

        AddFalg = False
        if(LenListkey == None):
            AddFalg = True
        else:
            if(LenListkey['len'] == len(key[0])):
                LenListkey['count'] += 1
            else:
                AddFalg = True

        if(AddFalg == True):
             LenListkey = {'len': len(key[0]), 'count': 1}
             LenList.append(LenListkey)

    LenListInfo = {'TotalFreq':TotalFreq, 'ListSum':FilterCnt, 'FilterFreq':FilterFreq, 'List':LenList}
    return LenListInfo

def SplitListRate(datalist, rate=1.0):
    if(rate > 1.0):
        assert False, "(rate > 1.0)"
        
    result_list = [], []
    datanum = len(datalist)
    for i in range(0, datanum):
        item = datalist[i]
        per = (i + 1) / datanum
        if(per <= rate):
            result_list[0].append(item)
        else:
            result_list[1].append(item)
    return result_list

def GetAvg(NumList):
    return float(sum(NumList)) / max(len(NumList), 1)    

def get_filename_from_title(file_title):
    """문자열을 파일 이름에 적합하도록 변경
    """
    filename = file_title
    filename = filename.replace(' ', '_') # 공백문자를 '_'로 바꾼다.
    filename = filename.replace('-', '_') # '-'를 '_'로 바꾼다.
    filename = filename.replace('’s', '') # {’s}를 지운다.
    filename = filename.replace("'s", '') # {'s}를 지운다.
    filename = filename.replace(',', '_') # ','를 '_'로 바꾼다.
    filename = filename.replace('[', '_') # ','를 '_'로 바꾼다.
    filename = filename.replace(']', '_') # ','를 '_'로 바꾼다.
    filename = filename.replace('<', '_') # ','를 '_'로 바꾼다.
    filename = filename.replace('>', '_') # ','를 '_'로 바꾼다.
    filename = filename.replace('{', '_') # ','를 '_'로 바꾼다.
    filename = filename.replace('}', '_') # ','를 '_'로 바꾼다.
    filename = filename.replace('"', '_') # ','를 '_'로 바꾼다.
    filename = filename.replace("'", '_') # ','를 '_'로 바꾼다.
    #
    return filename


