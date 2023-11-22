from hgbasic import get_char_code_value_string3

#----------------------------------
#----------------------------------
글자상태_한글 = 'H' # 'Han'
글자상태_영문자 = 'E' # 'Eng'
글자상태_숫자 = 'N' # 'Num'
글자상태_공백 = 'S' # 'Spc'
글자상태_탭 = 'T' # 'Tab'
글자상태_리턴 = 'R' # 'CR'
글자상태_줄바꿈 = 'L' # 'LF'
글자상태_기호 = 'I' # 'Sign'
글자상태_자모 = 'h' # 'Jamo'
글자상태_한자 = 'C' # 'Hanja'
글자상태_일문자 = 'J' # 'Japan'
글자상태_라틴어 = 'e' # 'Latin' 
글자상태_라틴어3 = '3' # 'Latin3'
글자상태_라틴어4 = '4' # 'Latin4'
글자상태_라틴어5 = '5' # 'Latin5'
글자상태_음성 = 'P' # 'Phonetic' # Phonetic Extensions 1D00(ᴀ) ~ 1D7F(ᵿ)
#글자상태_그리스어 = 'G' # 'Greek'    # Greek and Coptic 0370(Ͱ) ~ 03FF(Ͽ) ==> 영문자 토큰에 있어야 한다.
글자상태_키릴 = 'Y' # 'Cyrillic' # Cyrillic 0400(Ѐ) ~ 04FF(ӿ)
글자상태_아랍어 = 'A' # 'Arabic'   # Arabic 0600(؀ ) ~ 06FF(‎ۿ‎)
#----- 
글자상태_엑스 = 'X' # 'Extra'
글자상태_널 = 'Z' # 'Zero'
#----- 
글자상태_몰라 = 'NotDefine'
#----------------------------------
#----------------------------------


