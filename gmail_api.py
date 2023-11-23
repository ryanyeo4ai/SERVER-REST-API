# -*- coding:utf-8 -*- 
import smtplib 
from email.mime.text import MIMEText 

def sendMail(me, you, msg): 
    smtp = smtplib.SMTP('', 587) 
    smtp.ehlo() 
    smtp.starttls() # TLS 사용시 필요 
    smtp.login(me, '') 
    msg = MIMEText('본문 테스트 메시지') 
    msg['Subject'] = '테스트' 
    msg['To'] = you
    smtp.sendmail(me, you, msg.as_string())
    smtp.quit()

    
if __name__ == "__main__": 
    sendMail('', '', '메일보내기')

