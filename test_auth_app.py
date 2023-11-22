from flask import Flask
from flask_restx import Resource, Api
from auth import Auth

app = Flask(__name__)
api = Api(
    app,
    version='0.1',
    title="JustKode's API Server",
    description="JustKode's Todo API Server!",
    terms_url="/",
    contact="justkode@kakao.com",
    license="MIT"
)

api.add_namespace(Auth, '/auth')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)