def get_script(char1):
    # old: get_char_type
    if(len(char1) != 1): # 1글자만 허용
        return 0
    ord_char = ord(char1)
    if((ord_char >= 0xAC00) and (ord_char <= 0xD7A3)): 
        return 글자상태_한글 # hangul 0xAC00(가) 0xD7A3(힣))
    elif((ord_char >= ord('a')) and (ord_char <= ord('z'))):
         return 글자상태_영문자 # english # 0x0061(a) ~ 0x007a(z)
    elif((ord_char >= ord('A')) and (ord_char <= ord('Z'))): 
        return 글자상태_영문자 # english # 0x0041(A) ~ 0x005a(Z)
    elif((ord_char >= ord('ａ')) and (ord_char <= ord('ｚ'))): # 전각 알파벳
         return 글자상태_영문자 # fullwidth english # 0xff41(ａ) ~ 0xff5a(ｚ)
    elif((ord_char >= ord('Ａ')) and (ord_char <= ord('Ｚ'))): # 전각 알파벳
        return 글자상태_영문자 # fullwidth english # 0xff21(Ａ) ~ 0xff3a(Ｚ)
    elif((ord_char >= ord('0')) and (ord_char <= ord('9'))): 
        return 글자상태_숫자 # number # 0x0030(0) ~ 0x0039(9)
    elif((ord_char >= ord('０')) and (ord_char <= ord('９'))): # 전각 숫자
        return 글자상태_숫자 # number # 0xff10(０) ~ 0xff19(９)
    elif(ord_char == ord(' ')): 
        return 글자상태_공백 # space 0x0020
    elif(ord_char == ord('\t')): 
        return 글자상태_탭 # tab 0x0009
    elif(ord_char == ord('\r')): 
        return 글자상태_리턴 # carrage-return 0x000D	
    elif(ord_char == ord('\n')): 
        return 글자상태_줄바꿈 # line-feed  0x000A
    elif((ord_char >= 1) and (ord_char <= 127)): 
        return 글자상태_기호  # sign
    #----------------------------------
    #----------------------------------
    #----- Hangul Jamo
    elif((ord_char >= 0x1100) and (ord_char <= 0x11FF)): 
        return 글자상태_자모 # hangul Jamo 0x1100(ᄀ) 0x11FF(ᇿ))
    elif((ord_char >= 0xA960) and (ord_char <= 0xA97C)): 
        return 글자상태_자모 # hangul Jamo extended-A 0xA960(ꥠ) 0xA97C(ꥼ))
    elif((ord_char >= 0xD7B0) and (ord_char <= 0xD7C6)): 
        return 글자상태_자모 # hangul Jamo extended-B1 0xD7B0(ힰ) 0xD7C6(ퟆ))
    elif((ord_char >= 0xD7CB) and (ord_char <= 0xD7FB)): 
        return 글자상태_자모 # hangul Jamo extended-B2 0xD7CB(ퟋ) 0xD7FB(ퟻ))
    elif((ord_char >= 0x3131) and (ord_char <= 0x318E)): 
        return 글자상태_자모 # Hangul Compatibility Jamo 0x3131(ᄀ) 0x318e(ㆎ))
    elif((ord_char >= 0xFFA0) and (ord_char <= 0xFFDC)): 
        return 글자상태_자모 # hangul Jamo Halfwidth 0xFFA0(filler) 0xFFDC(ￜ)) # 'Halfwidth Hangul variants'
    #----------------------------------
    #----------------------------------
    #----- CJK Unified Ideographs -----
    elif((ord_char >= 0x4E00) and (ord_char <= 0x9FFC)): 
        return 글자상태_한자 # (20928) CJK Unified Ideographs 0x4E00(一) 0x9FFC(鿯) <= 화면 출력 안 됨
    elif((ord_char >= 0x3400) and (ord_char <= 0x4DBF)): 
        return 글자상태_한자 # (6592) CJK Unified Ideographs  Extension-A 0x3400(㐀) 0x4DBF(䶿) <= 화면 출력 안 됨
    elif((ord_char >= 0x20000) and (ord_char <= 0x2A6DD)): 
        return 글자상태_한자 # (42720) CJK Unified Ideographs  Extension-B 0x20000(𠀀) 0x2A6DD(�)
    elif((ord_char >= 0x2A700) and (ord_char <= 0x2B734)): 
        return 글자상태_한자 # (4160) CJK Unified Ideographs  Extension-C 0x2A700(�) 0x2B734(�)
    elif((ord_char >= 0x2B740) and (ord_char <= 0x2B81D)): 
        return 글자상태_한자 # (224) CJK Unified Ideographs  Extension-D 0x2B740(�) 0x2B81D(�)
    elif((ord_char >= 0x2B820) and (ord_char <= 0x2CEA1)): 
        return 글자상태_한자 # (5776) CJK Unified Ideographs  Extension-E 0x2B820(慐) 0x2CEA1(�) # {0x2B820(慐)}한자는 유니코드에서 보여주는 글자랑 다른 글자가 표시된 것이다.
    elif((ord_char >= 0x2CEB0) and (ord_char <= 0x2EBE0)): 
        return 글자상태_한자 # (7488) CJK Unified Ideographs  Extension-F 0x2CEB0(話) 0x2EBE0(�) # {0x2CEB0(話)}한자는 유니코드에서 보여주는 글자랑 다른 글자가 표시된 것이다.
    elif((ord_char >= 0x30000) and (ord_char <= 0x3134A)): 
        return 글자상태_한자 # (7488) CJK Unified Ideographs  Extension-F 0x30000() 0x3134A(侅)  # {0x3134A(侅)}한자는 유니코드에서 보여주는 글자랑 다른 글자가 표시된 것이다.
    #----- CJK Compatibility Ideographs -----
    elif((ord_char >= 0xF900) and (ord_char <= 0xFAFF)): 
        return 글자상태_한자 # CJK Compatibility Ideographs(한중일 호환용 한자)	0xF900(豈) - 0xFAFF {실제 글자는 0xFAD9(龎)까지}
    elif((ord_char >= 0x2F800) and (ord_char <= 0x2FA1F)): 
        return 글자상태_한자  # CJK Compatibility Ideographs Supplement(한중일 호환용 한자 보충) 0x2F800(丽) - 0x2FA1F {실제 글자는 0x2FA1D(𪘀)까지}
    #----- CJK Radicals / Kangxi Radicals -----
    elif((ord_char >= 0x2F00) and (ord_char <= 0x2FDF)): 
        return 글자상태_한자  # CJK Radicals / Kangxi Radicals  0x2F00(⼀) - 0x2FDF {실제 글자는 0x2FD5(⿕)까지}
    elif((ord_char >= 0x2E80) and (ord_char <= 0x2EFF)): 
        return 글자상태_한자  # CJK Radicals Supplement(한중일 부수 보충)	0x2E80(⺀) - 0x2EFF {실제 글자는 0x2EF3(⻳)까지}
    elif((ord_char >= 0x31C0) and (ord_char <= 0x31EF)): 
        return 글자상태_한자 # CJK Strokes  0x31C0(㇀) - 0x31EF {실제 글자는 0x31E3(㇣)까지}
    #----------------------------------
    #----------------------------------
    # 일본어 가나
    elif((ord_char >= ord('ぁ')) and (ord_char <= ord('ゟ'))):
        return 글자상태_일문자 # Hiragana 0x3041(ぁ) ~ 0x309F(ゟ)
    elif((ord_char >= ord('ァ')) and (ord_char <= ord('ヿ'))): 
        return 글자상태_일문자 # Katakana 0x30A1(ァ) ~ 0x30FF(ヿ)
    elif((ord_char >= ord('ㇰ')) and (ord_char <= ord('ㇿ'))):
        return 글자상태_일문자 # Katakana Phonetic Extensions 0x31F0(ㇰ) ~ 0x31FF(ㇿ)
    elif((ord_char >= 0x1B000) and (ord_char <= 0x1B0FF)): 
        return 글자상태_일문자   # Kana Supplement 0x1B000(𛀀) ~ 0x1B0FF(𛃿)
    elif((ord_char >= 0x1B100) and (ord_char <= 0x1B11E)): 
        return 글자상태_일문자   # Kana Extended-A 0x1B100(𛄀) ~ 0x1B11E(𛄞)
    elif((ord_char >= 0x1B150) and (ord_char <= 0x1B167)): 
        return 글자상태_일문자   # Small Kana Extension 0x1B150(𛅐) ~ 0x1B167(𛅧)
    elif((ord_char >= 0xFF65) and (ord_char <= 0xFF9F)): 
        return 글자상태_일문자   # Halfwidth Katakana variants 0xFF65(･) ~ 0xFF9F( ﾟ)
    elif((ord_char >= ord('〱')) and (ord_char <= ord('〵'))): 
        return 글자상태_일문자 # Kana repeat marks 0x3031(〱) ~ 0x3035(〵) <= CJK Symbols and Punctuation
    #----------------------------------
    #----------------------------------
    # 라틴계 문자         # https://unicode.org/charts/nameslist/ 참조
    elif((ord_char >= ord('À')) and (ord_char <= ord('Ö'))): 
        return 글자상태_라틴어 # Latin-1 Supplement 0x00C0(À) ~ 0x00D6(Ö)
    elif((ord_char >= ord('Ø')) and (ord_char <= ord('ö'))): 
        return 글자상태_라틴어 # Latin-1 Supplement 0x00D8(Ø) ~ 0x00F6(ö)
    elif((ord_char >= ord('ø')) and (ord_char <= ord('ÿ'))):
        return 글자상태_라틴어 # Latin-1 Supplement 0x00F8(ø) ~ 0x00FF(ÿ)
    elif((ord_char >= ord('Ā')) and (ord_char <= ord('ſ'))): 
    #----- 
        return 글자상태_라틴어 # Latin Extended-A 0x0100(Ā) ~ 0x017F(ſ) <= European Latin
    elif((ord_char >= 0x1E00) and (ord_char <= 0x1EFF)): 
        return 글자상태_라틴어 # Latin Extended Additional 0x1E00(Ḁ) ~ 0x1EFF(ỿ)
    elif((ord_char >= ord('ƀ')) and (ord_char <= ord('ƿ'))): 
    #----- 
        return 글자상태_라틴어 # Latin Extended-B 0x0180(ƀ) ~ 0x01BF(ƿ) <= Non-European and historic Latin ...
    elif((ord_char >= ord('Ǆ')) and (ord_char <= ord('ɏ'))): 
        return 글자상태_라틴어 # Latin Extended-B 0x01C4(Ǆ) ~ 0x024F(ɏ)
    #----- 
    elif((ord_char >= 0x0250) and (ord_char <= 0x02AF)): 
        return 글자상태_라틴어 # IPA Extensions 0x0250(ɐ) ~ 0x02AF(ʯ)
    #----- 
    elif((ord_char >= 0x02B0) and (ord_char <= 0x02F8)): 
        return 글자상태_라틴어 # Spacing Modifier Letters 0x02B0(ʰ) ~ 0x02F8(˸) [끝은 0x02FF(˿)이지만 알파벳이 아니라서 그 앞에 끝을 잡음]
    #----- 
    elif((ord_char >= 0x0300) and (ord_char <= 0x036F)): 
        return 글자상태_라틴어 # Combining Diacritical Marks 0x0300(◌̀ )~0x036F(◌ͯ )        
    #----- 
    elif((ord_char >= 0x0370) and (ord_char <= 0x03FF)): 
        # 영어 발음기호 글자 중에 [Greek and Coptic]에 있는 것이 있다. 
        # 발음기호 표기 ('θril')에 그리스 문자를 사용하므로 영문자 토큰으로 다뤄야 단어가 끊어지지 않는다.
        return 글자상태_라틴어 # Greek and Coptic 0x0370(Ͱ) ~ 0x03FF(Ͽ)  
    #----- 
    #----- 
    #----- 
    elif((ord_char >= ord('Ⱡ')) and (ord_char <= ord('Ɀ'))): 
        return 글자상태_라틴어3 # Latin Extended-C 0x2C60(Ⱡ) ~ 0x2C7F(Ɀ)
    #----- 
    elif((ord_char >= 0xA720) and (ord_char <= 0xA7FF)): 
        return 글자상태_라틴어4 # Latin Extended-D 0xA720(꜠) ~ 0xA7FF(ꟿ)
    #----- 
    elif((ord_char >= 0xAB30) and (ord_char <= 0xAB67)): 
        return 글자상태_라틴어5 # Latin Extended-E 0xAB30(ꬰ) ~ 0xAB67(ꭧ)
    #----- 
    #----- 
    #----- 
    elif((ord_char >= 0x1D00) and (ord_char <= 0x1D7F)): 
        return 글자상태_음성 # Phonetic Extensions 0x1D00(ᴀ) ~ 0x1D7F(ᵿ)
    elif((ord_char >= 0x1D80) and (ord_char <= 0x1DBF)): 
        return 글자상태_음성 # Phonetic Extensions Supplement 0x1D80(ᶀ) ~ 0x1DBF(ᶿ)
    #----- 
    elif((ord_char >= 0x0400) and (ord_char <= 0x04FF)): 
        return 글자상태_키릴 # Cyrillic 0x0400(Ѐ) ~ 0x04FF(ӿ)
    #----- 
    elif((ord_char >= 0x0600) and (ord_char <= 0x06FF)): 
        return 글자상태_아랍어 # Arabic 0x0600(؀ ) ~ 0x06FF(‎ۿ‎)
    elif((ord_char >= 0x08A0) and (ord_char <= 0x08FF)): 
        return 글자상태_아랍어 # Arabic Extended-A 0x08A0(‎ࢠ) ~ 08FF(◌ࣿ) # 화면에 다르게 보인다.  
    #----------------------------------
    #----------------------------------
    elif(ord_char >= 128): 
        return 글자상태_엑스  # extra
    else: 
        return 글자상태_널 # 0x00 Zero

