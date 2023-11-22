from flask import Flask
import ssl

app = Flask(__name__)

@app.route("/")

def hello():

    return "Hello World"

if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='deepbackend_com_cert.cer', keyfile='deepbackend_com.key', password='secret')
    app.run(host="0.0.0.0", port=8080, ssl_context=ssl_context)