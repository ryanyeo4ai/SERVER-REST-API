from flask import Flask
from flask_mail import Mail, Message
#from app import mail

mail = Mail()

app = Flask(__name__)
mail.init_app(app)

@app.route('/send_email') #get echo api
def send_mail():
    msg = Message('test', sender='inchoon.yeo@gmail.com', recipients=['inchoon.yeo@gmail.com'])        # 메일 세팅
    msg.body = 'only text'        # text body
    msg.html = '<h1>Reset Your Password</h1>'        # html body
    mail.send(msg)      # 메일 발송
    return 'Sent'
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080) 