def get_script_name(script, HangulName=False):
    # old: get_char_type_fullname
    if(script == 글자상태_한글): 
        if(HangulName==True): return '한글'
        else: return 'Han'
    elif(script == 글자상태_영문자): 
        if(HangulName==True): return '영문자'
        else: return 'Eng'
    elif(script == 글자상태_숫자): 
        if(HangulName==True): return '숫자'
        else: return 'Num'
    elif(script == 글자상태_공백): 
        return 'Spc'
    elif(script == 글자상태_탭): return 'Tab'
    elif(script == 글자상태_리턴): return 'CR'
    elif(script == 글자상태_줄바꿈): return 'LF'
    elif(script == 글자상태_기호): return 'Sign'
    elif(script == 글자상태_자모): 
        if(HangulName==True): return '한글자모'
        else: return 'Jamo'
    elif(script == 글자상태_한자): 
        if(HangulName==True): return '한자'
        else: return 'Hanja'
    elif(script == 글자상태_일문자): 
        if(HangulName==True): return '일본가나'
        else: return 'Japan'
    elif(script == 글자상태_라틴어): return 'Latin' 
    elif(script == 글자상태_라틴어3): return 'Latin3'
    elif(script == 글자상태_라틴어4): return 'Latin4'
    elif(script == 글자상태_라틴어5): return 'Latin5'
    elif(script == 글자상태_음성): return 'Phonetic' # Phonetic Extensions 1D00(ᴀ) ~ 1D7F(ᵿ)
    elif(script == 글자상태_키릴): 
        if(HangulName==True): return '키릴문자'
        else: return 'Cyrillic' # Cyrillic 0400(Ѐ) ~ 04FF(ӿ)
    elif(script == 글자상태_아랍어): return 'Arabic'   # Arabic 0600(؀ ) ~ 06FF(‎ۿ‎)
    #----- 
    elif(script == 글자상태_엑스): return 'Extra'
    elif(script == 글자상태_널): return 'Zero'
    #----------------------------------
    #----------------------------------
    else:return 글자상태_몰라

_keyword_char_state_list_ = [
    글자상태_한글, # 'Han'
    글자상태_영문자, # 'Eng'
    글자상태_숫자, # 'Num'
    글자상태_자모, # 'Jamo'
    글자상태_한자, # 'Hanja'
    글자상태_일문자, # 'Japan'
    글자상태_라틴어, # 'Latin'
    글자상태_라틴어3, # 'Latin3'
    글자상태_라틴어4, # 'Latin4'
    글자상태_라틴어5, # 'Latin5'
    글자상태_음성, # 'Phonetic' # Phonetic Extensions 1D00(ᴀ) ~ 1D7F(ᵿ)
    글자상태_키릴, # 'Cyrillic' # Cyrillic 0400(Ѐ) ~ 04FF(ӿ)
    글자상태_아랍어, # 'Arabic'   # Arabic 0600(؀ ) ~ 06FF(‎ۿ‎)
]
_non_keyword_char_state_list_ = [
    글자상태_공백,# space
    글자상태_탭,# tab
    글자상태_리턴,# carrage-return
    글자상태_줄바꿈,# line-feed
    글자상태_기호,# sign
    글자상태_엑스,# extra
    글자상태_널, # 0x00 Zero
]

def _is_script_keyword_old(script):
    # old: is_char_type_keyword
    '''
    if(script == 글자상태_한글): return True # 'Han'
    elif(script == 글자상태_영문자): return True # 'Eng'
    elif(script == 글자상태_숫자): return True # 'Num'
    elif(script == 글자상태_자모): return True # 'Jamo'
    elif(script == 글자상태_한자): return True # 'Hanja'
    elif(script == 글자상태_일문자): return True # 'Japan'
    elif(script == 글자상태_라틴어): return True # 'Latin'
    elif(script == 글자상태_라틴어3): return True # 'Latin3'
    elif(script == 글자상태_라틴어4): return True # 'Latin4'
    elif(script == 글자상태_라틴어5): return True # 'Latin5'
    elif(script == 글자상태_음성): return True # 'Phonetic' # Phonetic Extensions 1D00(ᴀ) ~ 1D7F(ᵿ)
    elif(script == 글자상태_키릴): return True # 'Cyrillic' # Cyrillic 0400(Ѐ) ~ 04FF(ӿ)
    elif(script == 글자상태_아랍어): return True # 'Arabic'   # Arabic 0600(؀ ) ~ 06FF(‎ۿ‎)
    else: return False
    '''
    if script in _keyword_char_state_list_:
        return True
    else: 
        return False

def is_2byte_Compatibility_unit(char1):
    # CJK Compatibility 중에서 영문자로 된 단위
    if(len(char1) != 1): # 1글자만 허용
        return False
    ord_char = ord(char1)
    if((ord_char >= 0x3371) and (ord_char <= 0x337A)):
        return True # Squared Latin abbreviations // 3371 ㍱ SQUARE HPA(h P a) // 337A  SQUARE IU(I U)
    elif((ord_char >= 0x3380) and (ord_char <= 0x33DF)):
        # Squared Latin abbreviations or Abbreviations involving liter symbols
        # 3380 ㎀ SQUARE PA AMPS (p A) ~ 33DF  SQUARE A OVER M (A ∕ m)
        return True
    else:
        return False

