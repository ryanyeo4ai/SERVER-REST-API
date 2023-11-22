from flask import Flask
#import pandas as pd

app = Flask(__name__)
 
@app.route('/')
@app.route('/index')
def index():
    return 'Hello Flask!'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)    
