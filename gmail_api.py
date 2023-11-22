# -*- coding:utf-8 -*- 
import smtplib 
from email.mime.text import MIMEText 

def sendMail(me, you, msg): 
    smtp = smtplib.SMTP('smtp.gmail.com', 587) 
    smtp.ehlo() 
    smtp.starttls() # TLS 사용시 필요 
    smtp.login(me, 'kissme!004') 
    msg = MIMEText('본문 테스트 메시지') 
    msg['Subject'] = '테스트' 
    msg['To'] = you
    smtp.sendmail(me, you, msg.as_string())
    smtp.quit()

    
if __name__ == "__main__": 
    sendMail('paul.yeo94@gmail.com', 'inchoon.yeo@gmail.com', '메일보내기')