def get_scripts(str):
    # old: get_string_char_type_string
    # old: get_char_type_string__string
    hglen = len(str)
    scripts = '';
    for i in range(hglen):
        char1 = str[i]
        script1 = get_script(char1)
        if(script1 != 0):
            scripts += get_script(char1)
        else:
            print('logic error: get_script(char1) == 0')
            print(str)
            return scripts
    return scripts

def get_keyword_type_num__scripts(scripts):
    # old: get_keyword_type_num__chartype_string
    hglen = len(scripts)
    keyword_type_num = 0
    for i in range(0, hglen):
        if(scripts[i] in _keyword_char_state_list_):
            keyword_type_num += 1
    return keyword_type_num

def print_scripts__string(str, type_fullname=False, sep='\t'):
    # old: print_string_char_type
    # old: print_char_type_string__string
    hglen = len(str)
    print ("string len : ", hglen)
    print('순서:', sep, '글자', sep, '십진수', sep, '16진수', sep, '(스크립트)')
    for i in range(0, hglen):
        char1 = str[i]
        script1 = get_script(char1)
        if(type_fullname==True):
            script1 = get_script_name(script1);
        char_code_value_string = get_char_code_value_string3(char1, sep=sep)
        print('%i:' %i, sep, char_code_value_string, sep, '(', script1, ')')
    print ("")

def get_script_list(str):
    # old: get_string_char_type_list
    # old: get_char_type_list__string
    # old: get_script_list__string
    hglen = len(str)
    scripts = get_scripts(str)
    scripts_len = len(scripts)
    #print ("string  len: ", hglen)
    #print ("char type len: ", scripts_len)
    #print ("char type list: ", scripts)

    #####
    script_list = []
    if(hglen <= 0): # 외부에서 실수로 내용이 없는 문자열을 전달할 수도 있다.
        return script_list
        
    #######################################
    ##script_rec = {
    ##'script': '',  # 문자 상태
    ##'pos': -1,     # 문자열에서 토큰 위치
    ##'len': 0,      # 토큰 길이
    ##'string': ''   # 토큰 문자열
    ##'ending': None #맨 끝에 있는 토큰(복합 토큰에서 사용)
    ##}
    #######################################

    script_pre = ''
    pos_pre = -1
    samecnt = 0
    for i in range(0, hglen):
        script = scripts[i]
        if(script_pre == script):
            samecnt += 1
        else: # 문자 상태가 달라도 {한글, 영문자}는 추가 검사를 한다.
            if((script_pre == 글자상태_한글) and (script == 글자상태_자모)): # {한글음절+한글자모}
                samecnt += 1
            elif((script_pre == 글자상태_자모) and (script == 글자상태_한글)): # {한글자모+한글음절}
                samecnt += 1
            elif((script_pre == 글자상태_영문자) and (script == 글자상태_라틴어)): # {영문자+라틴확장}
                samecnt += 1
            elif((script_pre == 글자상태_라틴어) and (script == 글자상태_영문자)): # {라틴확장+영문자}
                samecnt += 1
            else:
                if(i != 0): # first-item
                    wordlen = (samecnt + 1)
                    word = str[pos_pre: (pos_pre + wordlen)]
                    script_rec = {
                        'script': script_pre, # 문자 상태
                        'pos': pos_pre,       # 문자열에서 토큰 위치
                        'len': wordlen,       # 토큰 길이
                        'string': word,       # 토큰 문자열
                        #'ending': None,      #맨 끝에 있는 토큰(복합 토큰에서 사용)
                    }
                    script_list.append(script_rec)
                    #print ('cur-state (%i) :' %i, '[' + script_pre, '-', script +']')

                script_pre = script
                samecnt = 0
                pos_pre = i

    if((i + 1) == hglen): # last-item
        wordlen = (samecnt + 1)
        word = str[pos_pre: (pos_pre + wordlen)]

        script_rec = {
            'script': script_pre, # 문자 상태
            'pos': pos_pre,       # 문자열에서 토큰 위치
            'len': wordlen,       # 토큰 길이
            'string': word,       # 토큰 문자열
            #'ending': None,      #맨 끝에 있는 토큰(복합 토큰에서 사용)
        }
        script_list.append(script_rec)
        #print ('cur-state (%i) :' %i, '[' + script_pre, '-', script +']')
    if(len(script_list) <= 0):
        print('i : %i' %i)
        print('logic error: empty script_list')
    #print('script_list : ', script_list)
    return script_list

def print_script_list(script_list, no_print_ending = True, no_print_white_char = False, simple_print = False):
    # old: print_chartype_list
    if(script_list == None): return
    script_list_len = len(script_list)
    #print( "script list len : " , script_list_len)

    for i in range(0, script_list_len):
        script_rec = dict(script_list[i])
        if(no_print_white_char == True):
            if((script_rec['script'] == 글자상태_공백) or (script_rec['script'] == 글자상태_탭)): # space or tab
                continue
        if(no_print_ending == True):
            if 'ending' in script_rec: del script_rec['ending']
        if(simple_print == True):
            print( "%i :\t" %i, script_rec['string'] + '\t[', script_rec['pos'], ':', script_rec['len'], ']' )
        else:
            print( "%i :\t" %i, script_rec)

def get_hybrid_script2(script_first, script_second):
    #script_rec = { 'script': '', 'pos': -1, 'len': 0, 'string': '', 'ending': None}

    hybrid_type = False
    if(script_first['script'] == 글자상태_숫자):
        if(script_second['script'] == 글자상태_한글): # 1월
            hybrid_type = True
        elif(script_second['script'] == 글자상태_영문자): # 10cm
            hybrid_type = True
        elif(script_second['len'] == 1):
                if(is_2byte_Compatibility_unit(script_second['string']) == True):
                    hybrid_type = True # 2000㏄    3000㏄  (㏄: 영문자 c의 연속이 아니다.)

    elif(script_first['script'] == 글자상태_영문자):
        if((script_second['script'] == 글자상태_한글) or (script_second['script'] == 글자상태_숫자)): # K리그
            hybrid_type = True
    elif(script_first['script'] == 글자상태_한글):
        if(script_second['script'] == 글자상태_영문자): # 한미FTA
            hybrid_type = True
        elif(script_second['script'] == 글자상태_숫자): # 미그21
            hybrid_type = True
        elif(script_second['script'] == 글자상태_한자): # 중앙亞
            hybrid_type = True
    elif(script_first['script'] == 글자상태_한자):
        if(script_second['script'] == 글자상태_한글): # 李총리
            hybrid_type = True
    elif(script_first['string'] == '-'):
        if(script_second['script'] == 글자상태_숫자): # -17
            hybrid_type = True
    elif(script_first['string'] == '+'):
        if(script_second['script'] == 글자상태_숫자): # +15
            hybrid_type = True
    elif(script_first['string'] == '$'):
        if(script_second['script'] == 글자상태_숫자): # $10
            hybrid_type = True

    if(hybrid_type == True):
        script_new = dict(script_first);
        script_new['script'] += script_second['script']
        script_new['len'] += script_second['len']
        script_new['string'] += script_second['string']

        script_new['ending'] = dict(script_second)
        return script_new
    else:
        return None

