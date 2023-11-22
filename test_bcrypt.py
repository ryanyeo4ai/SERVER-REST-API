from flask import Flask
import bcrypt
 
 
app = Flask(__name__)
 
app.config['SECRET_KEY'] = 'I am your father'
app.config['BCRYPT_LEVEL'] = 10
 
 
# bcrypt = Bcrypt(app)
 
 
pw_hash = bcrypt.hashpw("password".encode("utf-8"), bcrypt.gensalt())
pw_hash2 = bcrypt.hashpw("password".encode("utf-8"), bcrypt.gensalt())
 
utf_8_data = "password".encode("utf-8")
print(f'utf_8_data : {utf_8_data}')
print(f'encoded pw_hash {pw_hash.encode("utf-8")}')
result = bcrypt.checkpw(utf_8_data, pw_hash.encode("utf-8")) # True
print(f'pw_hash : {pw_hash}')
print(f'encrypt password : {bcrypt.hashpw(utf_8_data, bcrypt.gensalt())}')
#즉 password 라는 비밀번호를 암호화하고, 이후에 체크하는 작업을 할때 해당 메소드를 통해 일치여부 확인 가능
 
if pw_hash == pw_hash2 :
    print('True')
else:
    print('False')

print(result)
# 그러나 같은 password를 넣어도 다른 암호화 값이 나온다.