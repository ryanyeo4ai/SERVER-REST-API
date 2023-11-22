import pyotp     # pyotp 
import datetime

def generate_otp():
    # otp에 사용할 키 - base32 방식 A-Z 2-7까지를 이용하고 = 는 채워야하는 공간 패딩 처리용
    otp_key = 'GAYDAMBQGAYDAMBQGAYDAMBQGA======'

    # totp 생성
    totp = pyotp.TOTP(otp_key)
    # 현재 시간 얻기
    now = datetime.datetime.now()

    # 현재 시간 출력
    print('current time : ', now)
    # totp.at을 이용한 TOTP 값 출력, totp.now를 이용한 출력
    otp_data = str(totp.at(datetime.datetime.now()))
    print("now totp.at: " +  str(totp.at(datetime.datetime.now())) + ", totp.now : " + totp.now())
    # 현재 시간에 30초를 더해서 totp.at으로 30초 후 OTP 값을 출력
    print('next otp : ', totp.at(int(now.timestamp())+30))

    return otp_data



    
if __name__ == "__main__":
    send_mail("inchoon.yeo@gmail.com") 