def get_hybrid_script3(script_first, script_second, script_third):
    #script_rec = { 'script': '', 'pos': -1, 'len': 0, 'string': '', 'ending': None}

    hybrid_type = False
    if(script_first['script'] == 글자상태_숫자):
        if((script_second['string'] == '.') or (script_second['string'] == '/')):
            if(script_third['script'] == 글자상태_숫자): # 1.5   1/5
                hybrid_type = True
        elif(script_second['script'] == 글자상태_영문자):
            if(script_third['script'] == 글자상태_한글): # 26cm의
                hybrid_type = True
        elif(script_second['script'] == 글자상태_한글):
            if(script_third['script'] == 글자상태_영문자): # 2천CC
                hybrid_type = True
        elif(script_second['len'] == 1):
                if(is_2byte_Compatibility_unit(script_second['string']) == True):
                    if(script_third['script'] == 글자상태_한글):
                        hybrid_type = True # 2000㏄급  3000㏄급  (㏄: 영문자 c의 연속이 아니다.)

    elif(script_first['script'] == 글자상태_영문자):
        if(script_second['string'] == '&'):
            if(script_third['script'] == 글자상태_영문자): # m&a  r&d
                hybrid_type = True
        elif(script_second['string'] == '-'):
            if(script_third['script'] == 글자상태_영문자): # out-performed
                hybrid_type = True
            elif(script_third['script'] == 글자상태_한글): # CD-롬  D-데이
                hybrid_type = True
            if(script_third['script'] == 글자상태_숫자): # D-3
                hybrid_type = True
        elif(script_second['string'] == "'"):
            if(script_third['script'] == 글자상태_영문자): # didn't  Here's
                hybrid_type = True
        elif(script_second['string'] == "+"):
            if(script_third['script'] == 글자상태_영문자): # ctl+v
                hybrid_type = True

    elif(script_first['script'] == 글자상태_한글):
        if(script_second['string'] == '·'):
            if(script_third['script'] == 글자상태_한글): # 한·일
                # 첫 스크립트는 1음절로 제한한다. 2음절 이상은 어색한 것이 많다.
                if(script_first['len'] == 1):
                    hybrid_type = True
        elif(script_second['string'] == '-'):
            if(script_third['script'] == 글자상태_숫자): # 미그-21
                hybrid_type = True
            if(script_third['script'] == 글자상태_영문자): # 스커드-C
                hybrid_type = True
                
        elif(script_second['script'] == 글자상태_숫자):
            if(script_third['script'] == 글자상태_한글): # 천5백  세계1위
                hybrid_type = True
        elif(script_second['script'] == 글자상태_영문자):
            if(script_third['script'] == 글자상태_숫자): # 갤S10
                hybrid_type = True
            elif(script_third['script'] == 글자상태_한글): # 벙커C유
                hybrid_type = True

    elif(script_first['string'] == '-'):
        if(script_second['script'] == 글자상태_숫자):
            if(script_third['script'] == 글자상태_한글): # -17도
                hybrid_type = True
    elif(script_first['string'] == '+'):
        if(script_second['script'] == 글자상태_숫자):
            if(script_third['script'] == 글자상태_한글): # +17도
                hybrid_type = True

    if(hybrid_type == True):
        script_new = dict(script_first);
        script_new['script'] += script_second['script']
        script_new['len'] += script_second['len']
        script_new['string'] += script_second['string']

        script_new['script'] += script_third['script']
        script_new['len'] += script_third['len']
        script_new['string'] += script_third['string']

        script_new['ending'] = dict(script_third)
        return script_new
    else:
        return None

def get_hybrid_script4(script_first, script_second, script_third, script_forth):
    #script_rec = { 'script': '', 'pos': -1, 'len': 0, 'string': '', 'ending': None}

    hybrid_type = False
    if(script_first['script'] == 글자상태_숫자):
        if(script_second['string'] == '.'):
            if(script_third['script'] == 글자상태_숫자): # 1.5
                if(script_forth['script'] == 글자상태_한글): # 1.5미터
                    hybrid_type = True
                elif(script_forth['string'] == '$'): # 10.5$
                    hybrid_type = True
                elif(script_forth['string'] == '%'): # 0.5%
                    hybrid_type = True
                elif(script_forth['script'] == 글자상태_영문자): # 16.6g
                    hybrid_type = True
        elif(script_second['string'] == '/'):
            if(script_third['script'] == 글자상태_숫자): # 1/4
                if(script_forth['script'] == 글자상태_한글): # 2/4분기
                    hybrid_type = True
        elif(script_second['script'] == 글자상태_한글):
            if(script_third['script'] == 글자상태_숫자):
                if(script_forth['script'] == 글자상태_한글): # 1시5분
                    hybrid_type = True
        elif(script_second['script'] == 글자상태_영문자):
            if(script_third['string'] == '/'):
                if(script_forth['script'] == 글자상태_영문자): # 80km/h
                    hybrid_type = True

    elif(script_first['script'] == 글자상태_영문자):
        if(script_second['string'] == '.'):
            if(script_third['script'] == 글자상태_영문자): # m&a  r&d
                if(script_forth['string'] == '.'): # U.S.
                    hybrid_type = True                
        elif(script_second['script'] == 글자상태_숫자):
            if(script_third['script'] == 글자상태_영문자): 
                if(script_forth['script'] == 글자상태_숫자): # H5N1
                    hybrid_type = True                
            elif(script_third['string'] == '-'): 
                if(script_forth['script'] == 글자상태_한글): # A1-광구
                    hybrid_type = True                
    
    elif(script_first['script'] == 글자상태_한글):
        if(script_second['script'] == 글자상태_영문자):
            if((script_third['string'] == '/') or (script_third['string'] == '.') or (script_third['string'] == '&')):
                if(script_forth['script'] == 글자상태_영문자): # 유실방지대책T/F  워싱턴D.C  나라M&D
                    hybrid_type = True                
    
    elif((script_first['string'] == '-') or (script_first['string'] == '+')):
        if(script_second['script'] == 글자상태_숫자):
            if(script_third['script'] == '.'):
                if(script_forth['script'] == 글자상태_숫자): # -1.7    +1.7
                    hybrid_type = True
    
    elif(script_first['string'] == '$'):
        if(script_second['script'] == 글자상태_숫자):
            if(script_third['script'] == '.'):
                if(script_forth['script'] == 글자상태_숫자): # $1.7
                    hybrid_type = True

    if(hybrid_type == True):
        script_new = dict(script_first);
        script_new['script'] += script_second['script']
        script_new['len'] += script_second['len']
        script_new['string'] += script_second['string']

        script_new['script'] += script_third['script']
        script_new['len'] += script_third['len']
        script_new['string'] += script_third['string']

        script_new['script'] += script_forth['script']
        script_new['len'] += script_forth['len']
        script_new['string'] += script_forth['string']

        script_new['ending'] = dict(script_forth)
        return script_new
    else:
        return None

