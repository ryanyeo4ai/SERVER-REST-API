from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

user = 'ryan yeo'

pw_hash = bcrypt.generate_password_hash(user)
print(f'pw_hash : {pw_hash}')
print(bcrypt.check_password_hash(pw_hash, user)) # returns True