def get_hybrid_script5(script_first, script_second, script_third, script_forth, script_fifth):
    #script_rec = { 'script': '', 'pos': -1, 'len': 0, 'string': '', 'ending': None}

    hybrid_type = False
    if((script_first['string'] == '-') or (script_first['string'] == '+')):
        if(script_second['script'] == 글자상태_숫자):
            if(script_third['string'] == '.'): # -17.
                if(script_forth['script'] == 글자상태_숫자): # -17.1
                    if(script_fifth['script'] == 글자상태_한글): # -17.1도    +17.1도
                        hybrid_type = True
    elif(script_first['script'] == 글자상태_숫자):
        if(script_second['string'] == '.'):
            if(script_third['script'] == 글자상태_숫자): # 1.5
                if(script_forth['string'] == '.'): # 2019.1.
                    if(script_fifth['script'] == 글자상태_숫자): # 2019.1.1
                        hybrid_type = True
        elif(script_second['string'] == '/'):
            if(script_third['script'] == 글자상태_숫자): # 1/5
                if(script_forth['string'] == '/'): # 2019/1/
                    if(script_fifth['script'] == 글자상태_숫자): # 2019/1/1
                        hybrid_type = True
        elif(script_second['string'] == '-'):
            if(script_third['script'] == 글자상태_영문자): # 10-year
                if(script_forth['string'] == '-'): # 10-year-
                    if(script_fifth['script'] == 글자상태_영문자): # 10-year-old
                        hybrid_type = True
    elif(script_first['script'] == 글자상태_영문자):
        if(script_second['string'] == '-'):
            if(script_third['script'] == 글자상태_영문자):
                if(script_forth['string'] == '-'):
                    if(script_fifth['script'] == 글자상태_영문자): # commander-in-chief
                        hybrid_type = True
        elif(script_second['string'] == '.'):
            if(script_third['script'] == 글자상태_영문자):
                if(script_forth['string'] == '.'):
                    if(script_fifth['script'] == 글자상태_영문자): # edition.cnn.com
                        hybrid_type = True
    #elif(script_first['script'] == 글자상태_한글):
    #    if(script_second['string'] == '·'):
    #        if(script_third['script'] == 글자상태_한글): # 한·일
    #            hybrid_type = True
    #    elif(script_second['script'] == 글자상태_숫자):
    #        if(script_third['script'] == 글자상태_한글): # 천5백  세계1위
    #            hybrid_type = True

    if(hybrid_type == True):
        script_new = dict(script_first);
        script_new['script'] += script_second['script']
        script_new['len'] += script_second['len']
        script_new['string'] += script_second['string']

        script_new['script'] += script_third['script']
        script_new['len'] += script_third['len']
        script_new['string'] += script_third['string']

        script_new['script'] += script_forth['script']
        script_new['len'] += script_forth['len']
        script_new['string'] += script_forth['string']

        script_new['script'] += script_fifth['script']
        script_new['len'] += script_fifth['len']
        script_new['string'] += script_fifth['string']

        script_new['ending'] = dict(script_fifth)
        return script_new
    else:
        return None

def get_hybrid_script_list5(script_list):
    script_list_len = len(script_list)
    #print( "script list len : " , script_list_len)

    #script_rec = { 'script': '', 'pos': -1, 'len': 0, 'string': '', 'ending': None}

    hybrid_script_list = []
    script_rec_pre4 = None
    script_rec_pre3 = None
    script_rec_pre2 = None
    script_rec_pre = None
    script_rec = None
    for i in range(script_list_len):        
        script_rec = script_list[i]
        if(script_rec_pre != None):   # 2개
            if(script_rec_pre2 != None):  # 3개
                if(script_rec_pre3 != None):  # 4개
                    if(script_rec_pre4 != None):  # 5개
                        hybrid_script = get_hybrid_script5(script_rec_pre4, script_rec_pre3, script_rec_pre2, script_rec_pre, script_rec)
                        if(hybrid_script != None):
                            #print( "dbg: (4) %i (hybrid_script != None)" %i)
                            hybrid_script_list.append(hybrid_script)
                            script_rec_pre4 = None
                            script_rec_pre3 = None
                            script_rec_pre2 = None
                            script_rec_pre = None
                            script_rec = None

        if(script_rec_pre4 != None): # 1개 처리
            #print( "dbg: (1) %i (script_rec_pre4 != None)" %i)
            hybrid_script_list.append(script_rec_pre4)

        script_rec_pre4 = script_rec_pre3
        script_rec_pre3 = script_rec_pre2
        script_rec_pre2 = script_rec_pre
        script_rec_pre = script_rec
        ### goto for-loop back 

    if(script_rec_pre4 != None): #last
        hybrid_script_list.append(script_rec_pre4)
    if(script_rec_pre3 != None): #last
        hybrid_script_list.append(script_rec_pre3)
    if(script_rec_pre2 != None): #last
        hybrid_script_list.append(script_rec_pre2)
    if(script_rec_pre != None): #last
        hybrid_script_list.append(script_rec_pre)

    return hybrid_script_list

def get_hybrid_script_list4(script_list):
    script_list_len = len(script_list)
    #print( "script list len : " , script_list_len)

    #script_rec = { 'script': '', 'pos': -1, 'len': 0, 'string': '', 'ending': None}

    hybrid_script_list = []
    script_rec_pre3 = None
    script_rec_pre2 = None
    script_rec_pre = None
    script_rec = None
    for i in range(script_list_len):        
        script_rec = script_list[i]
        if(script_rec_pre != None):   # 2개
            if(script_rec_pre2 != None):  # 3개
                if(script_rec_pre3 != None):  # 4개
                    hybrid_script = get_hybrid_script4(script_rec_pre3, script_rec_pre2, script_rec_pre, script_rec)
                    if(hybrid_script != None):
                        #print( "dbg: (4) %i (hybrid_script != None)" %i)
                        hybrid_script_list.append(hybrid_script)
                        script_rec_pre3 = None
                        script_rec_pre2 = None
                        script_rec_pre = None
                        script_rec = None

        if(script_rec_pre3 != None): # 1개 처리
            #print( "dbg: (1) %i (script_rec_pre3 != None)" %i)
            hybrid_script_list.append(script_rec_pre3)

        script_rec_pre3 = script_rec_pre2
        script_rec_pre2 = script_rec_pre
        script_rec_pre = script_rec
        ### goto for-loop back 

    if(script_rec_pre3 != None): #last
        hybrid_script_list.append(script_rec_pre3)
    if(script_rec_pre2 != None): #last
        hybrid_script_list.append(script_rec_pre2)
    if(script_rec_pre != None): #last
        hybrid_script_list.append(script_rec_pre)

    return hybrid_script_list

def get_hybrid_script_list3(script_list):
    script_list_len = len(script_list)
    #print( "script list len : " , script_list_len)

    #script_rec = { 'script': '', 'pos': -1, 'len': 0, 'string': '', 'ending': None}

    hybrid_script_list = []
    script_rec_pre2 = None
    script_rec_pre = None
    script_rec = None
    for i in range(script_list_len):        
        script_rec = script_list[i]
        if(script_rec_pre != None):   # 2개
            if(script_rec_pre2 != None):  # 3개
                hybrid_script = get_hybrid_script3(script_rec_pre2, script_rec_pre, script_rec)
                if(hybrid_script != None):
                    #print( "dbg: (3) %i (hybrid_script != None)" %i)
                    hybrid_script_list.append(hybrid_script)
                    script_rec_pre2 = None
                    script_rec_pre = None
                    script_rec = None

        if(script_rec_pre2 != None): # 1개 처리
            #print( "dbg: (1) %i (script_rec_pre2 != None)" %i)
            hybrid_script_list.append(script_rec_pre2)

        script_rec_pre2 = script_rec_pre
        script_rec_pre = script_rec
        ### goto for-loop back 

    if(script_rec_pre2 != None): #last
        hybrid_script_list.append(script_rec_pre2)
    if(script_rec_pre != None): #last
        hybrid_script_list.append(script_rec_pre)

    return hybrid_script_list

def get_hybrid_script_list2(script_list):
    script_list_len = len(script_list)
    #print( "script list len : " , script_list_len)

    #script_rec = { 'script': '', 'pos': -1, 'len': 0, 'string': '', 'ending': None}

    hybrid_script_list = []
    script_rec_pre = None
    script_rec = None
    i = 0
    while (i < script_list_len):
        script_rec = script_list[i]
        if(script_rec_pre != None):
            hybrid_script = get_hybrid_script2(script_rec_pre, script_rec)

            if(hybrid_script != None):
                #print( "dbg: %i (hybrid_script != None)" %i)
                hybrid_script_list.append(hybrid_script)
                script_rec = None
            else:
                #print( "dbg: %i (hybrid_script == None)" %i)
                hybrid_script_list.append(script_rec_pre)

        script_rec_pre = script_rec
        i += 1

    if(script_rec != None): #last
        hybrid_script_list.append(script_rec)

    return hybrid_script_list

def get_hybrid_script_list(script_list):
    hybrid_script_list5 = get_hybrid_script_list5(script_list)
    #print_script_list(hybrid_script_list5)

    hybrid_script_list4 = get_hybrid_script_list4(hybrid_script_list5)
    #print_script_list(hybrid_script_list4)

    hybrid_script_list3 = get_hybrid_script_list3(hybrid_script_list4)
    #print_script_list(hybrid_script_list3)

    hybrid_script_list2 = get_hybrid_script_list2(hybrid_script_list3)
    return hybrid_script_list2

def get_script_list_text(script_list):
    # old: get_chartype_list_text
    script_list_len = len(script_list)
    #print( "script list len : " , script_list_len)

    #script_rec = { 'script': '', 'pos': -1, 'len': 0, 'string': '', 'ending': None}

    script_list_text = '';
    for i in range(script_list_len):        
        script_list_text += script_list[i]['string']
        i += 1

    return script_list_text

def HGGetToken(str, debugflag = False, no_print_ending=True, 
    no_print_white_char=False, simple_print=False):
    # old: get_string_char_type
    # old: GetCharTypeList_String
    # old: GetScriptList
    if(debugflag == True): 
        print("<script list>")
    str_script_list = get_script_list(str)
    if(debugflag == True): 
        print_script_list(str_script_list)

    if(debugflag == True): 
        print("\r\n<hybrid script list>")
    new_str_script_list = get_hybrid_script_list(str_script_list)# 스크립트 합성 => 토큰 변환
    if(debugflag == True): 
        print_script_list(new_str_script_list, no_print_ending, no_print_white_char, simple_print)

    return new_str_script_list

def GetStringListByScriptList(script_list):
    # old: make_word_tok_by_script_list
    if(script_list == None): return None
    script_list_len = len(script_list)
    #print( "script list len : " , script_list_len)

    string_list = []
    for i in range(0, script_list_len):
        script_rec = script_list[i]
        string_list.append(script_rec['string'])
    return string_list

def MakeWordTokByScriptList(script_list, debugPrint=False):
    # old: make_word_tok_by_script_list
    if(script_list == None): return None
    script_list_len = len(script_list)
    #print( "script list len : " , script_list_len)

    tok_list = []
    for i in range(script_list_len):
        script_rec = script_list[i]
        if(debugPrint == True):
            print('script_rec:', script_rec)
            
        if(script_rec['script'] in _keyword_char_state_list_): 
            pass
        elif(script_rec['script'] in _non_keyword_char_state_list_): 
            continue
        else:
            if(len(script_rec['script']) <= 1):
                continue
            if(get_keyword_type_num__scripts(script_rec['script']) <= 0):
                if(debugPrint == True):
                    print('continue # kwd type 하나도 없는 경우')
                continue # kwd type 하나도 없는 경우
            else: # type 2ㄱㅐ 이상
                pass
        #
        tok_list.append(script_rec['string'])
    #
    return tok_list

def DelNonKeywordScript(script_list):
    if(script_list == None): return 
    script_list_len = len(script_list)
    #print( "script list len : " , script_list_len)

    i = 0
    while (i < script_list_len):
        #print(i, ':', script_list[i])
        script_rec = script_list[i]
        if(script_rec['script'] in _keyword_char_state_list_): 
            pass
        else:
            if(len(script_rec['script']) <= 1):
                del script_list[i]
                i -= 1
            elif(get_keyword_type_num__scripts(script_rec['script']) <= 0):
                del script_list[i] # kwd type 하나도 없는 경우
                i -= 1
            else: # type 2ㄱㅐ 이상
                pass

        script_list_len = len(script_list)
        #print( "script list len : " , script_list_len)
        i += 1

def HGGetKeywordList(string, debugPrint=False):
    # old: get_word_tok_by_string
    # old: GetWordTokByString
    # old: HGGetWordToken
    str_script_list = HGGetToken(string, debugflag = False)
    if(str_script_list == None): 
        return None
    if(debugPrint == True):
        print('str_script_list:', *str_script_list, sep='\n')
    wordtok = MakeWordTokByScriptList(str_script_list, debugPrint=debugPrint)
    #print (wordtok)
    return wordtok

def test_script(chkstr):
    ##########
    char_type_string = get_scripts(chkstr)
    print('string len :', len(chkstr))
    print(chkstr)
    print('scripts num:', len(char_type_string))
    print(char_type_string)
    print("")

    script_list = get_script_list(chkstr)
    print('script_list num:', len(script_list))
    print("")

    #=token_list = HGGetToken(chkstr)
    token_list = HGGetToken(chkstr, debugflag = True)
    print('token_list num:', len(token_list))
    print("")

    script_list_text = get_script_list_text(token_list)
    print('[Origin Text(' + str(len(chkstr)) + ')]', chkstr)
    print('[New Text(' + str(len(script_list_text)) + ')]', script_list_text)
    if(chkstr != script_list_text):
        print("Error: not same.")
    else: 
        print("Ok: same.")
    print(""), print(""), print("")

def test_script_tok(chkstr, debugPrint=False):
    word_tok = HGGetKeywordList(chkstr, debugPrint=debugPrint)
    print (word_tok)
    print(""), print(""), print("")

def HGTokenize(string, LowerCase=False, tokenType = 'korean'):
    import re

    WordDictList = []
    if(string == None): 
        return WordDictList
    
    #
    if(LowerCase == True): # 소문자화
        string = string.lower()
    
    #=WordList = string.split()
    if(tokenType == 'hgtoken'): # dilimit kwd token
        WordList = HGGetKeywordList(string)
    #=elif(tokenType == 'korean'): # 한글 지원(아직 지원 안 함, 아래로 가서 처리)
    else: # 한글 지원:
        """
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
        아래는 사용하지 않고 참고용으로 남겨둔다.
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
        #-----
        #-----
        # 영문_숫자_한글음절_한자_한글자모_호환자모_히라가나(ぐ,ゟ)_가타카나(゠,ヿ)
        # 포함되는 유형: bag's bag-sender 한·일 韓·美 한ㆍ일
        #  ===> 이건 {_token_connet_???_char_} 처리할 때만 가능
        #-----
        #---
        _token_hgsyllable_ = "가-힣" # 한글 자모
        _token_hgjamo_char_ = "ᄀ-ᇿ" # 한글 자모
        _token_hgjamo_char_ext_a_ = "ꥠ-ꥼ" # 한글 자모 A
        _token_hgjamo_char_ext_b_ = "ힰ-ퟻ" # 한글 자모 B
        _token_hgjamo_compat_char_ = "ㄱ-ㅣㅥ-ㆎ" # 한글 호환 자모

        _token_hgjamo_ = _token_hgjamo_char_
        _token_hgjamo_ = _token_hgjamo_char_ext_a_
        _token_hgjamo_ += _token_hgjamo_char_ext_b_
        _token_hgjamo_ += _token_hgjamo_compat_char_

        _token_hangul_ = _token_hgsyllable_
        _token_hangul_ += _token_hgjamo_
        #---
        _token_hanja_ = "一-鿼"
        _token_japan_ = "ぐ-ゟ゠-ヿ"
        _token_latin_number_ ="0-9"
        _token_latin_basic_ ="a-zA-Z"
        _token_latin_supplement_ ="À-ÿ"
        _token_latin_supplement_a_ ="Ā-ſ"
        _token_latin_supplement_b_ ="ƀ-ɏ"
        #-------------
        #-------------
        
        #---
        _token_char_pattern_ = ""
        _token_char_pattern_ += _token_latin_number_
        _token_char_pattern_ += _token_latin_basic_
        _token_char_pattern_ += _token_latin_supplement_
        _token_char_pattern_ += _token_latin_supplement_a_
        _token_char_pattern_ += _token_latin_supplement_b_

        #---
        _token_char_pattern_ += _token_hangul_
        _token_char_pattern_ += _token_hanja_
        _token_char_pattern_ += _token_japan_

        #---
        #---
        _token_pattern_ = "[" + _token_char_pattern_ + "]+"
        
        #---
        #--- 여기는 로직을 위해 분할 선언한 것을 합친 것이고, 아래는 통합해서 전달한 것
        #=WordList = re.findall(_token_pattern_, string)
        #---
        # 소문자, 대문자, 라틴 보충, 라틴 보충 확장A, 라틴 보충 확장B, 한글 음절, 한글 자모, 한글 자모 확장A, 한글 자모 확장B, 한자, 가나
        WordList = re.findall("[a-zA-ZÀ-ÿĀ-ſƀ-ɏ0-9가-힣ᄀ-ᇿꥠ-ꥼힰ-ퟻㄱ-ㅣㅥ-ㆎ一-鿼ぐ-ゟ゠-ヿ]+", string)
        
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
        """
        #-----
        # 1) re.findall("[\w]+", string) 방식은 접어(예:can't)를 분리하기 때문에 
        # 온전한 접어(예:can't) 형태는 오지 않는 문제가 있다.
        # 2) 접어(예:can't)를 처리하기 위해 작은따옴표 {'}를 추가한 
        # re.findall("[\w']+", string) 방식으로 처리하면 가능하다.
        #-----
        # 토큰 분리
        WordList = list()
        #= TokenList = re.findall("[\w]+", string) # 접어(예:can't) 포함되지 않고 분리됨
        TokenList = re.findall("[\w']+", string) # 접어(예:can't) 포함됨
        for word in TokenList:
            # add-1) 양 끝에 알파벳이 아닌 문자('_') 제거: {_now then_ _common_}
            # add-2) 중간에 알파벳이 아닌 문자('_') 분리: {gentle_men  woman_kind 1_st  21_st  30_th}
            divlist = word.split('_') # {gentle_men  woman_kind 1_st  21_st  30_th}
            if(len(divlist) > 0): # 분리된 단어 목록이 있는 경우
                for reword in divlist:
                    if(len(reword) > 0): # '_' 문자만 있었던 경우에는 분리되면 빈 문자열이 됨
                        WordList.append(reword)
            else:
                WordList.append(word)

        #######################                
        #######################                
        # 아래 코드 보충: 
        # 1) re.findall("[\w]+", string) 방식으로 호출하면 아래 코드는 필요 없지만 
        # 2) 접어(예:can't)를 처리하기 위해 작은따옴표 {'}를 추가한 
        # re.findall("[\w']+", string) 방식으로 처리할 경우에는 아래 코드가 필요하다. 
        # 나중에 코드가 바뀌더라도 실수하지 않도록 필요 없더라도 아래 코드는 계속 유지한다.
        #######################
        #######################
        #---
        # 위에서 연결 문자를 사용할 경우에
        # 단어 앞(prefix)과 뒤(suffix)에서 불필요한 기호 문자 삭제: {'-·ㆍ}
        #---
        _token_connet_eng_char_ = "'" # 영문자 토큰 합성 글자: quatation
        _del_fix_chars_ = _token_connet_eng_char_ # "'" # 영문자 토큰 합성 글자: quatation
        #---
        #=_token_connet_bacic_char_ = ",.\-" # 토큰 합성 글자: minus
        #=_token_connet_hangul_char_ = "·ㆍ" # 한글 토큰 합성 글자: middle-dot, old-hgjamo-a
        #---
        #=_del_fix_chars_ += _token_connet_bacic_char_ # ",.\-" # 토큰 합성 글자: minus
        #---
        WordList = [token.strip(_del_fix_chars_) for token in WordList] 
                
    #print (WordList)
    return WordList

